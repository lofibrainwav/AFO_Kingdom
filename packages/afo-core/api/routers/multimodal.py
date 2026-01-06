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
                tmp_path, num_frames=num_frames, transcribe=transcribe, language=language
            )
            return result
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Video processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/music/generate")
async def generate_music(request: dict[str, Any]) -> dict[str, Any]:
    """
    Generate music from TimelineState using MLX MusicGen.

    Args:
        request: Request containing timeline_state and generation parameters
    """
    try:
        timeline_state = request.get("timeline_state")
        if not timeline_state:
            raise HTTPException(status_code=400, detail="timeline_state is required")

        provider = request.get("provider", "mlx_musicgen")
        quality = request.get("quality", "high")

        # Import MLX MusicGen provider
        try:
            from AFO.multimodal.music_provider import get_music_router

            router = get_music_router()
            result = router.generate_music(
                timeline_state, quality=quality, local_only=True, max_cost=0.0
            )

            if result.get("success"):
                # Return audio file URL for frontend access
                audio_path = result.get("output_path", result.get("audio_path"))
                if audio_path:
                    # Convert to web-accessible URL
                    audio_url = f"/api/audio/{Path(audio_path).name}"
                    return {
                        "success": True,
                        "audio_path": audio_path,
                        "audio_url": audio_url,
                        "duration": result.get("duration", 30),
                        "title": timeline_state.get("title", "Generated Music"),
                        "provider": provider,
                    }

            return {
                "success": False,
                "error": result.get("error", "Music generation failed"),
                "details": result,
            }

        except ImportError:
            raise HTTPException(status_code=503, detail="Music generation service not available")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Music generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Music generation failed: {e!s}")


@router.get("/audio/{filename}")
async def get_audio_file(filename: str) -> Any:
    """
    Serve generated audio files.

    Args:
        filename: Audio file name
    """
    from fastapi.responses import FileResponse

    audio_path = Path("artifacts") / filename
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(path=audio_path, media_type="audio/wav", filename=filename)


@router.post("/av/join")
async def join_audio_video(request: dict[str, Any]) -> dict[str, Any]:
    """
    Join audio and video files to create complete AV content.

    Args:
        request: Request containing video_path, audio_path, and output options
    """
    try:
        video_path = request.get("video_path")
        audio_path = request.get("audio_path")
        output_path = request.get(
            "output_path", f"artifacts/av_join_{int(__import__('time').time())}.mp4"
        )
        duration_match = request.get("duration_match", "min")
        timeline_state = request.get("timeline_state")

        if not video_path or not audio_path:
            raise HTTPException(status_code=400, detail="video_path and audio_path are required")

        # AV Join Engine 사용
        try:
            from AFO.multimodal.av_join_engine import get_av_join_engine

            engine = get_av_join_engine()

            if timeline_state:
                # TimelineState 기반 AV 생성
                result = engine.join_with_timeline_state(
                    timeline_state, video_path, audio_path, output_path
                )
            else:
                # 기본 AV JOIN
                result = engine.join_audio_video(
                    video_path, audio_path, output_path, duration_match=duration_match
                )

            if result.get("success"):
                # 웹 접근 가능한 URL로 변환
                output_filename = Path(output_path).name
                result["av_url"] = f"/api/av/{output_filename}"

            return result

        except ImportError:
            raise HTTPException(status_code=503, detail="AV Join engine not available")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AV join failed: {e}")
        raise HTTPException(status_code=500, detail=f"AV join failed: {e!s}")


@router.post("/av/create-complete")
async def create_complete_av(request: dict[str, Any]) -> dict[str, Any]:
    """
    Create complete AV from TimelineState (auto-generate video + audio + join).

    Args:
        request: Request containing timeline_state and options
    """
    try:
        timeline_state = request.get("timeline_state")
        if not timeline_state:
            raise HTTPException(status_code=400, detail="timeline_state is required")

        # 미래: CapCut + MusicGen 자동 통합
        # 현재는 수동 파일 기반 (테스트용)
        video_path = request.get("video_path", "artifacts/sample_video.mp4")
        audio_path = request.get("audio_path", "artifacts/mlx_music_test.wav")
        output_path = request.get(
            "output_path", f"artifacts/complete_av_{int(__import__('time').time())}.mp4"
        )

        try:
            from AFO.multimodal.av_join_engine import get_av_join_engine

            engine = get_av_join_engine()
            result = engine.create_complete_av_from_timeline(
                timeline_state, video_path, audio_path, output_path
            )

            if result.get("success"):
                output_filename = Path(output_path).name
                result["av_url"] = f"/api/av/{output_filename}"

            return result

        except ImportError:
            raise HTTPException(status_code=503, detail="AV creation engine not available")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Complete AV creation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Complete AV creation failed: {e!s}")


@router.get("/av/{filename}")
async def get_av_file(filename: str) -> Any:
    """
    Serve generated AV files.

    Args:
        filename: AV file name
    """
    from fastapi.responses import FileResponse

    av_path = Path("artifacts") / filename
    if not av_path.exists():
        raise HTTPException(status_code=404, detail="AV file not found")

    return FileResponse(path=av_path, media_type="video/mp4", filename=filename)
