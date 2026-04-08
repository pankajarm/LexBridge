"""LexBridge Streamlit UI.

Cross-Lingual M&A Due Diligence Intelligence System.

Usage:
    streamlit run src/ui/app.py
"""

import sys
from pathlib import Path

# Ensure project root is on sys.path for imports
_root = str(Path(__file__).parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

import streamlit as st
import pandas as pd


# --- Page config ---
st.set_page_config(
    page_title="LexBridge",
    page_icon="\u2696\ufe0f",
    layout="wide",
)


# --- Cached initialization ---
@st.cache_resource
def load_components():
    """Load all LexBridge components (cached across sessions)."""
    from src.embeddings.harrier_embedder import HarrierEmbedder
    from src.storage.vector_store import VectorStore
    from src.storage.graph_store import GraphStore
    from src.llm.gemma_llm import GemmaLLM
    from src.graph.workflow import build_workflow

    embedder = HarrierEmbedder()
    vector_store = VectorStore()
    graph_store = GraphStore()
    llm = GemmaLLM()
    workflow = build_workflow(embedder, vector_store, graph_store, llm)

    return embedder, vector_store, graph_store, llm, workflow


embedder, vector_store, graph_store, llm, workflow = load_components()


# --- Sidebar ---
with st.sidebar:
    st.title("\u2696\ufe0f LexBridge")
    st.caption("Cross-Lingual M&A Due Diligence Intelligence")
    st.divider()

    st.subheader("Suggested Queries")
    suggested_queries = [
        "Find all Roundup product liability filings",
        "Zeige mir alle Dokumente ueber Produkthaftungsrisiken",
        "What is the total litigation exposure from glyphosate claims?",
        "Compare indemnification clauses across merger documents",
        "What due diligence gaps exist in the Bayer-Monsanto review?",
        "Show all entities connected to Roundup",
    ]
    for sq in suggested_queries:
        if st.button(sq, key=f"sq_{hash(sq)}", use_container_width=True):
            st.session_state["active_query"] = sq

    st.divider()
    st.subheader("Tech Stack")
    st.markdown("""
    - **Embeddings**: Harrier-OSS-v1-0.6B
    - **LLM**: Gemma 4 (llama-server)
    - **Vector DB**: Qdrant (embedded)
    - **Graph DB**: FalkorDB (embedded)
    - **Orchestration**: LangGraph
    - **Languages**: English, German
    """)


# --- Tabs ---
tab1, tab2, tab3 = st.tabs([
    "Document Search & Analysis",
    "Entity Relationship Graph",
    "Risk Dashboard",
])


# ============================================================
# Tab 1: Document Search & Analysis
# ============================================================
with tab1:
    st.header("Document Search & Analysis")

    # Query input
    default_query = st.session_state.get("active_query", "")
    query = st.text_input(
        "Ask about M&A documents in any language...",
        value=default_query,
        placeholder="e.g., Zeige mir alle Dokumente ueber Produkthaftungsrisiken",
    )

    if query:
        with st.spinner("Processing query across languages..."):
            initial_state = {
                "messages": [],
                "query": query,
                "query_type": "document_search",
                "search_results": [],
                "graph_results": [],
                "risk_report": {},
                "agent_trace": [],
                "final_response": "",
            }
            result = workflow.invoke(initial_state)

        # Display response
        st.subheader("Analysis")
        st.markdown(result.get("final_response", "No response generated."))

        # Result cards
        search_results = result.get("search_results", [])
        if search_results:
            st.subheader(f"Retrieved Documents ({len(search_results)})")
            for doc in search_results:
                lang = doc.get("language", "?")
                flag = {"en": "\U0001f1fa\U0001f1f8", "de": "\U0001f1e9\U0001f1ea"}.get(lang, "\U0001f310")
                title = doc.get("title", "Untitled")
                score = doc.get("score", 0)
                doc_type = doc.get("doc_type", "unknown")
                jurisdiction = doc.get("jurisdiction", "?")
                summary = doc.get("summary", "")
                risk_factors = doc.get("risk_factors", [])
                monetary = doc.get("monetary_value", 0)

                with st.container(border=True):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"### {flag} {title}")
                        st.caption(f"Similarity: {score:.3f} | {doc_type} | {jurisdiction}")
                        st.write(summary)
                        if risk_factors:
                            rf_tags = " ".join(
                                f"`{rf}`" if isinstance(rf, str) else f"`{rf}`"
                                for rf in risk_factors
                            )
                            st.markdown(f"Risk factors: {rf_tags}")
                    with col2:
                        if monetary and monetary > 0:
                            st.metric("Monetary Value", f"${monetary:,.0f}")

        # Risk report rendering
        risk_report = result.get("risk_report", {})
        if risk_report:
            report_type = risk_report.get("type", "")
            st.subheader("Risk Report")

            if report_type == "risk_assessment":
                st.markdown(risk_report.get("analysis", ""))
                exposure = risk_report.get("total_monetary_exposure", 0)
                if exposure:
                    st.metric("Total Monetary Exposure", f"${exposure:,.0f}")
                claims = risk_report.get("claims", [])
                if claims:
                    st.dataframe(pd.DataFrame(claims), use_container_width=True)

            elif report_type == "clause_comparison":
                labels = risk_report.get("labels", [])
                matrix = risk_report.get("similarity_matrix", [])
                if labels and matrix:
                    import plotly.express as px
                    fig = px.imshow(
                        matrix,
                        x=labels, y=labels,
                        color_continuous_scale="RdYlGn",
                        title="Clause Similarity Heatmap",
                        aspect="auto",
                    )
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)

            elif report_type == "gap_analysis":
                coverage = risk_report.get("coverage_pct", 0)
                missing = risk_report.get("missing_types", [])
                st.metric("Coverage", f"{coverage:.1f}%")
                st.markdown(risk_report.get("analysis", ""))
                if missing:
                    st.warning(f"Missing document types: {', '.join(missing)}")

        # Agent trace
        agent_trace = result.get("agent_trace", [])
        if agent_trace:
            with st.expander("Agent Trace", expanded=False):
                agent_icons = {
                    "supervisor": "\U0001f9d1\u200d\u2696\ufe0f",
                    "semantic_search": "\U0001f50d",
                    "graph_query": "\U0001f578\ufe0f",
                    "risk_analysis": "\u26a0\ufe0f",
                    "synthesizer": "\U0001f4dd",
                }
                for entry in agent_trace:
                    agent = entry.get("agent", "unknown")
                    icon = agent_icons.get(agent, "\u2699\ufe0f")
                    action = entry.get("action", "")
                    st.markdown(f"{icon} **{agent}**: {action}")
                    detail_keys = [k for k in entry if k not in ("agent", "action")]
                    if detail_keys:
                        details = {k: entry[k] for k in detail_keys}
                        st.json(details)


# ============================================================
# Tab 2: Entity Relationship Graph
# ============================================================
with tab2:
    st.header("Entity Relationship Graph")

    try:
        from streamlit_agraph import agraph, Node, Edge, Config

        nodes_list = []
        edges_list = []
        seen_nodes = set()

        color_map = {
            "Company": "#4169E1",
            "Product": "#2E8B57",
            "LegalClaim": "#DC143C",
            "RegulatoryBody": "#FF8C00",
            "Chemical": "#8B008B",
            "RiskFactor": "#8B0000",
            "Document": "#808080",
        }

        # Query relationships
        queries = [
            ("MATCH (a:Company)-[r:ACQUIRED]->(b:Company) RETURN a.name AS src, 'Company' AS src_type, 'ACQUIRED' AS rel, b.name AS tgt, 'Company' AS tgt_type", None),
            ("MATCH (c:Company)-[r:MANUFACTURES]->(p:Product) RETURN c.name AS src, 'Company' AS src_type, 'MANUFACTURES' AS rel, p.name AS tgt, 'Product' AS tgt_type", None),
            ("MATCH (p:Product)-[r:CONTAINS_CHEMICAL]->(ch:Chemical) RETURN p.name AS src, 'Product' AS src_type, 'CONTAINS_CHEMICAL' AS rel, ch.name AS tgt, 'Chemical' AS tgt_type", None),
            ("MATCH (l:LegalClaim)-[r:FILED_AGAINST]->(c:Company) RETURN l.case_name AS src, 'LegalClaim' AS src_type, 'FILED_AGAINST' AS rel, c.name AS tgt, 'Company' AS tgt_type", None),
            ("MATCH (l:LegalClaim)-[r:TARGETS]->(p:Product) RETURN l.case_name AS src, 'LegalClaim' AS src_type, 'TARGETS' AS rel, p.name AS tgt, 'Product' AS tgt_type", None),
            ("MATCH (r:RegulatoryBody)-[i:INVESTIGATES]->(p:Product) RETURN r.name AS src, 'RegulatoryBody' AS src_type, 'INVESTIGATES' AS rel, p.name AS tgt, 'Product' AS tgt_type", None),
        ]

        for cypher, _ in queries:
            try:
                results = graph_store.query(cypher)
                for row in results:
                    src = str(row.get("src", ""))
                    tgt = str(row.get("tgt", ""))
                    src_type = row.get("src_type", "Document")
                    tgt_type = row.get("tgt_type", "Document")
                    rel = row.get("rel", "RELATED")

                    if src and src not in seen_nodes:
                        nodes_list.append(Node(
                            id=src, label=src[:30],
                            size=25, color=color_map.get(src_type, "#808080"),
                        ))
                        seen_nodes.add(src)
                    if tgt and tgt not in seen_nodes:
                        nodes_list.append(Node(
                            id=tgt, label=tgt[:30],
                            size=25, color=color_map.get(tgt_type, "#808080"),
                        ))
                        seen_nodes.add(tgt)
                    if src and tgt:
                        edges_list.append(Edge(source=src, target=tgt, label=rel))
            except Exception:
                pass

        if nodes_list:
            config = Config(
                width=900, height=600, directed=True,
                physics=True, hierarchical=False,
                nodeHighlightBehavior=True,
                highlightColor="#F7A7A6",
            )
            agraph(nodes=nodes_list, edges=edges_list, config=config)

            # Legend
            st.markdown("**Legend:**")
            legend_cols = st.columns(len(color_map))
            for col, (label, color) in zip(legend_cols, color_map.items()):
                col.markdown(
                    f'<span style="color:{color}; font-weight:bold;">\u25cf</span> {label}',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No graph data available. Run `python scripts/setup_databases.py` first.")

    except ImportError:
        st.warning(
            "Install streamlit-agraph for interactive graph visualization:\n\n"
            "`pip install streamlit-agraph`"
        )


# ============================================================
# Tab 3: Risk Dashboard
# ============================================================
with tab3:
    st.header("Risk Dashboard")

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Documents", vector_store.count())
    with col2:
        st.metric("Graph Nodes", graph_store.node_count())
    with col3:
        st.metric("Relationships", graph_store.relationship_count())
    with col4:
        st.metric("Languages", 2)

    st.divider()

    # Documents by language
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Documents by Language")
        try:
            lang_data = graph_store.query(
                "MATCH (d:Document) RETURN d.language AS language, count(d) AS count ORDER BY count DESC"
            )
            if lang_data:
                df_lang = pd.DataFrame(lang_data)
                st.bar_chart(df_lang.set_index("language"))
            else:
                st.info("No document data available.")
        except Exception:
            st.info("No document data available.")

    with col_right:
        st.subheader("Documents by Type")
        try:
            type_data = graph_store.query(
                "MATCH (d:Document) RETURN d.doc_type AS doc_type, count(d) AS count ORDER BY count DESC"
            )
            if type_data:
                df_type = pd.DataFrame(type_data)
                st.bar_chart(df_type.set_index("doc_type"))
            else:
                st.info("No document data available.")
        except Exception:
            st.info("No document data available.")

    st.divider()

    # Risk factors table
    st.subheader("Risk Factors")
    try:
        risk_data = graph_store.get_risk_factors_by_category()
        if risk_data:
            df_risk = pd.DataFrame(risk_data)
            st.dataframe(df_risk, use_container_width=True, hide_index=True)
        else:
            st.info("No risk factor data available.")
    except Exception:
        st.info("No risk factor data available.")

    st.divider()

    # Litigation exposure
    st.subheader("Litigation Exposure")
    try:
        claims_data = graph_store.get_litigation_exposure("Monsanto Company")
        if claims_data:
            df_claims = pd.DataFrame(claims_data)
            if "value" in df_claims.columns and "claim" in df_claims.columns:
                import plotly.express as px
                fig = px.bar(
                    df_claims, x="value", y="claim",
                    orientation="h",
                    title="Claims by Monetary Value",
                    labels={"value": "Monetary Value ($)", "claim": "Claim"},
                )
                fig.update_layout(height=400, yaxis={"categoryorder": "total ascending"})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.dataframe(df_claims, use_container_width=True, hide_index=True)
        else:
            st.info("No litigation data available.")
    except Exception:
        st.info("No litigation data available.")

    st.divider()

    # Cross-lingual document similarities
    st.subheader("Cross-Lingual Document Similarities")
    try:
        sim_data = graph_store.query(
            "MATCH (d1:Document)-[s:SIMILAR_TO {cross_lingual: true}]->(d2:Document) "
            "RETURN d1.title AS doc_1, d2.title AS doc_2, d1.language AS lang_1, "
            "d2.language AS lang_2, s.score AS similarity "
            "ORDER BY s.score DESC LIMIT 20"
        )
        if sim_data:
            df_sim = pd.DataFrame(sim_data)
            st.dataframe(df_sim, use_container_width=True, hide_index=True)
        else:
            st.info("No cross-lingual similarity data available. Run setup_databases.py first.")
    except Exception:
        st.info("No cross-lingual similarity data available.")
