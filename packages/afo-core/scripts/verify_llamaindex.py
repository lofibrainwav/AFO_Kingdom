#!/usr/bin/env python3
"""
TICKET-030 Verification: LlamaIndex Multimodal RAG
===================================================
Verifies all LlamaIndex modules are correctly installed and importable.
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def verify_dependencies():
    """Verify LlamaIndex dependencies are installed."""
    print("=== Phase A: Dependency Verification ===")

    deps = [
        ("llama_index.core", "llama-index"),
        ("llama_index.llms.ollama", "llama-index-llms-ollama"),
        ("llama_index.embeddings.ollama", "llama-index-embeddings-ollama"),
        ("llama_index.vector_stores.chroma", "llama-index-vector-stores-chroma"),
        ("chromadb", "chromadb"),
    ]

    all_ok = True
    for module, package in deps:
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError as e:
            print(f"  ❌ {package}: {e}")
            all_ok = False

    return all_ok


def verify_modules():
    """Verify AFO RAG modules are importable."""
    print("\n=== Phase B-E: Module Verification ===")

    modules = [
        ("afo.rag.llamaindex_rag", "Core RAG"),
        ("afo.rag.llamaindex_vision", "Vision"),
        ("afo.rag.llamaindex_hybrid", "Hybrid Search"),
        ("afo.rag.llamaindex_reranker", "Reranker"),
        ("afo.rag.llamaindex_eval", "Evaluation"),
        ("afo.rag", "Package __init__"),
    ]

    all_ok = True
    for module, name in modules:
        try:
            __import__(module)
            print(f"  ✅ {name} ({module})")
        except ImportError as e:
            print(f"  ❌ {name}: {e}")
            all_ok = False

    return all_ok


def verify_ollama_connection():
    """Verify Ollama connection."""
    print("\n=== Ollama Connection Test ===")

    import os

    import httpx

    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    try:
        response = httpx.get(f"{base_url}/api/tags", timeout=5.0)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"  ✅ Ollama connected at {base_url}")
            print(f"  📦 Models available: {len(models)}")
            for m in models[:3]:
                print(f"      - {m['name']}")
            return True
    except Exception as e:
        print(f"  ⚠️ Ollama not available: {e}")
        return False


def verify_settings():
    """Verify LlamaIndex settings configuration."""
    print("\n=== Settings Configuration Test ===")

    try:
        from afo.rag.llamaindex_rag import configure_settings

        configure_settings()

        from llama_index.core import Settings

        print(f"  ✅ LLM: {Settings.llm}")
        print(f"  ✅ Embed: {Settings.embed_model}")
        return True
    except Exception as e:
        print(f"  ❌ Settings config failed: {e}")
        return False


def main():
    """Run all verifications."""
    print("=" * 60)
    print("TICKET-030: LlamaIndex Multimodal RAG Verification")
    print("=" * 60)

    results = {
        "Dependencies": verify_dependencies(),
        "Modules": verify_modules(),
        "Ollama": verify_ollama_connection(),
        "Settings": verify_settings(),
    }

    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)

    all_pass = True
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {name}: {status}")
        if not passed:
            all_pass = False

    print("\n" + "=" * 60)
    if all_pass:
        print("🎉 ALL VERIFICATIONS PASSED - Trinity Score +10 Expected!")
    else:
        print("⚠️ Some verifications failed - review above")
    print("=" * 60)

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
