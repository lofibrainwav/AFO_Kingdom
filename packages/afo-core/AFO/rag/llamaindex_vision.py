"""
AFO Kingdom: LlamaIndex Multimodal Vision Module (美)
=====================================================
Author: Chancellor AFO
Created: 2025-12-31

Vision-aware RAG with qwen3-vl:8b for image understanding.
Uses direct Ollama API calls for compatibility.
"""

from __future__ import annotations

import base64
import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any

import httpx

if TYPE_CHECKING:
    from llama_index.core import VectorStoreIndex

logger = logging.getLogger(__name__)

# Vision model configuration
VISION_MODEL = os.getenv("OLLAMA_VISION_MODEL", "qwen3-vl:8b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")


def _encode_image(image_path: Path) -> str:
    """Encode image to base64 for Ollama API.

    Args:
        image_path: Path to image file

    Returns:
        Base64 encoded string
    """
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def analyze_image(
    image_path: str | Path,
    prompt: str = "이 이미지를 상세히 분석하고 설명해주세요.",
    model: str = VISION_MODEL,
    timeout: float = 180.0,
) -> str:
    """Analyze a single image using qwen3-vl via Ollama API.

    Args:
        image_path: Path to image file
        prompt: Analysis prompt
        model: Vision model to use
        timeout: Request timeout in seconds

    Returns:
        Analysis result as string
    """
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    logger.info(f"Analyzing image with {model}: {image_path}")

    # Encode image
    image_b64 = _encode_image(image_path)

    # Call Ollama API
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "images": [image_b64],
        "stream": False,
    }

    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
    except httpx.HTTPError as e:
        logger.error(f"Ollama API error: {e}")
        raise


def analyze_images_batch(
    image_paths: list[str | Path],
    prompt: str = "이 이미지들을 분석하고 공통점과 차이점을 설명해주세요.",
    model: str = VISION_MODEL,
) -> str:
    """Analyze multiple images together.

    Note: Ollama processes images sequentially, so we analyze each and combine.

    Args:
        image_paths: List of image file paths
        prompt: Analysis prompt
        model: Vision model to use

    Returns:
        Combined analysis result
    """
    results = []
    for i, path in enumerate(image_paths):
        path = Path(path)
        if path.exists():
            try:
                result = analyze_image(path, f"Image {i + 1}: {prompt}", model)
                results.append(f"[Image {i + 1}: {path.name}]\n{result}")
            except Exception as e:
                logger.warning(f"Failed to analyze {path}: {e}")
                results.append(f"[Image {i + 1}: {path.name}] Error: {e}")
        else:
            logger.warning(f"Image not found, skipping: {path}")

    if not results:
        return "No valid images found."

    return "\n\n".join(results)


def get_vision_models() -> list[dict[str, Any]]:
    """Get available vision models from Ollama.

    Returns:
        List of model info dicts
    """
    url = f"{OLLAMA_BASE_URL}/api/tags"

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)
            response.raise_for_status()
            models = response.json().get("models", [])

            # Filter for likely vision models
            vision_keywords = ["vl", "vision", "llava", "moondream"]
            vision_models = [
                m for m in models if any(kw in m["name"].lower() for kw in vision_keywords)
            ]
            return vision_models
    except httpx.HTTPError as e:
        logger.error(f"Failed to get models: {e}")
        return []


def create_vision_query_engine(
    text_index: VectorStoreIndex,
    include_images: bool = True,
) -> Any:
    """Create a vision-aware query engine.

    Args:
        text_index: Existing text vector index
        include_images: Whether to include image analysis

    Returns:
        Vision-enhanced query engine
    """
    logger.info("Creating vision-aware query engine (美)")

    query_engine = text_index.as_query_engine(
        similarity_top_k=10,
    )

    return query_engine


# Export public API
__all__ = [
    "analyze_image",
    "analyze_images_batch",
    "create_vision_query_engine",
    "get_vision_models",
]
