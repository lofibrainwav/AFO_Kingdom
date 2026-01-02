# Trinity Score: 92.0 (Multimodal Integration)
"""
Multimodal Router for AFO Kingdom
Exposes Vision, Audio, and Video RAG services via REST API.

2025 Best Practice: Unified multimodal endpoint with graceful degradation.
"""

import logging
import tempfile
from pathlib import Path
from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/multimodal", tags=["Multimodal"])


@router.get("/status")
async def get_multimodal_status() -> dict[str, Any]:
    """Get status of all multimodal services."""
    status = {
        "vision": {"available": False, "model": None},
        "audio": {"available": False, "model": None},
        "video": {"available": False, "dependencies": []},
    }

    # Check Vision Service
    try:
        from services.vision_service import get_vision_service

        vision = get_vision_service()
        status["vision"] = {
            "available": vision._ollama_available,
            "model": vision.model if vision._ollama_available else None,
        }
    except Exception as e:
        logger.warning(f"Vision service not available: {e}")

    # Check Audio Service
    try:
        from services.audio_service import get_audio_service

        audio = get_audio_service()
        status["audio"] = {
            "available": audio._whisper_available,
            "model": audio.model_name if audio._whisper_available else None,
        }
    except Exception as e:
        logger.warning(f"Audio service not available: {e}")

    # Check Video Service
    try:
        from services.video_rag_service import get_video_rag_service

        video = get_video_rag_service()
        status["video"] = {
            "available": video._ffmpeg_available,
            "dependencies": ["ffmpeg", "vision", "audio"],
        }
    except Exception as e:
        logger.warning(f"Video service not available: {e}")

    return status


@router.post("/vision/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    prompt: str = Form(default="Describe this image in detail."),
    language: str = Form(default="en"),
) -> dict[str, Any]:
    """
    Analyze an image using Vision AI (qwen3-vl).

    Args:
        file: Image file (jpg, png, webp)
        prompt: Analysis prompt
        language: Response language (en, ko)
    """
    try:
        from services.vision_service import get_vision_service

        vision = get_vision_service()

        if not vision._ollama_available:
            raise HTTPException(status_code=503, detail="Vision service not available")

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            result = vision.analyze_image(tmp_path, prompt=prompt, language=language)
            return result
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Vision analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/audio/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str | None = Form(default=None),
    task: str = Form(default="transcribe"),
) -> dict[str, Any]:
    """
    Transcribe audio using Whisper.

    Args:
        file: Audio file (mp3, wav, m4a)
        language: Source language (auto-detect if None)
        task: "transcribe" or "translate" (to English)
    """
    try:
        from services.audio_service import get_audio_service

        audio = get_audio_service()

        if not audio._whisper_available:
            raise HTTPException(status_code=503, detail="Whisper not available")

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            result = audio.transcribe(tmp_path, language=language, task=task)
            return result
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Audio transcription failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/video/process")
async def process_video(
    file: UploadFile = File(...),
    num_frames: int = Form(default=5),
    transcribe: bool = Form(default=True),
    language: str = Form(default="ko"),
) -> dict[str, Any]:
    """
    Process video with keyframe extraction and audio transcription.

    Args:
        file: Video file (mp4, mov, avi)
        num_frames: Number of keyframes to extract
        transcribe: Whether to transcribe audio
        language: Response language for descriptions
    """
    try:
        from services.video_rag_service import get_video_rag_service

        video = get_video_rag_service()

        if not video._ffmpeg_available:
            raise HTTPException(status_code=503, detail="ffmpeg not available")

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            result = video.process_video(
                tmp_path,
                num_frames=num_frames,
                transcribe=transcribe,
                language=language,
            )
            return result
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Video processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
