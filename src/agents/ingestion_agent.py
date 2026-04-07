"""Ingestion agent: processes legal documents into vector + graph stores."""

import json
from pathlib import Path

from src.config import DATA_DIR


SAMPLE_DOCS_DIR = DATA_DIR / "sample_documents"
ENTITY_ALIASES_FILE = SAMPLE_DOCS_DIR / "_entity_aliases.json"


def _load_documents() -> list[dict]:
    """Load LEX-*.json files from sample_documents directory."""
    docs = []
    if not SAMPLE_DOCS_DIR.exists():
        print(f"[Ingestion] No sample documents directory found at {SAMPLE_DOCS_DIR}")
        return docs

    for fpath in sorted(SAMPLE_DOCS_DIR.glob("LEX-*.json")):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                doc = json.load(f)
                docs.append(doc)
        except Exception as e:
            print(f"[Ingestion] Error loading {fpath.name}: {e}")

    print(f"[Ingestion] Loaded {len(docs)} documents from {SAMPLE_DOCS_DIR}")
    return docs


def _build_static_graph(graph_store):
    """Seed the knowledge graph with static entities and relationships."""
    # Companies
    graph_store.add_company("Bayer AG", jurisdiction="DE", role="acquirer")
    graph_store.add_company("Monsanto Company", jurisdiction="US", role="target")
    graph_store.link_acquisition("Bayer AG", "Monsanto Company", date="2018-06-07", value=63_000_000_000)

    # Products
    graph_store.add_product("Roundup", category="herbicide", active_ingredient="Glyphosate")
    graph_store.add_product("Ranger Pro", category="herbicide", active_ingredient="Glyphosate")

    # Chemicals
    graph_store.add_chemical("Glyphosate", cas_number="1071-83-6", classification="probable_carcinogen_2A")

    # Link products to chemicals
    graph_store.link_product_chemical("Roundup", "Glyphosate")
    graph_store.link_product_chemical("Ranger Pro", "Glyphosate")

    # Link companies to products
    graph_store.link_company_product("Monsanto Company", "Roundup")
    graph_store.link_company_product("Monsanto Company", "Ranger Pro")

    # Regulatory bodies
    regulatory_bodies = [
        ("EPA", "US", "environmental"),
        ("IARC", "INTL", "health"),
        ("BaFin", "DE", "financial"),
        ("Bundeskartellamt", "DE", "antitrust"),
        ("EU Commission", "EU", "antitrust"),
        ("SEC", "US", "securities"),
        ("DOJ", "US", "antitrust"),
    ]
    for name, jur, atype in regulatory_bodies:
        graph_store.add_regulatory_body(name, jurisdiction=jur, authority_type=atype)

    # Regulatory investigations
    graph_store.link_regulatory_investigation("EPA", "Roundup", status="ongoing")
    graph_store.link_regulatory_investigation("IARC", "Roundup", status="classified_2A")

    print("[Ingestion] Static graph entities seeded.")


def _ingest_document_to_graph(doc: dict, graph_store):
    """Add a single document and its relationships to the graph."""
    # Add document node
    graph_store.add_document(doc)

    doc_id = doc["id"]

    # Add companies mentioned and link
    for party in doc.get("parties", []):
        graph_store.add_company(party)
        graph_store.link_document_company(doc_id, party)

    # Add risk factors and link
    for rf in doc.get("risk_factors", []):
        if isinstance(rf, dict):
            graph_store.add_risk_factor(
                rf.get("name", ""),
                category=rf.get("category", ""),
                severity=rf.get("severity", ""),
            )
            graph_store.link_document_risk(doc_id, rf.get("name", ""))
        elif isinstance(rf, str):
            graph_store.add_risk_factor(rf)
            graph_store.link_document_risk(doc_id, rf)

    # Add contract clauses and link
    for clause in doc.get("contract_clauses", []):
        if isinstance(clause, dict):
            graph_store.add_contract_clause(clause)
            graph_store.link_document_clause(doc_id, clause.get("clause_type", ""))
        elif isinstance(clause, str):
            graph_store.add_contract_clause({"clause_type": clause, "summary": "", "language": doc.get("language", "")})
            graph_store.link_document_clause(doc_id, clause)

    # Add cross-references between documents
    for ref_id in doc.get("references", []):
        graph_store.link_document_reference(doc_id, ref_id)

    # Extract legal claims from litigation_filing documents
    if doc.get("doc_type") == "litigation_filing":
        case_name = doc.get("title", f"Claim-{doc_id}")
        monetary_value = doc.get("monetary_value", 0)
        parties = doc.get("parties", [])

        graph_store.add_legal_claim(
            case_name=case_name,
            claim_type="product_liability",
            status="filed",
            jurisdiction=doc.get("jurisdiction", ""),
            filing_date=doc.get("date", ""),
            monetary_value=monetary_value,
        )

        # Link claim to target company (defendant)
        for party in parties:
            if party in ("Monsanto Company", "Bayer AG"):
                graph_store.link_claim_company(case_name, party)

        # Link claim to products mentioned
        content_lower = doc.get("content", "").lower()
        if "roundup" in content_lower:
            graph_store.link_claim_product(case_name, "Roundup")
        if "ranger pro" in content_lower:
            graph_store.link_claim_product(case_name, "Ranger Pro")


def _load_entity_aliases(graph_store):
    """Load cross-lingual entity aliases from _entity_aliases.json."""
    if not ENTITY_ALIASES_FILE.exists():
        print("[Ingestion] No entity aliases file found, skipping.")
        return

    try:
        with open(ENTITY_ALIASES_FILE, "r", encoding="utf-8") as f:
            aliases = json.load(f)

        for canonical, local_names in aliases.items():
            for local_name in local_names:
                # Add the local entity node if it doesn't exist
                graph_store.add_company(local_name)
                graph_store.link_entity_alias(canonical, local_name)

        print(f"[Ingestion] Loaded entity aliases for {len(aliases)} entities.")
    except Exception as e:
        print(f"[Ingestion] Error loading entity aliases: {e}")


def _compute_cross_lingual_similarities(docs: list[dict], embedder, graph_store, threshold: float = 0.75):
    """Compute cross-lingual similarity edges between documents of different languages."""
    # Group documents by language
    by_lang = {}
    for doc in docs:
        lang = doc.get("language", "unknown")
        by_lang.setdefault(lang, []).append(doc)

    languages = list(by_lang.keys())
    if len(languages) < 2:
        print("[Ingestion] Fewer than 2 languages found, skipping cross-lingual similarity.")
        return

    # For each pair of languages, compute pairwise similarities
    edge_count = 0
    for i in range(len(languages)):
        for j in range(i + 1, len(languages)):
            lang_a, lang_b = languages[i], languages[j]
            docs_a = by_lang[lang_a]
            docs_b = by_lang[lang_b]

            # Embed documents from each language
            texts_a = [d.get("content", d.get("summary", ""))[:500] for d in docs_a]
            texts_b = [d.get("content", d.get("summary", ""))[:500] for d in docs_b]

            if not texts_a or not texts_b:
                continue

            embeddings_a = embedder.embed_documents(texts_a)
            embeddings_b = embedder.embed_documents(texts_b)

            import numpy as np
            emb_a = np.array(embeddings_a)
            emb_b = np.array(embeddings_b)
            sim_matrix = emb_a @ emb_b.T

            # Create edges above threshold
            for ai in range(len(docs_a)):
                for bi in range(len(docs_b)):
                    score = float(sim_matrix[ai][bi])
                    if score >= threshold:
                        graph_store.link_similar_documents(
                            docs_a[ai]["id"], docs_b[bi]["id"],
                            score=round(score, 4), cross_lingual=True,
                        )
                        edge_count += 1

    print(f"[Ingestion] Created {edge_count} cross-lingual similarity edges (threshold={threshold}).")


def ingest_documents(embedder, vector_store, graph_store):
    """Full ingestion pipeline: load documents, embed, store in vector + graph."""
    docs = _load_documents()
    if not docs:
        print("[Ingestion] No documents to ingest.")
        return

    # Build static knowledge graph
    _build_static_graph(graph_store)

    # Batch embed all document contents with Harrier
    print(f"[Ingestion] Embedding {len(docs)} documents...")
    contents = [doc.get("content", doc.get("summary", "")) for doc in docs]
    embeddings = embedder.embed_documents(contents)

    # Upsert to Qdrant with metadata
    print("[Ingestion] Upserting to vector store...")
    batch_items = []
    for doc, embedding in zip(docs, embeddings):
        metadata = {
            "title": doc.get("title", ""),
            "content": doc.get("content", "")[:500],
            "summary": doc.get("summary", ""),
            "language": doc.get("language", ""),
            "doc_type": doc.get("doc_type", ""),
            "jurisdiction": doc.get("jurisdiction", ""),
            "date": doc.get("date", ""),
            "parties": doc.get("parties", []),
            "products": doc.get("products", []),
            "risk_factors": [
                rf.get("name", rf) if isinstance(rf, dict) else rf
                for rf in doc.get("risk_factors", [])
            ],
            "monetary_value": doc.get("monetary_value", 0),
        }
        batch_items.append({"id": doc["id"], "vector": embedding, "metadata": metadata})

    vector_store.upsert_batch(batch_items)
    print(f"[Ingestion] Upserted {len(batch_items)} vectors.")

    # Build document graph
    print("[Ingestion] Building knowledge graph...")
    for doc in docs:
        _ingest_document_to_graph(doc, graph_store)

    # Load entity aliases
    _load_entity_aliases(graph_store)

    # Compute cross-lingual similarity edges
    print("[Ingestion] Computing cross-lingual similarities...")
    _compute_cross_lingual_similarities(docs, embedder, graph_store, threshold=0.75)

    print(
        f"[Ingestion] Complete. "
        f"Vectors: {vector_store.count()}, "
        f"Nodes: {graph_store.node_count()}, "
        f"Relationships: {graph_store.relationship_count()}"
    )
