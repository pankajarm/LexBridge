#!/usr/bin/env python3
"""Download and cache models required by LexBridge.

Downloads:
1. Harrier-OSS-v1-0.6B multilingual embeddings (sentence-transformers)
2. Gemma 4 LLM via llama-server (instructions printed)

Usage:
    python scripts/download_models.py
"""

import sys


def download_harrier():
    """Download and cache the Harrier embedding model."""
    print("=" * 60)
    print("LexBridge Model Download")
    print("=" * 60)
    print()
    print("[1/2] Downloading Harrier-OSS-v1-0.6B embeddings...")
    print("      This is a ~1.2 GB download (first time only).")
    print()

    try:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(
            "microsoft/harrier-oss-v1-0.6b",
            device="cpu",  # CPU for download; runtime uses MPS/CUDA
            model_kwargs={"torch_dtype": "auto"},
        )

        # Verify with a quick test
        test_emb = model.encode("test", normalize_embeddings=True)
        assert len(test_emb) == 1024, f"Expected dim=1024, got {len(test_emb)}"

        print(f"      Harrier model cached successfully (dim={len(test_emb)}).")
        print()
    except Exception as e:
        print(f"      ERROR downloading Harrier: {e}")
        print("      Make sure you have: pip install sentence-transformers>=4.1")
        print("      Also requires: transformers>=4.51 (for Qwen3 architecture)")
        sys.exit(1)

    print("[2/2] Gemma 4 LLM (via llama-server)")
    print("      LexBridge uses llama-server for the LLM backend.")
    print("      Install and run with:")
    print()
    print("        brew install llama.cpp")
    print("        llama-server -hf ggml-org/gemma-4-E2B-it-GGUF:Q4_K_M")
    print()
    print("      The model (~5 GB) will be downloaded on first run.")
    print("      LexBridge works without it (mock responses), but")
    print("      full LLM analysis requires the server running.")
    print()
    print("=" * 60)
    print("LexBridge model setup complete!")
    print("=" * 60)


if __name__ == "__main__":
    download_harrier()
