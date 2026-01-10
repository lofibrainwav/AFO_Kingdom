#!/usr/bin/env python3
"""왕국 현재 상태 기반 Trinity Score 계산 테스트."""

import os
import pathlib
import sys

# 경로 추가
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent, "packages", "afo-core"))


def calculate_current_kingdom_trinity_score():
    """현재 왕국 상태를 평가하여 Trinity Score 계산."""

    # 현재 왕국 상태 데이터 (지피지기 결과 기반)
    kingdom_status = {
        "valid_structure": True,  # 헌법 준수 확인됨
        "risk_level": 0.05,  # 모델 스위칭 WARN이지만 전체 GREEN
        "narrative": "complete",  # 41가지 원칙 완전 구현
        "system_health": "GREEN",  # 헬스 체크 GREEN
        "trinity_os_score": 100,  # TRINITY-OS 완벽
        "mcp_servers": 11,  # 11개 MCP 서버 운영
        "skills_registry": 30,  # 30개 Skills 등록
        "api_endpoints": 49,  # 49개 API 엔드포인트
    }

    try:
        from AFO.services.trinity_calculator import trinity_calculator

        # Raw scores 계산
        raw_scores = trinity_calculator.calculate_raw_scores(kingdom_status)
        print(f"Raw Scores: {raw_scores}")

        # Trinity Score 계산
        final_score = trinity_calculator.calculate_trinity_score(raw_scores)
        print(f"Trinity Score: {final_score}")

        # 5기둥별 해석
        pillars = [
            "眞 (Truth)",
            "善 (Goodness)",
            "美 (Beauty)",
            "孝 (Serenity)",
            "永 (Eternity)",
        ]
        for i, (pillar, score) in enumerate(zip(pillars, raw_scores)):
            print(f"{pillar}: {score:.2f} ({score*100:.0f}%)")

        return final_score

    except Exception as e:
        print(f"Trinity Score 계산 실패: {e}")
        import traceback

        traceback.print_exc()
        return None


if __name__ == "__main__":
    score = calculate_current_kingdom_trinity_score()
    if score is not None:
        print(f"\n🎯 최종 Trinity Score: {score}/100")
        if score >= 90:
            print("등급: 백전불태 준비 완료 🌟")
        elif score >= 70:
            print("등급: 양호 ⚡")
        else:
            print("등급: 개선 필요 🔧")
    else:
        print("Trinity Score 계산에 실패했습니다.")
