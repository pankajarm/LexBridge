#!/usr/bin/env python3
"""Set up LexBridge databases: generate sample documents, embed, and ingest.

Usage:
    python scripts/setup_databases.py
"""

import json
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.config import DATA_DIR


SAMPLE_DOCS_DIR = DATA_DIR / "sample_documents"

# Sample M&A due diligence documents (EN + DE)
SAMPLE_DOCUMENTS = [
    {
        "id": "LEX-001",
        "title": "Johnson v. Monsanto Company - Product Liability Filing",
        "content": (
            "Plaintiff Dewayne Johnson alleges that prolonged exposure to Monsanto's Roundup "
            "herbicide, containing the active ingredient glyphosate, caused his terminal non-Hodgkin "
            "lymphoma. The plaintiff, a former school groundskeeper, used Roundup and Ranger Pro "
            "regularly as part of his employment duties. Scientific evidence presented includes the "
            "IARC 2015 classification of glyphosate as a probable human carcinogen (Group 2A). "
            "Plaintiff seeks compensatory and punitive damages for failure to warn."
        ),
        "summary": "Product liability lawsuit against Monsanto for Roundup-related cancer claims.",
        "language": "en",
        "doc_type": "litigation_filing",
        "jurisdiction": "US",
        "date": "2018-03-15",
        "parties": ["Monsanto Company"],
        "products": ["Roundup", "Ranger Pro"],
        "risk_factors": [
            {"name": "glyphosate_cancer_risk", "category": "litigation", "severity": "critical"},
            {"name": "failure_to_warn", "category": "litigation", "severity": "high"},
        ],
        "monetary_value": 289000000,
        "confidentiality": "public",
        "contract_clauses": [],
        "references": [],
    },
    {
        "id": "LEX-002",
        "title": "Bayer-Monsanto Merger Agreement - Indemnification Provisions",
        "content": (
            "Section 8.4 of the Merger Agreement between Bayer AG and Monsanto Company provides "
            "for broad indemnification of the Acquirer against pre-closing liabilities. The "
            "indemnification clause covers all pending and future litigation related to Roundup "
            "product liability claims, environmental remediation costs, and regulatory fines. "
            "The cap on indemnification is set at $5 billion, with a basket threshold of $250 million. "
            "Cross-border enforcement provisions specify that German courts shall have jurisdiction "
            "for disputes arising under this section."
        ),
        "summary": "Indemnification provisions in the Bayer-Monsanto merger agreement covering Roundup liabilities.",
        "language": "en",
        "doc_type": "merger_agreement",
        "jurisdiction": "US",
        "date": "2016-09-14",
        "parties": ["Bayer AG", "Monsanto Company"],
        "products": ["Roundup"],
        "risk_factors": [
            {"name": "indemnification_cap_risk", "category": "financial", "severity": "high"},
            {"name": "cross_border_enforcement", "category": "regulatory", "severity": "medium"},
        ],
        "monetary_value": 5000000000,
        "confidentiality": "confidential",
        "contract_clauses": [
            {"clause_type": "indemnification", "summary": "Broad indemnification with $5B cap", "language": "en"},
            {"clause_type": "jurisdiction", "summary": "German courts for dispute resolution", "language": "en"},
        ],
        "references": [],
    },
    {
        "id": "LEX-003",
        "title": "Produkthaftungsklage - Roundup Glyphosat Risikobewertung",
        "content": (
            "Die vorliegende Risikobewertung analysiert die Produkthaftungsrisiken im Zusammenhang "
            "mit dem Herbizid Roundup und seinem Wirkstoff Glyphosat. Nach der Einstufung durch die "
            "IARC als wahrscheinlich krebserregend (Gruppe 2A) im Jahr 2015 sind weltweit ueber "
            "125.000 Klagen eingereicht worden. Die geschaetzte Gesamtexposition belaeuft sich auf "
            "ueber 10 Milliarden USD. Bayer AG traegt als Erwerber von Monsanto Company die volle "
            "Haftung fuer alle bestehenden und zukuenftigen Ansprueche. Die Risikokategorien umfassen "
            "Produkthaftung, regulatorische Risiken und Reputationsrisiken."
        ),
        "summary": "Risikobewertung der Produkthaftung fuer Roundup/Glyphosat nach IARC-Klassifizierung.",
        "language": "de",
        "doc_type": "risk_assessment",
        "jurisdiction": "DE",
        "date": "2019-01-20",
        "parties": ["Bayer AG", "Monsanto Company"],
        "products": ["Roundup"],
        "risk_factors": [
            {"name": "glyphosate_cancer_risk", "category": "litigation", "severity": "critical"},
            {"name": "total_exposure_10B", "category": "financial", "severity": "critical"},
            {"name": "reputational_damage", "category": "reputational", "severity": "high"},
        ],
        "monetary_value": 10000000000,
        "confidentiality": "internal",
        "contract_clauses": [],
        "references": ["LEX-001"],
    },
    {
        "id": "LEX-004",
        "title": "EPA Regulatory Correspondence - Glyphosate Re-registration",
        "content": (
            "The U.S. Environmental Protection Agency (EPA) has completed its interim review of "
            "glyphosate registration. The EPA concludes that glyphosate is not likely to be "
            "carcinogenic to humans, diverging from the IARC classification. However, the EPA "
            "requires updated labeling and risk mitigation measures for ecological risks. Monsanto "
            "Company must submit revised product labels within 180 days. Non-compliance may result "
            "in registration cancellation and additional enforcement actions."
        ),
        "summary": "EPA interim review of glyphosate finding it non-carcinogenic but requiring label updates.",
        "language": "en",
        "doc_type": "regulatory_correspondence",
        "jurisdiction": "US",
        "date": "2020-01-30",
        "parties": ["Monsanto Company"],
        "products": ["Roundup"],
        "risk_factors": [
            {"name": "regulatory_non_compliance", "category": "regulatory", "severity": "medium"},
            {"name": "conflicting_regulatory_findings", "category": "regulatory", "severity": "high"},
        ],
        "monetary_value": 0,
        "confidentiality": "public",
        "contract_clauses": [],
        "references": [],
    },
    {
        "id": "LEX-005",
        "title": "Hardeman v. Monsanto - Settlement Agreement",
        "content": (
            "Settlement Agreement between Edwin Hardeman and Monsanto Company. The parties agree "
            "to settle all claims arising from plaintiff's non-Hodgkin lymphoma allegedly caused by "
            "Roundup exposure. Monsanto agrees to pay $80 million in compensatory damages. The "
            "settlement includes a confidentiality clause, non-admission of liability, and mutual "
            "release of all related claims. The agreement is governed by California law."
        ),
        "summary": "Settlement of Roundup cancer claim for $80M with confidentiality provisions.",
        "language": "en",
        "doc_type": "settlement_agreement",
        "jurisdiction": "US",
        "date": "2019-05-13",
        "parties": ["Monsanto Company"],
        "products": ["Roundup"],
        "risk_factors": [
            {"name": "settlement_precedent", "category": "litigation", "severity": "high"},
        ],
        "monetary_value": 80000000,
        "confidentiality": "confidential",
        "contract_clauses": [
            {"clause_type": "confidentiality", "summary": "Mutual confidentiality obligations", "language": "en"},
            {"clause_type": "non_admission", "summary": "No admission of liability", "language": "en"},
            {"clause_type": "release", "summary": "Mutual release of all related claims", "language": "en"},
        ],
        "references": ["LEX-001"],
    },
    {
        "id": "LEX-006",
        "title": "BaFin Pruefbericht - Bayer AG Uebernahme Monsanto",
        "content": (
            "Die Bundesanstalt fuer Finanzdienstleistungsaufsicht (BaFin) hat die Offenlegungspflichten "
            "der Bayer AG im Zusammenhang mit der Uebernahme von Monsanto Company geprueft. Der "
            "Pruefbericht stellt fest, dass Bayer AG die Haftungsrisiken aus den Glyphosat-Klagen "
            "in den Quartalsberichten unzureichend offengelegt hat. BaFin empfiehlt erweiterte "
            "Risikoberichterstattung in kuenftigen Veroeffentlichungen gemaess der EU-Marktmissbrauchsverordnung. "
            "Monetaere Sanktionen von bis zu 2,5 Millionen Euro sind moeglich."
        ),
        "summary": "BaFin-Pruefung der Bayer AG Offenlegung zu Monsanto-Uebernahmerisiken.",
        "language": "de",
        "doc_type": "bafin_filing",
        "jurisdiction": "DE",
        "date": "2019-11-15",
        "parties": ["Bayer AG"],
        "products": [],
        "risk_factors": [
            {"name": "disclosure_deficiency", "category": "regulatory", "severity": "high"},
            {"name": "market_abuse_regulation_risk", "category": "regulatory", "severity": "medium"},
        ],
        "monetary_value": 2500000,
        "confidentiality": "restricted",
        "contract_clauses": [],
        "references": ["LEX-003"],
    },
    {
        "id": "LEX-007",
        "title": "SEC Filing - Bayer AG Risk Factor Disclosure (Form 20-F)",
        "content": (
            "Bayer AG Annual Report on Form 20-F filed with the U.S. Securities and Exchange "
            "Commission. Risk Factors section discloses: (1) Pending and future Roundup litigation "
            "with estimated exposure exceeding $10 billion; (2) Regulatory risks across multiple "
            "jurisdictions; (3) Integration risks from Monsanto acquisition; (4) Potential impact "
            "on crop science revenue if glyphosate products face bans. The company has established "
            "a $4.5 billion litigation reserve for Roundup-related claims."
        ),
        "summary": "SEC annual filing disclosing Roundup litigation reserves and cross-jurisdictional risks.",
        "language": "en",
        "doc_type": "sec_filing",
        "jurisdiction": "US",
        "date": "2020-02-28",
        "parties": ["Bayer AG", "Monsanto Company"],
        "products": ["Roundup"],
        "risk_factors": [
            {"name": "litigation_reserve_4.5B", "category": "financial", "severity": "critical"},
            {"name": "integration_risk", "category": "financial", "severity": "medium"},
            {"name": "product_ban_risk", "category": "regulatory", "severity": "high"},
        ],
        "monetary_value": 4500000000,
        "confidentiality": "public",
        "contract_clauses": [],
        "references": ["LEX-003", "LEX-004"],
    },
    {
        "id": "LEX-008",
        "title": "IARC Monograph 112 - Glyphosate Carcinogenicity Assessment",
        "content": (
            "The International Agency for Research on Cancer (IARC) Monograph 112 evaluates the "
            "carcinogenicity of glyphosate, the active ingredient in Roundup herbicide. Based on "
            "limited evidence of carcinogenicity in humans and sufficient evidence in experimental "
            "animals, glyphosate is classified as probably carcinogenic to humans (Group 2A). "
            "Mechanistic evidence includes genotoxicity and oxidative stress. This classification "
            "has significant implications for regulatory agencies and ongoing litigation worldwide."
        ),
        "summary": "IARC classification of glyphosate as Group 2A probable carcinogen.",
        "language": "en",
        "doc_type": "scientific_study",
        "jurisdiction": "INTL",
        "date": "2015-03-20",
        "parties": [],
        "products": ["Roundup"],
        "risk_factors": [
            {"name": "glyphosate_cancer_risk", "category": "environmental", "severity": "critical"},
        ],
        "monetary_value": 0,
        "confidentiality": "public",
        "contract_clauses": [],
        "references": [],
    },
    {
        "id": "LEX-009",
        "title": "Due Diligence Report - Monsanto Acquisition Environmental Liabilities",
        "content": (
            "Independent due diligence assessment of environmental liabilities associated with "
            "Monsanto Company operations. The report identifies significant exposure from: "
            "(1) Superfund sites linked to PCB contamination in Anniston, Alabama; "
            "(2) Glyphosate groundwater contamination in agricultural regions; "
            "(3) Agent Orange legacy claims from Vietnam-era operations. Total estimated "
            "environmental liability ranges from $2 billion to $8 billion depending on "
            "regulatory outcomes. Recommends enhanced environmental reserves."
        ),
        "summary": "Due diligence report on Monsanto environmental liabilities including PCB and Agent Orange.",
        "language": "en",
        "doc_type": "due_diligence_report",
        "jurisdiction": "US",
        "date": "2016-06-30",
        "parties": ["Bayer AG", "Monsanto Company"],
        "products": ["Roundup"],
        "risk_factors": [
            {"name": "environmental_contamination", "category": "environmental", "severity": "critical"},
            {"name": "superfund_liability", "category": "environmental", "severity": "high"},
            {"name": "agent_orange_legacy", "category": "litigation", "severity": "medium"},
        ],
        "monetary_value": 8000000000,
        "confidentiality": "confidential",
        "contract_clauses": [],
        "references": [],
    },
    {
        "id": "LEX-010",
        "title": "Rechtsgutachten - Grenzueberschreitende Haftung Bayer-Monsanto",
        "content": (
            "Dieses Rechtsgutachten untersucht die grenzueberschreitenden Haftungsfragen im "
            "Zusammenhang mit der Uebernahme von Monsanto durch Bayer AG. Zentrale Fragestellungen "
            "sind: (1) Durchgriffshaftung der deutschen Muttergesellschaft fuer US-Tochteransprueche; "
            "(2) Anerkennung und Vollstreckung von US-Urteilen in Deutschland; (3) Anwendbares Recht "
            "bei Produkthaftungsanspruechen mit internationalen Bezuegen. Das Gutachten empfiehlt "
            "eine Haftungsabschirmung durch gesellschaftsrechtliche Strukturierung und die Einrichtung "
            "eines Cross-Border Litigation Management Teams."
        ),
        "summary": "Rechtsgutachten zur grenzueberschreitenden Haftung bei der Bayer-Monsanto Uebernahme.",
        "language": "de",
        "doc_type": "legal_memo",
        "jurisdiction": "DE",
        "date": "2017-03-10",
        "parties": ["Bayer AG", "Monsanto Company"],
        "products": [],
        "risk_factors": [
            {"name": "piercing_corporate_veil", "category": "litigation", "severity": "high"},
            {"name": "cross_border_enforcement", "category": "regulatory", "severity": "high"},
        ],
        "monetary_value": 0,
        "confidentiality": "privileged",
        "contract_clauses": [],
        "references": ["LEX-002"],
    },
    {
        "id": "LEX-011",
        "title": "Pilliod v. Monsanto - Punitive Damages Award",
        "content": (
            "In Pilliod v. Monsanto Company, a California jury awarded $2.055 billion in damages "
            "to Alva and Alberta Pilliod, a married couple who both developed non-Hodgkin lymphoma "
            "after using Roundup for over 30 years. The award includes $55 million in compensatory "
            "damages and $2 billion in punitive damages. The jury found that Monsanto acted with "
            "malice and failed to adequately warn consumers about cancer risks associated with "
            "Roundup. This represents the largest single Roundup verdict to date."
        ),
        "summary": "Record $2B punitive damages verdict against Monsanto in Roundup cancer case.",
        "language": "en",
        "doc_type": "litigation_filing",
        "jurisdiction": "US",
        "date": "2019-05-13",
        "parties": ["Monsanto Company"],
        "products": ["Roundup"],
        "risk_factors": [
            {"name": "punitive_damages_exposure", "category": "litigation", "severity": "critical"},
            {"name": "malice_finding", "category": "litigation", "severity": "critical"},
        ],
        "monetary_value": 2055000000,
        "confidentiality": "public",
        "contract_clauses": [],
        "references": ["LEX-001", "LEX-008"],
    },
    {
        "id": "LEX-012",
        "title": "Bundeskartellamt Freigabebescheid - Bayer/Monsanto Zusammenschluss",
        "content": (
            "Das Bundeskartellamt hat den Zusammenschluss von Bayer AG und Monsanto Company unter "
            "Auflagen freigegeben. Die Freigabe ist an folgende Bedingungen geknuepft: (1) Veraeusserung "
            "des gesamten Saatgutgeschaefts von Bayer an BASF SE; (2) Lizenzierung bestimmter "
            "Pflanzenschutzmittel-Patente; (3) Einrichtung eines unabhaengigen Compliance-Monitors "
            "fuer einen Zeitraum von drei Jahren. Der Zusammenschlusswert betraegt 63 Milliarden USD. "
            "Die EU-Kommission hat parallel eine eigene Pruefung durchgefuehrt."
        ),
        "summary": "Bundeskartellamt-Freigabe der Bayer-Monsanto Fusion unter wettbewerbsrechtlichen Auflagen.",
        "language": "de",
        "doc_type": "cross_border_regulatory",
        "jurisdiction": "DE",
        "date": "2018-03-21",
        "parties": ["Bayer AG", "Monsanto Company"],
        "products": [],
        "risk_factors": [
            {"name": "divestiture_requirements", "category": "regulatory", "severity": "high"},
            {"name": "compliance_monitoring", "category": "regulatory", "severity": "medium"},
        ],
        "monetary_value": 63000000000,
        "confidentiality": "public",
        "contract_clauses": [],
        "references": ["LEX-002"],
    },
]


def generate_sample_documents():
    """Write sample LEX-*.json documents to disk."""
    SAMPLE_DOCS_DIR.mkdir(parents=True, exist_ok=True)

    for doc in SAMPLE_DOCUMENTS:
        fpath = SAMPLE_DOCS_DIR / f"{doc['id']}.json"
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)

    # Write entity aliases
    aliases = {
        "Bayer AG": ["Bayer Aktiengesellschaft", "Bayer"],
        "Monsanto Company": ["Monsanto", "Monsanto Co."],
        "Roundup": ["Roundup Ready", "Roundup Pro"],
        "Glyphosate": ["Glyphosat", "N-(phosphonomethyl)glycine"],
        "EPA": ["Environmental Protection Agency", "US-Umweltbehoerde"],
        "IARC": ["International Agency for Research on Cancer", "Internationale Agentur fuer Krebsforschung"],
        "BaFin": ["Bundesanstalt fuer Finanzdienstleistungsaufsicht"],
        "Bundeskartellamt": ["Federal Cartel Office"],
    }
    aliases_path = SAMPLE_DOCS_DIR / "_entity_aliases.json"
    with open(aliases_path, "w", encoding="utf-8") as f:
        json.dump(aliases, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(SAMPLE_DOCUMENTS)} sample documents + entity aliases in {SAMPLE_DOCS_DIR}")


def main():
    """Set up LexBridge databases."""
    print("=" * 60)
    print("LexBridge Database Setup")
    print("=" * 60)
    print()

    # Step 1: Generate sample documents
    print("[1/5] Generating sample M&A due diligence documents...")
    generate_sample_documents()
    print()

    # Step 2: Load Harrier embedder
    print("[2/5] Loading Harrier embedding model...")
    from src.embeddings.harrier_embedder import HarrierEmbedder
    embedder = HarrierEmbedder()
    print()

    # Step 3: Initialize vector store
    print("[3/5] Initializing Qdrant vector store...")
    from src.storage.vector_store import VectorStore
    vector_store = VectorStore()
    print(f"      Vector store ready at {vector_store.path}")
    print()

    # Step 4: Initialize graph store
    print("[4/5] Initializing FalkorDB graph store...")
    from src.storage.graph_store import GraphStore
    graph_store = GraphStore()
    print(f"      Graph store ready.")
    print()

    # Step 5: Ingest documents
    print("[5/5] Ingesting documents into vector + graph stores...")
    from src.agents.ingestion_agent import ingest_documents
    ingest_documents(embedder, vector_store, graph_store)
    print()

    # Print stats
    print("=" * 60)
    print("LexBridge Database Setup Complete!")
    print("=" * 60)
    print(f"  Vectors:       {vector_store.count()}")
    print(f"  Graph Nodes:   {graph_store.node_count()}")
    print(f"  Relationships: {graph_store.relationship_count()}")
    print()
    print("Next steps:")
    print("  1. (Optional) Start LLM: llama-server -hf ggml-org/gemma-4-E2B-it-GGUF:Q4_K_M")
    print("  2. Run CLI:      python main.py")
    print("  3. Run UI:       streamlit run src/ui/app.py")


if __name__ == "__main__":
    main()
