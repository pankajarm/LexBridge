"""LexBridge configuration."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"

# Model settings
HARRIER_MODEL_NAME = os.getenv("HARRIER_MODEL_NAME", "microsoft/harrier-oss-v1-0.6b")

# Database paths
QDRANT_PATH = os.getenv("QDRANT_PATH", str(DATA_DIR / "qdrant"))
FALKORDB_PATH = os.getenv("FALKORDB_PATH", str(DATA_DIR / "falkordb"))

# LLM settings (connects to llama-server OpenAI-compatible API)
LLM_API_BASE = os.getenv("LLM_API_BASE", "http://localhost:8080/v1")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gemma-4")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))

# Embedding settings
EMBEDDING_DEVICE = os.getenv("EMBEDDING_DEVICE", "mps")
EMBEDDING_BATCH_SIZE = int(os.getenv("EMBEDDING_BATCH_SIZE", "32"))
EMBEDDING_DIM = 1024

# Qdrant collection
QDRANT_COLLECTION = "legal_documents"

# Legal task prompts for Harrier
HARRIER_PROMPTS = {
    "document_search": "Given a legal due diligence query, retrieve relevant M&A documents and filings",
    "document_similarity": "Identify semantically similar legal documents across jurisdictions",
    "entity_matching": "Match legal entity names that refer to the same company, product, or regulatory body across languages",
    "risk_assessment": "Find documents disclosing litigation risks, regulatory risks, or financial exposure",
    "clause_comparison": "Retrieve contract clauses related to indemnification, liability, or risk allocation",
}

# Supported languages
SUPPORTED_LANGUAGES = ["en", "de"]
