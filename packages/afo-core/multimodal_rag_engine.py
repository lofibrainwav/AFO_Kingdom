"""
Multimodal RAG Engine for AFO Kingdom (Phase 2)
Handles multimodal content (images, audio, video) in RAG pipelines.
"""
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
from pathlib import Path
import base64
import json

@dataclass
class MultimodalDocument:
    """A document that can contain text, images, or other media."""
    content: str
    content_type: str = "text"  # text, image, audio, video
    metadata: Dict[str, Any] = None
    embedding: Optional[List[float]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class MultimodalRAGEngine:
    """
    Multimodal RAG Engine supporting text, images, and other media.
    """
    
    def __init__(self, embedding_model: str = "default"):
        self.embedding_model = embedding_model
        self.documents: List[MultimodalDocument] = []
        self.supported_types = ["text", "image", "audio", "video"]
    
    def add_document(self, content: str, content_type: str = "text", 
                     metadata: Dict[str, Any] = None) -> None:
        """Add a document to the RAG index."""
        doc = MultimodalDocument(
            content=content,
            content_type=content_type,
            metadata=metadata or {}
        )
        self.documents.append(doc)
    
    def add_image(self, image_path: str, description: str = "") -> None:
        """Add an image document."""
        self.add_document(
            content=description or f"Image: {image_path}",
            content_type="image",
            metadata={"path": image_path}
        )
    
    def search(self, query: str, top_k: int = 5, 
               content_types: List[str] = None) -> List[MultimodalDocument]:
        """
        Search for relevant documents.
        
        Args:
            query: Search query
            top_k: Number of results to return
            content_types: Filter by content types (None = all)
            
        Returns:
            List of matching documents
        """
        # Filter by content type if specified
        candidates = self.documents
        if content_types:
            candidates = [d for d in candidates if d.content_type in content_types]
        
        # Simple keyword matching (would use embeddings in production)
        query_lower = query.lower()
        scored = []
        for doc in candidates:
            score = sum(1 for word in query_lower.split() if word in doc.content.lower())
            if score > 0:
                scored.append((score, doc))
        
        # Sort by score and return top_k
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:top_k]]
    
    def retrieve_with_context(self, query: str, context: Dict[str, Any] = None,
                              top_k: int = 5) -> Dict[str, Any]:
        """
        Retrieve documents with context awareness.
        
        Returns:
            Dict containing results and metadata
        """
        results = self.search(query, top_k)
        return {
            "query": query,
            "results": results,
            "count": len(results),
            "context_used": context is not None
        }
    
    def process_image(self, image_path: str) -> Dict[str, Any]:
        """Process an image for RAG indexing."""
        path = Path(image_path)
        if not path.exists():
            return {"error": f"Image not found: {image_path}"}
        
        return {
            "path": str(path),
            "name": path.name,
            "size": path.stat().st_size,
            "type": path.suffix,
            "indexed": True
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics."""
        type_counts = {}
        for doc in self.documents:
            type_counts[doc.content_type] = type_counts.get(doc.content_type, 0) + 1
        
        return {
            "total_documents": len(self.documents),
            "by_type": type_counts,
            "embedding_model": self.embedding_model
        }

# Default instance
multimodal_rag_engine = MultimodalRAGEngine()

def get_multimodal_engine() -> MultimodalRAGEngine:
    """Get the default multimodal RAG engine."""
    return multimodal_rag_engine
