"""
SunoBranch - Suno AI 음악 생성 통합
TimelineState 기반 프로그래머틱 음악 생성으로 TikTok급 AV 콘텐츠 자동 완성

API 엔드포인트: 비공식 Suno API (sunoapi.org, gcui-art/suno-api 등)
고급 매개변수: custom_mode, style, title, tags, duration 지원
에러 처리: 재시도 + Graceful Fallback + 비용 최적화
"""

import logging
import time
from typing import Any, Optional

import requests

logger = logging.getLogger(__name__)

# Suno API 엔드포인트 (비공식 - 2026년 기준)
SUNO_API_BASE = "https://api.sunoapi.org/api/v1"

# 음악 지시어 → Suno 프롬프트 매핑
MUSIC_DIRECTIVE_MAP = {
    "slow_build": "slow atmospheric pads, low energy, slow tempo, ambient intro, cinematic build",
    "drop_beat": "heavy drop beat, high energy, fast tempo, 808 bass and synth lead, trap elements",
    "peak_energy": "epic orchestral climax, peak energy, full instruments riser, emotional peak",
    "emotional_piano": "emotional piano melody, soft strings, slow tempo, heartfelt, cinematic",
    "tiktok_trend": "trendy pop beat, upbeat tempo, catchy melody, viral potential, modern production",
    "dance_challenge": "high energy dance beat, fast tempo, motivational, pump up, EDM elements",
    "story_time": "soft acoustic guitar, storytelling melody, warm atmosphere, narrative feel",
    "victory_theme": "triumphant orchestral, rising strings, powerful brass, victory celebration",
}


class SunoBranch:
    """
    Suno AI 음악 생성 브랜치
    TimelineState를 음악 프롬프트로 변환하여 자동 음악 생성
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or self._load_api_key()
        self.session = requests.Session()
        self.session.headers.update(
            {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        )

    def _load_api_key(self) -> str:
        """환경 변수에서 Suno API 키 로드"""
        import os

        api_key = os.getenv("SUNO_API_KEY")
        if not api_key:
            raise ValueError("SUNO_API_KEY 환경 변수가 설정되지 않음")
        return api_key

    def generate_music_from_timeline(
        self,
        timeline_sections,
        custom_mode: bool = True,
        style: str = "epic orchestral cinematic",
        title: str = "AFO Kingdom Theme",
        tags: str = "epic, cinematic, kingdom",
        max_retries: int = 3,
        dry_run: bool = True,
    ):
        """
        TimelineState를 Suno 음악으로 변환

        Args:
            timeline_sections: TimelineState sections
            custom_mode: 고급 모드 사용 여부
            style: 음악 스타일
            title: 곡 제목
            tags: 태그
            max_retries: 최대 재시도 횟수
            dry_run: 실제 생성 없이 계획만 반환

        Returns:
            음악 생성 결과
        """
        try:
            # TimelineState → Suno 프롬프트 변환
            prompt_data = self._convert_timeline_to_prompt(timeline_sections, custom_mode)

            # 고급 매개변수 적용
            if custom_mode:
                payload = {
                    "prompt": prompt_data["prompt"],
                    "model": "V5",  # 최신 모델
                    "custom_mode": True,
                    "instrumental": False,
                    "style": style,
                    "title": title,
                    "tags": tags,
                    "duration": prompt_data["duration"],
                }
            else:
                payload = {
                    "prompt": prompt_data["prompt"],
                    "model": "V4_5ALL",
                    "instrumental": False,
                    "duration": prompt_data["duration"],
                }

            if dry_run:
                return {
                    "success": True,
                    "mode": "dry_run",
                    "prompt_data": prompt_data,
                    "payload": payload,
                    "estimated_cost": "~$0.08",
                    "timeline_sections": len(timeline_sections),
                }

            # 실제 API 호출 (에러 처리 포함)
            result = self._call_suno_api_safe(payload, max_retries)

            return {
                "success": result["success"],
                "mode": "wet_run",
                "audio_url": result.get("audio_url"),
                "song_id": result.get("song_id"),
                "title": result.get("title", title),
                "duration": result.get("duration"),
                "model": result.get("model", "V5"),
                "error": result.get("error"),
                "timeline_sections": len(timeline_sections),
                "cost": "~$0.08",
            }

        except Exception as e:
            logger.error(f"Suno 음악 생성 실패: {e}")
            return {
                "success": False,
                "error": str(e),
                "mode": "error",
                "timeline_sections": len(timeline_sections),
            }

    def _convert_timeline_to_prompt(self, timeline_sections, custom_mode: bool = True):
        """
        TimelineState를 Suno 프롬프트로 변환

        Args:
            timeline_sections: TimelineState sections
            custom_mode: 고급 모드 여부

        Returns:
            프롬프트 데이터
        """
        total_duration = sum(
            section.get("end", 0) - section.get("start", 0) for section in timeline_sections
        )

        if custom_mode:
            # 고급 모드: 세부 시간별 프롬프트
            prompt_parts = []
            for section in timeline_sections:
                start_time = section.get("start", 0)
                end_time = section.get("end", start_time + 3)
                directive = section.get("music_directive", "slow_build")
                music_desc = MUSIC_DIRECTIVE_MAP.get(directive, directive)

                prompt_parts.append(f"[{start_time}-{end_time}] {music_desc}")

            full_prompt = " | ".join(prompt_parts) or "epic orchestral kingdom theme"

            return {
                "prompt": full_prompt,
                "duration": int(total_duration),
                "sections": len(timeline_sections),
                "custom_mode": True,
            }
        else:
            # 단순 모드: 통합 프롬프트
            directives = [
                section.get("music_directive", "slow_build") for section in timeline_sections
            ]
            dominant_directive = max(set(directives), key=directives.count)
            music_desc = MUSIC_DIRECTIVE_MAP.get(dominant_directive, dominant_directive)

            return {
                "prompt": f"{music_desc}, {len(timeline_sections)} section composition",
                "duration": int(total_duration),
                "sections": len(timeline_sections),
                "custom_mode": False,
            }

    def _call_suno_api_safe(self, payload, max_retries: int = 3):
        """
        Suno API 안전 호출 (에러 처리 + 재시도)

        Args:
            payload: API 페이로드
            max_retries: 최대 재시도 횟수

        Returns:
            API 응답 데이터
        """
        for attempt in range(max_retries):
            try:
                response = self.session.post(f"{SUNO_API_BASE}/generate", json=payload, timeout=60)

                # HTTP 에러 처리
                response.raise_for_status()

                data = response.json()

                # API 에러 코드 처리
                if data.get("code") == 200:
                    return {
                        "success": True,
                        "audio_url": data.get("audio_url"),
                        "song_id": data.get("song_id"),
                        "title": data.get("title"),
                        "duration": data.get("duration"),
                        "model": data.get("model"),
                    }
                elif data.get("code") == 400:
                    return {
                        "success": False,
                        "error": "콘텐츠 위반 또는 잘못된 프롬프트",
                        "details": data.get("message", "Unknown 400 error"),
                    }
                elif data.get("code") in (401, 403):
                    return {
                        "success": False,
                        "error": "API 키 인증 실패",
                        "details": "키 재발급 또는 로그인 필요",
                    }
                elif data.get("code") == 429:
                    if attempt < max_retries - 1:
                        wait_time = 10 * (2**attempt)  # Exponential backoff
                        logger.warning(f"Rate limit 초과, {wait_time}초 대기")
                        time.sleep(wait_time)
                        continue
                    else:
                        return {
                            "success": False,
                            "error": "Rate limit 초과 및 최대 재시도 실패",
                        }
                elif data.get("code") >= 500:
                    if attempt < max_retries - 1:
                        logger.warning(f"서버 오류 {data.get('code')}, 재시도 {attempt + 1}")
                        time.sleep(5)
                        continue
                    else:
                        return {
                            "success": False,
                            "error": "서버 오류 및 최대 재시도 실패",
                        }
                else:
                    return {
                        "success": False,
                        "error": f"알 수 없는 API 에러: {data.get('code')}",
                        "details": data.get("message", "Unknown error"),
                    }

            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    logger.warning(f"타임아웃, 재시도 {attempt + 1}")
                    continue
                else:
                    return {
                        "success": False,
                        "error": "타임아웃 및 최대 재시도 실패",
                    }

            except requests.exceptions.RequestException as e:
                return {
                    "success": False,
                    "error": f"네트워크 오류: {e!s}",
                }

        return {
            "success": False,
            "error": "최대 재시도 횟수 초과",
        }

    def get_available_music_directives(self):
        """
        사용 가능한 음악 지시어 목록 반환

        Returns:
            지시어 이름 리스트
        """
        return list(MUSIC_DIRECTIVE_MAP.keys())


# 글로벌 SunoBranch 인스턴스
_suno_branch = None


def get_suno_branch(api_key: str | None = None):
    """
    SunoBranch 싱글톤 인스턴스 반환

    Args:
        api_key: Suno API 키 (옵션)

    Returns:
        SunoBranch 인스턴스
    """
    global _suno_branch
    if _suno_branch is None:
        _suno_branch = SunoBranch(api_key)
    return _suno_branch


def suno_generate_music(
    timeline,
    custom_mode: bool = True,
    style: str = "epic orchestral cinematic",
    title: str = "AFO Kingdom Theme",
    tags: str = "epic, cinematic, kingdom",
    dry_run: bool = True,
):
    """
    Suno 음악 생성 편의 함수

    Args:
        timeline: TimelineState sections
        custom_mode: 고급 모드 사용
        style: 음악 스타일
        title: 곡 제목
        tags: 태그
        dry_run: 실제 생성 없이 계획만

    Returns:
        음악 생성 결과
    """
    suno = get_suno_branch()
    return suno.generate_music_from_timeline(
        timeline, custom_mode, style, title, tags, dry_run=dry_run
    )


if __name__ == "__main__":
    # 테스트용 TimelineState
    test_timeline = [
        {"start": 0, "end": 3, "music_directive": "slow_build"},
        {"start": 3, "end": 6, "music_directive": "drop_beat"},
        {"start": 6, "end": 9, "music_directive": "peak_energy"},
    ]

    # Dry run 테스트
    result = suno_generate_music(
        test_timeline,
        custom_mode=True,
        style="epic orchestral cinematic",
        title="AFO Kingdom Victory Theme",
        tags="epic, victory, kingdom",
        dry_run=True,
    )

    print("🎵 Suno 음악 생성 테스트 결과:")
    print(f"성공: {result.get('success', False)}")
    print(f"모드: {result.get('mode', 'unknown')}")
    print(f"섹션 수: {result.get('timeline_sections', 0)}")
    if result.get("success") and result.get("mode") == "dry_run":
        prompt_data = result.get("prompt_data", {})
        print(f"프롬프트: {prompt_data.get('prompt', 'N/A')}")
        print(f"예상 길이: {prompt_data.get('duration', 0)}초")
        print(f"예상 비용: {result.get('estimated_cost', 'N/A')}")
    elif result.get("mode") == "wet_run":
        print(f"음악 URL: {result.get('audio_url', 'N/A')}")
        print(f"곡 제목: {result.get('title', 'N/A')}")
        print("🎯 AFO 왕국의 음악 브랜치 탄생!")
    else:
        print(f"오류: {result.get('error', '알 수 없는 오류')}")

    print(f"\n사용 가능한 음악 지시어: {get_suno_branch().get_available_music_directives()}")
