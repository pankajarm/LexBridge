#!/usr/bin/env python3
"""LexBridge CLI entry point.

Cross-Lingual M&A Due Diligence Intelligence System.

Usage:
    python main.py
    python main.py --query "Find all Roundup product liability filings"
"""

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(
        description="LexBridge: Cross-Lingual M&A Due Diligence Intelligence"
    )
    parser.add_argument(
        "--query", "-q",
        type=str,
        default=None,
        help="Query to process (interactive mode if omitted)",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("LexBridge")
    print("Cross-Lingual M&A Due Diligence Intelligence")
    print("=" * 60)
    print()

    # Initialize components
    print("Loading components...")
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
    print("All components loaded.\n")

    def process_query(query: str):
        """Process a single query through the LexBridge workflow."""
        print(f"Query: {query}")
        print("-" * 40)

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

        # Display results
        print(f"\nClassified as: {result.get('query_type', 'unknown')}")
        print(f"Search results: {len(result.get('search_results', []))}")
        print(f"Graph results: {len(result.get('graph_results', []))}")

        if result.get("risk_report"):
            report = result["risk_report"]
            print(f"Risk report type: {report.get('type', 'none')}")

        print(f"\n{'=' * 40}")
        print("RESPONSE:")
        print("=" * 40)
        print(result.get("final_response", "No response generated."))

        # Show agent trace
        print(f"\n{'=' * 40}")
        print("AGENT TRACE:")
        print("=" * 40)
        for entry in result.get("agent_trace", []):
            print(f"  [{entry.get('agent', '?')}] {entry.get('action', '?')}")

        return result

    if args.query:
        process_query(args.query)
    else:
        # Interactive mode
        print("Enter queries (type 'quit' to exit):")
        print("Example: Find all Roundup product liability filings\n")

        while True:
            try:
                query = input("LexBridge> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break

            if not query:
                continue
            if query.lower() in ("quit", "exit", "q"):
                print("Goodbye!")
                break

            try:
                process_query(query)
            except Exception as e:
                print(f"Error: {e}")
            print()


if __name__ == "__main__":
    main()
