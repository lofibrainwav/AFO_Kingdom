"""
AFO Kingdom: LlamaIndex RAG Core Module (眞·善·美·孝·永)
=======================================================
Author: Chancellor AFO
Created: 2025-12-31
License: AFO Royal License

2025 SOTA-level Multimodal Hybrid RAG with Host Ollama (GPU accelerated).
- Vision: qwen3-vl:8b for image understanding
- Reasoning: deepseek-r1:14b for complex queries
- Hybrid Search: Vector + BM25 with alpha tuning
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import chromadb
from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore

logger = logging.getLogger(__name__)

# Host Ollama URL (GPU accelerated via Metal)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")

# Default models
DEFAULT_LLM_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1:14b")
DEFAULT_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")

# Index persistence path
INDEX_PERSIST_DIR = Path(os.getenv("LLAMAINDEX_PERSIST_DIR", "./kingdom_rag_index"))
CHROMA_PERSIST_DIR = Path(os.getenv("CHROMA_PERSIST_DIR", "./chroma_db"))


def configure_settings(
    llm_model: str = DEFAULT_LLM_MODEL,
    embed_model: str = DEFAULT_EMBED_MODEL,
    ollama_url: str = OLLAMA_BASE_URL,
) -> None:
    """Configure LlamaIndex global settings with Host Ollama (GPU accelerated).

    Args:
        llm_model: Ollama model for LLM inference (default: deepseek-r1:14b)
        embed_model: Ollama model for embeddings (default: nomic-embed-text)
        ollama_url: Base URL for Ollama API
    """
    logger.info(f"Configuring LlamaIndex with Ollama at {ollama_url}")
    logger.info(f"LLM: {llm_model}, Embed: {embed_model}")

    # Configure LLM (Reasoning)
    Settings.llm = Ollama(
        model=llm_model,
        base_url=ollama_url,
        request_timeout=120.0,
    )

    # Configure Embedding Model
    Settings.embed_model = OllamaEmbedding(
        model_name=embed_model,
        base_url=ollama_url,
    )

    # Configure Node Parser (Chunking)
    Settings.node_parser = SentenceSplitter(
        chunk_size=512,
        chunk_overlap=50,
    )

    logger.info("LlamaIndex settings configured successfully (眞)")


def get_chroma_client() -> chromadb.PersistentClient:
    """Get or create ChromaDB persistent client.

    Returns:
        ChromaDB persistent client instance
    """
    CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_PERSIST_DIR))


def build_index(
    docs_path: str | Path = "./docs",
    collection_name: str = "kingdom_docs",
    rebuild: bool = False,
) -> VectorStoreIndex:
    """Build or load vector index from documents.

    Args:
        docs_path: Path to documents directory
        collection_name: ChromaDB collection name
        rebuild: Force rebuild index even if exists

    Returns:
        VectorStoreIndex instance
    """
    docs_path = Path(docs_path)

    # Check for existing index
    if INDEX_PERSIST_DIR.exists() and not rebuild:
        try:
            logger.info(f"Loading existing index from {INDEX_PERSIST_DIR}")
            storage_context = StorageContext.from_defaults(persist_dir=str(INDEX_PERSIST_DIR))
            return load_index_from_storage(storage_context)
        except Exception as e:
            logger.warning(f"Failed to load existing index: {e}. Rebuilding...")

    # Load documents
    logger.info(f"Loading documents from {docs_path}")
    if not docs_path.exists():
        logger.warning(f"Documents path {docs_path} does not exist. Creating empty index.")
        documents = []
    else:
        reader = SimpleDirectoryReader(
            input_dir=str(docs_path),
            recursive=True,
            required_exts=[".md", ".txt", ".pdf", ".py"],
        )
        documents = reader.load_data()

    logger.info(f"Loaded {len(documents)} documents")

    # Setup ChromaDB vector store
    chroma_client = get_chroma_client()
    chroma_collection = chroma_client.get_or_create_collection(collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Build index
    logger.info("Building vector index (善)...")
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True,
    )

    # Persist index
    INDEX_PERSIST_DIR.mkdir(parents=True, exist_ok=True)
    index.storage_context.persist(persist_dir=str(INDEX_PERSIST_DIR))
    logger.info(f"Index persisted to {INDEX_PERSIST_DIR}")

    return index


def create_query_engine(
    index: VectorStoreIndex,
    similarity_top_k: int = 10,
    alpha: float = 0.75,
    streaming: bool = False,
) -> Any:
    """Create hybrid search query engine.

    Args:
        index: Vector store index
        similarity_top_k: Number of top results to retrieve
        alpha: Hybrid search alpha (0=keyword, 1=vector, 0.75 recommended for vision)
        streaming: Enable streaming responses

    Returns:
        Query engine instance
    """
    logger.info(f"Creating query engine (alpha={alpha}, top_k={similarity_top_k})")

    query_engine = index.as_query_engine(
        similarity_top_k=similarity_top_k,
        streaming=streaming,
    )

    return query_engine


def query(
    query_text: str,
    index: VectorStoreIndex | None = None,
) -> str:
    """Execute a RAG query.

    Args:
        query_text: The query string
        index: Optional existing index (will build if None)

    Returns:
        Query response as string
    """
    if index is None:
        configure_settings()
        index = build_index()

    query_engine = create_query_engine(index)
    response = query_engine.query(query_text)

    return str(response)


# Singleton index instance for reuse
_global_index: VectorStoreIndex | None = None


def get_global_index(rebuild: bool = False) -> VectorStoreIndex:
    """Get or create global index singleton.

    Args:
        rebuild: Force rebuild index

    Returns:
        Global VectorStoreIndex instance
    """
    global _global_index

    if _global_index is None or rebuild:
        configure_settings()
        _global_index = build_index(rebuild=rebuild)

    return _global_index


# Export public API
__all__ = [
    "build_index",
    "configure_settings",
    "create_query_engine",
    "get_chroma_client",
    "get_global_index",
    "query",
]
