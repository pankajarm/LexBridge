"""Qdrant embedded vector store for legal document embeddings."""

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from src.config import QDRANT_PATH, QDRANT_COLLECTION, EMBEDDING_DIM


class VectorStore:
    """Qdrant embedded vector store — no server needed."""

    def __init__(self, path: str | None = None, embedding_dim: int = EMBEDDING_DIM):
        self.path = path or QDRANT_PATH
        self.embedding_dim = embedding_dim
        self.client = QdrantClient(path=self.path)
        self._ensure_collection()

    def _ensure_collection(self):
        collections = [c.name for c in self.client.get_collections().collections]
        if QDRANT_COLLECTION not in collections:
            self.client.create_collection(
                collection_name=QDRANT_COLLECTION,
                vectors_config=VectorParams(size=self.embedding_dim, distance=Distance.COSINE),
            )

    def upsert(self, doc_id: str, vector: list[float], metadata: dict):
        """Insert or update a document embedding with metadata."""
        point = PointStruct(
            id=hash(doc_id) % (2**63),
            vector=vector,
            payload={"doc_id": doc_id, **metadata},
        )
        self.client.upsert(collection_name=QDRANT_COLLECTION, points=[point])

    def upsert_batch(self, items: list[dict]):
        """Batch insert: each item has 'id', 'vector', 'metadata'."""
        points = [
            PointStruct(
                id=hash(item["id"]) % (2**63),
                vector=item["vector"],
                payload={"doc_id": item["id"], **item["metadata"]},
            )
            for item in items
        ]
        self.client.upsert(collection_name=QDRANT_COLLECTION, points=points)

    def search(
        self,
        query_vector: list[float],
        limit: int = 10,
        language: str | None = None,
        doc_type: str | None = None,
        jurisdiction: str | None = None,
        product: str | None = None,
    ) -> list[dict]:
        """Search for similar documents with optional metadata filters."""
        conditions = []
        if language:
            conditions.append(FieldCondition(key="language", match=MatchValue(value=language)))
        if doc_type:
            conditions.append(FieldCondition(key="doc_type", match=MatchValue(value=doc_type)))
        if jurisdiction:
            conditions.append(FieldCondition(key="jurisdiction", match=MatchValue(value=jurisdiction)))
        if product:
            conditions.append(FieldCondition(key="products", match=MatchValue(value=product)))

        query_filter = Filter(must=conditions) if conditions else None

        results = self.client.query_points(
            collection_name=QDRANT_COLLECTION,
            query=query_vector,
            query_filter=query_filter,
            limit=limit,
        )
        return [
            {
                "score": hit.score,
                "doc_id": hit.payload.get("doc_id"),
                **hit.payload,
            }
            for hit in results.points
        ]

    def count(self) -> int:
        """Get total number of vectors in the collection."""
        info = self.client.get_collection(QDRANT_COLLECTION)
        return info.points_count

    def delete_collection(self):
        """Delete the collection (for reset)."""
        self.client.delete_collection(QDRANT_COLLECTION)
