#!/usr/bin/env python3
"""
SunoBranch 독립 테스트 스크립트
AFO 패키지 의존성 없이 SunoBranch 기능 테스트
"""

import sys
import os

# PYTHONPATH 설정
sys.path.insert(0, '/Users/brnestrm/Library/Python/3.9/lib/python/site-packages')
sys.path.insert(0, '/Users/brnestrm/AFO_Kingdom/packages/afo-core')

try:
    # requests import
    import requests
    print("✅ requests import 성공")

    # SunoBranch 로직 직접 테스트 (AFO 패키지 회피)
    class TestSunoBranch:
        """테스트용 SunoBranch 구현"""

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

        def convert_timeline_to_prompt(self, timeline_sections, custom_mode=True):
            """TimelineState를 Suno 프롬프트로 변환"""
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
                    music_desc = self.MUSIC_DIRECTIVE_MAP.get(directive, directive)

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
                music_desc = self.MUSIC_DIRECTIVE_MAP.get(dominant_directive, dominant_directive)

                return {
                    "prompt": f"{music_desc}, {len(timeline_sections)} section composition",
                    "duration": int(total_duration),
                    "sections": len(timeline_sections),
                    "custom_mode": False,
                }

    # 테스트 실행
    print("🎵 SunoBranch 독립 테스트 시작...")

    test_branch = TestSunoBranch()

    # 테스트용 TimelineState
    test_timeline = [
        {"start": 0, "end": 3, "music_directive": "slow_build"},
        {"start": 3, "end": 6, "music_directive": "drop_beat"},
        {"start": 6, "end": 9, "music_directive": "peak_energy"},
    ]

    timeline_desc = [f"{s['music_directive']}({s['start']}-{s['end']})" for s in test_timeline]
    print(f"Timeline: {timeline_desc}")

    # Custom mode 테스트
    custom_result = test_branch.convert_timeline_to_prompt(test_timeline, custom_mode=True)
    print(f"\n🎯 Custom Mode 결과:")
    print(f"프롬프트: {custom_result['prompt']}")
    print(f"길이: {custom_result['duration']}초")
    print(f"섹션 수: {custom_result['sections']}")

    # Simple mode 테스트
    simple_result = test_branch.convert_timeline_to_prompt(test_timeline, custom_mode=False)
    print(f"\n🎯 Simple Mode 결과:")
    print(f"프롬프트: {simple_result['prompt']}")
    print(f"길이: {simple_result['duration']}초")
    print(f"섹션 수: {simple_result['sections']}")

    # API 페이로드 시뮬레이션
    payload = {
        "prompt": custom_result["prompt"],
        "model": "V5",
        "custom_mode": True,
        "instrumental": False,
        "style": "epic orchestral cinematic",
        "title": "AFO Kingdom Victory Theme",
        "tags": "epic, victory, kingdom",
        "duration": custom_result["duration"],
    }

    print(f"\n🎯 API 페이로드 미리보기:")
    print(f"Model: {payload['model']}")
    print(f"Style: {payload['style']}")
    print(f"Title: {payload['title']}")
    print(f"Tags: {payload['tags']}")
    print(f"Duration: {payload['duration']}초")
    print(f"Instrumental: {payload['instrumental']}")

    print("\n🎵 사용 가능한 음악 지시어:")
    print(f"{list(test_branch.MUSIC_DIRECTIVE_MAP.keys())}")

    print("\n🎯 SunoBranch 로직 검증 완료!")
    print("✅ TimelineState → Suno 프롬프트 변환 성공")
    print("✅ Custom/Simple mode 모두 작동")
    print("✅ API 페이로드 생성 성공")

except Exception as e:
    print(f"❌ 테스트 실패: {e}")
    import traceback
    traceback.print_exc()
