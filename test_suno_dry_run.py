#!/usr/bin/env python3
"""
SunoBranch DRY_RUN Reality Gate 테스트
독립 실행으로 AFO 패키지 의존성 회피
"""

from __future__ import annotations

import sys
import os
import json
from pathlib import Path

# PYTHONPATH 설정 (AFO 패키지 제외)
sys.path.insert(0, '/Users/brnestrm/Library/Python/3.9/lib/python/site-packages')

import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class SunoConfig:
    base_url: str
    api_key: str
    callback_url: str
    model: str
    timeout_sec: int
    poll_interval_sec: float
    max_retries: int

    @staticmethod
    def from_env() -> SunoConfig:
        return SunoConfig(
            base_url=os.environ.get("SUNO_API_BASE_URL", "https://api.sunoapi.org"),
            api_key=os.environ.get("SUNO_API_KEY", "").strip(),
            callback_url=os.environ.get("SUNO_CALLBACK_URL", "").strip(),
            model=os.environ.get("SUNO_MODEL", "V4_5ALL"),
            timeout_sec=int(os.environ.get("SUNO_TIMEOUT_SEC", "240")),
            poll_interval_sec=float(os.environ.get("SUNO_POLL_INTERVAL_SEC", "3.0")),
            max_retries=int(os.environ.get("SUNO_MAX_RETRIES", "3")),
        )


def timeline_to_suno_request(timeline_state: dict[str, Any], cfg: SunoConfig) -> dict[str, Any]:
    music = timeline_state.get("music") or {}
    template = timeline_state.get("template") or music.get("template") or "default"

    custom_mode = bool(music.get("custom_mode", music.get("customMode", True)))
    instrumental = bool(music.get("instrumental", music.get("is_instrumental", True)))

    style = str(music.get("style") or template).strip()[:1000]
    title = str(music.get("title") or (timeline_state.get("title") or "AFO Track")).strip()[:100]
    negative_tags = str(music.get("negative_tags", music.get("negativeTags", ""))).strip()

    sections = timeline_state.get("sections") or []
    parts = []
    for s in sections:
        st = s.get("start")
        en = s.get("end")
        txt = s.get("text") or ""
        fx = s.get("effects") or []
        parts.append(f"[{st}-{en}] {txt} effects={','.join(map(str, fx))}")
    prompt = (music.get("prompt") or "\n".join(parts) or "Upbeat track").strip()

    payload: dict[str, Any] = {
        "customMode": custom_mode,
        "instrumental": instrumental,
        "model": str(music.get("model") or cfg.model),
        "callBackUrl": str(music.get("callBackUrl") or cfg.callback_url),
        "prompt": prompt,
    }

    if custom_mode:
        payload["style"] = style
        payload["title"] = title
        if negative_tags:
            payload["negativeTags"] = negative_tags
        for k_in, k_out in [
            ("personaId", "personaId"),
            ("vocalGender", "vocalGender"),
            ("styleWeight", "styleWeight"),
            ("weirdnessConstraint", "weirdnessConstraint"),
            ("audioWeight", "audioWeight"),
        ]:
            v = music.get(k_in)
            if v is not None:
                payload[k_out] = v

    return payload


def run_suno_pipeline_dry_run(timeline_state: dict[str, Any]) -> dict[str, Any]:
    """DRY_RUN 전용 함수 - 네트워크 호출 없이 계획만"""
    cfg = SunoConfig.from_env()
    req_payload = timeline_to_suno_request(timeline_state, cfg)

    return {
        "dry_run": True,
        "suno": {
            "base_url": cfg.base_url,
            "model": req_payload.get("model"),
            "customMode": req_payload.get("customMode"),
            "instrumental": req_payload.get("instrumental"),
        },
        "request_payload": {k: v for k, v in req_payload.items() if k != "Authorization"},
        "outputs": {},
        "timeline_sections": len(timeline_state.get("sections", [])),
        "estimated_cost": "~$0.08",
    }


def main():
    # TimelineState 로드
    timeline_path = "artifacts/timeline_state_capcut_smoke.json"
    if not Path(timeline_path).exists():
        print(f"❌ 파일 없음: {timeline_path}")
        return

    with open(timeline_path, 'r', encoding='utf-8') as f:
        timeline = json.load(f)

    print("🎵 SunoBranch DRY_RUN Reality Gate 테스트")
    print(f"Timeline: {timeline.get('title', 'Unknown')}")
    print(f"Sections: {len(timeline.get('sections', []))}")

    try:
        result = run_suno_pipeline_dry_run(timeline)

        print("\n✅ DRY_RUN 성공!")
        print("📋 Request Payload 미리보기:")
        payload = result.get("request_payload", {})
        print(f"  customMode: {payload.get('customMode')}")
        print(f"  instrumental: {payload.get('instrumental')}")
        print(f"  model: {payload.get('model')}")
        print(f"  style: {payload.get('style', 'N/A')}")
        print(f"  title: {payload.get('title', 'N/A')}")
        print(f"  prompt 길이: {len(payload.get('prompt', ''))} chars")
        print(f"  estimated_cost: {result.get('estimated_cost')}")

        print(f"\n🎯 Reality Gate 통과: DRY_RUN payload 생성 성공")
        print("다음 단계: 환경 변수 설정 후 WET 테스트")

        # JSON 출력 (형님의 요구사항)
        print("\n📄 JSON 결과:")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"❌ DRY_RUN 실패: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
