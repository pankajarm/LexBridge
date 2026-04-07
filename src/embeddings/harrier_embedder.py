"""Harrier-OSS-v1-0.6B embedding wrapper with MPS support and legal task prompts."""

import torch
from sentence_transformers import SentenceTransformer

from src.config import HARRIER_MODEL_NAME, EMBEDDING_DEVICE, EMBEDDING_BATCH_SIZE, HARRIER_PROMPTS


class HarrierEmbedder:
    """Wrapper for Microsoft Harrier-OSS-v1-0.6B multilingual embeddings.

    Requires transformers>=4.51 for Qwen3 architecture support.
    Uses last-token pooling with L2 normalization (handled by sentence-transformers).
    """

    def __init__(
        self,
        model_name: str = HARRIER_MODEL_NAME,
        device: str | None = None,
    ):
        self.device = device or self._detect_device()
        print(f"Loading Harrier model on {self.device}...")
        self.model = SentenceTransformer(
            model_name,
            device=self.device,
            model_kwargs={"torch_dtype": "auto"},
        )
        self.dim = 1024
        print(f"Harrier model loaded: {model_name} (dim={self.dim})")

    def _detect_device(self) -> str:
        if EMBEDDING_DEVICE == "mps" and hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"
        if torch.cuda.is_available():
            return "cuda"
        return "cpu"

    def embed_query(self, query: str, task: str = "document_search") -> list[float]:
        """Embed a query with task-specific instruction prompt.

        Per Harrier spec, queries require an instruction prefix for best performance.
        Documents do not.
        """
        prompt = HARRIER_PROMPTS.get(task, HARRIER_PROMPTS["document_search"])
        instruction = f"Instruct: {prompt}\nQuery: "
        embedding = self.model.encode(
            query, prompt=instruction, normalize_embeddings=True, show_progress_bar=False,
        )
        return embedding.tolist()

    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        """Embed documents (no instruction prefix needed per Harrier spec)."""
        embeddings = self.model.encode(
            documents, normalize_embeddings=True,
            batch_size=EMBEDDING_BATCH_SIZE, show_progress_bar=len(documents) > 10,
        )
        return embeddings.tolist()

    def embed_entity(self, entity_name: str) -> list[float]:
        """Embed an entity name for cross-lingual entity resolution."""
        return self.embed_query(entity_name, task="entity_matching")

    def similarity(self, text1: str, text2: str) -> float:
        """Compute cosine similarity between two texts."""
        emb1 = self.model.encode(text1, normalize_embeddings=True)
        emb2 = self.model.encode(text2, normalize_embeddings=True)
        return float(emb1 @ emb2)
