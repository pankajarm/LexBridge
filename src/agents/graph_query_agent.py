"""Graph query agent: NL-to-Cypher with legal-domain helpers."""

from src.agents.state import LexBridgeState


def _entity_lookup_query(state: LexBridgeState, graph_store, llm) -> list[dict]:
    """Handle entity_lookup queries by extracting entity name and querying the graph."""
    query = state["query"]

    # Extract entity name from the query using LLM
    entities = llm.extract_entities(query)
    companies = entities.get("companies", [])
    products = entities.get("products", [])

    results = []

    # Try company subgraph first
    for company in companies:
        subgraph = graph_store.get_company_subgraph(company)
        if subgraph:
            results.extend(subgraph)

    # Then try product claims
    for product in products:
        claims = graph_store.get_product_claims(product)
        if claims:
            results.extend(claims)

    # Fallback: try well-known entities from the query text
    if not results:
        q_lower = query.lower()
        if any(w in q_lower for w in ["roundup", "glyphosate", "glyphosat"]):
            results = graph_store.get_product_claims("Roundup")
        if any(w in q_lower for w in ["monsanto"]):
            results.extend(graph_store.get_company_subgraph("Monsanto Company"))
        if any(w in q_lower for w in ["bayer"]):
            results.extend(graph_store.get_company_subgraph("Bayer AG"))

    return results


def _risk_exposure_query(state: LexBridgeState, graph_store) -> list[dict]:
    """Handle risk_assessment queries by aggregating claims and risk factors."""
    results = []

    # Query claims filed against Monsanto
    claims = graph_store.get_litigation_exposure("Monsanto Company")
    if claims:
        total_exposure = sum(c.get("value", 0) for c in claims if c.get("value"))
        results.append({
            "type": "litigation_exposure",
            "company": "Monsanto Company",
            "total_claims": len(claims),
            "total_monetary_exposure": total_exposure,
            "claims": claims,
        })

    # Aggregate risk factors
    risk_factors = graph_store.get_risk_factors_by_category()
    if risk_factors:
        results.append({
            "type": "risk_factors",
            "factors": risk_factors,
        })

    return results


def graph_query_node(state: LexBridgeState, graph_store, llm) -> dict:
    """Execute graph queries based on query type."""
    query_type = state.get("query_type", "document_search")

    if query_type == "entity_lookup":
        results = _entity_lookup_query(state, graph_store, llm)
    elif query_type in ("risk_assessment", "gap_analysis"):
        results = _risk_exposure_query(state, graph_store)
    else:
        # Generate Cypher from natural language using LLM
        schema = graph_store.get_schema()
        cypher = llm.generate_cypher(state["query"], schema)
        try:
            results = graph_store.query(cypher)
        except Exception as e:
            results = [{"error": str(e), "cypher": cypher}]

    trace_entry = {
        "agent": "graph_query",
        "action": f"query_{query_type}",
        "query": state["query"],
        "num_results": len(results),
    }

    return {
        "graph_results": results,
        "agent_trace": state.get("agent_trace", []) + [trace_entry],
    }
