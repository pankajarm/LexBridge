"""Risk analysis agent: jurisdiction-aware risk assessment, clause comparison, and gap analysis."""

from src.agents.state import LexBridgeState

# Expected document type categories for M&A due diligence gap analysis
EXPECTED_DOC_TYPES = [
    "litigation_filing",
    "regulatory_correspondence",
    "risk_assessment",
    "settlement_agreement",
    "insurance_policy",
    "indemnification_clause",
    "sec_filing",
    "scientific_study",
    "board_minutes",
    "due_diligence_report",
    "bafin_filing",
    "legal_memo",
    "integration_plan",
    "shareholder_communication",
    "merger_agreement",
    "cross_border_regulatory",
]


def _risk_assessment_mode(state: LexBridgeState, llm) -> dict:
    """Analyze litigation exposure grouped by jurisdiction."""
    search_results = state.get("search_results", [])
    graph_results = state.get("graph_results", [])

    # Group search results by jurisdiction
    by_jurisdiction = {}
    for doc in search_results:
        jur = doc.get("jurisdiction", "unknown")
        by_jurisdiction.setdefault(jur, []).append(doc)

    # Compute total monetary exposure from graph results
    total_exposure = 0.0
    claims = []
    for item in graph_results:
        if isinstance(item, dict) and item.get("type") == "litigation_exposure":
            total_exposure = item.get("total_monetary_exposure", 0)
            claims = item.get("claims", [])
            break

    # Build context for LLM analysis
    context_parts = []
    for jur, docs in by_jurisdiction.items():
        doc_summaries = "; ".join(
            d.get("summary", d.get("title", ""))[:200] for d in docs[:5]
        )
        context_parts.append(f"Jurisdiction {jur} ({len(docs)} docs): {doc_summaries}")

    context = "\n".join(context_parts)
    prompt = (
        f"Analyze the following M&A due diligence risk data.\n"
        f"Total litigation exposure: ${total_exposure:,.0f}\n"
        f"Number of claims: {len(claims)}\n\n"
        f"Documents by jurisdiction:\n{context}\n\n"
        f"Provide a risk assessment covering: litigation risk, regulatory risk, "
        f"financial exposure, and cross-jurisdictional concerns."
    )

    analysis = llm.generate(prompt)

    return {
        "type": "risk_assessment",
        "jurisdictions": {
            jur: {"doc_count": len(docs), "top_docs": [d.get("title", "") for d in docs[:3]]}
            for jur, docs in by_jurisdiction.items()
        },
        "total_monetary_exposure": total_exposure,
        "total_claims": len(claims),
        "claims": claims[:10],
        "analysis": analysis,
    }


def _clause_comparison_mode(state: LexBridgeState, embedder) -> dict:
    """Compare contract clauses using embedding similarity matrix."""
    search_results = state.get("search_results", [])

    # Take top 6 results for pairwise comparison
    top_docs = search_results[:6]
    if not top_docs:
        return {"type": "clause_comparison", "labels": [], "similarity_matrix": [], "analysis": "No clauses found."}

    # Embed the content of each document
    texts = [doc.get("content", doc.get("summary", doc.get("title", "")))[:1000] for doc in top_docs]
    labels = [doc.get("title", doc.get("doc_id", f"doc_{i}"))[:60] for i, doc in enumerate(top_docs)]
    embeddings = embedder.embed_documents(texts)

    # Compute pairwise similarity matrix
    import numpy as np
    emb_array = np.array(embeddings)
    similarity_matrix = (emb_array @ emb_array.T).tolist()

    return {
        "type": "clause_comparison",
        "labels": labels,
        "similarity_matrix": similarity_matrix,
        "num_clauses": len(top_docs),
    }


def _gap_analysis_mode(state: LexBridgeState, llm) -> dict:
    """Identify gaps in due diligence document coverage."""
    search_results = state.get("search_results", [])

    # Check doc_type coverage against expected categories
    found_types = {doc.get("doc_type", "") for doc in search_results}
    found_types.discard("")

    missing_types = [dt for dt in EXPECTED_DOC_TYPES if dt not in found_types]
    coverage_pct = (
        (len(EXPECTED_DOC_TYPES) - len(missing_types)) / len(EXPECTED_DOC_TYPES) * 100
        if EXPECTED_DOC_TYPES
        else 0
    )

    # LLM analysis of gaps
    prompt = (
        f"M&A due diligence gap analysis:\n"
        f"Coverage: {coverage_pct:.1f}% ({len(EXPECTED_DOC_TYPES) - len(missing_types)}/{len(EXPECTED_DOC_TYPES)} categories)\n"
        f"Found document types: {sorted(found_types)}\n"
        f"Missing document types: {missing_types}\n\n"
        f"Analyze the significance of the missing document types for M&A due diligence. "
        f"Which gaps pose the highest risk? What should be prioritized?"
    )

    analysis = llm.generate(prompt)

    return {
        "type": "gap_analysis",
        "expected_types": EXPECTED_DOC_TYPES,
        "found_types": sorted(found_types),
        "missing_types": missing_types,
        "coverage_pct": round(coverage_pct, 1),
        "analysis": analysis,
    }


def _general_synthesis_mode(state: LexBridgeState, llm) -> dict:
    """General synthesis of search and graph results."""
    search_results = state.get("search_results", [])
    graph_results = state.get("graph_results", [])

    context_parts = []
    for doc in search_results[:5]:
        context_parts.append(
            f"- {doc.get('title', 'Untitled')} [{doc.get('language', '?')}]: "
            f"{doc.get('summary', '')[:200]}"
        )
    for item in graph_results[:5]:
        context_parts.append(f"- Graph: {item}")

    context = "\n".join(context_parts)
    prompt = f"Synthesize the following M&A due diligence findings:\n\n{context}"
    analysis = llm.generate(prompt)

    return {
        "type": "general",
        "analysis": analysis,
    }


def risk_analysis_node(state: LexBridgeState, embedder, llm) -> dict:
    """Run risk analysis based on query type."""
    query_type = state.get("query_type", "document_search")

    if query_type == "risk_assessment":
        report = _risk_assessment_mode(state, llm)
    elif query_type == "clause_comparison":
        report = _clause_comparison_mode(state, embedder)
    elif query_type == "gap_analysis":
        report = _gap_analysis_mode(state, llm)
    else:
        report = _general_synthesis_mode(state, llm)

    trace_entry = {
        "agent": "risk_analysis",
        "action": f"analyze_{query_type}",
        "report_type": report.get("type", "unknown"),
    }

    return {
        "risk_report": report,
        "agent_trace": state.get("agent_trace", []) + [trace_entry],
    }
