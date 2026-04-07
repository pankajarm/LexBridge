"""Initialize databases and ingest sample data."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.generate_sample_documents import main as generate_documents
from src.embeddings.harrier_embedder import HarrierEmbedder
from src.storage.vector_store import VectorStore
from src.storage.graph_store import GraphStore
from src.agents.ingestion_agent import ingest_documents


def main():
    print("=" * 60)
    print("LexBridge Database Setup")
    print("=" * 60)

    # Step 1: Generate sample data
    print("\n[1/3] Generating sample document data...")
    generate_documents()

    # Step 2: Load embedder first to know the embedding dim
    print("\n[2/3] Loading embedding model...")
    embedder = HarrierEmbedder()

    # Initialize stores with correct dim
    print("Initializing databases...")
    vector_store = VectorStore(embedding_dim=embedder.dim)
    graph_store = GraphStore()
    print(f"  Qdrant: {vector_store.count()} vectors")
    print(f"  FalkorDB: {graph_store.node_count()} nodes")

    # Step 3: Ingest documents
    print("\n[3/3] Ingesting documents...")
    stats = ingest_documents(embedder, vector_store, graph_store)

    print("\n" + "=" * 60)
    print("Setup complete!")
    print(f"  Documents ingested: {stats.get('documents_ingested', 0)}")
    print(f"  Vectors in Qdrant: {stats.get('vectors_count', 0)}")
    print(f"  Nodes in graph: {stats.get('graph_nodes', 0)}")
    print(f"  Relationships in graph: {stats.get('graph_relationships', 0)}")
    print("\nRun: uv run streamlit run src/ui/app.py")


if __name__ == "__main__":
    main()
