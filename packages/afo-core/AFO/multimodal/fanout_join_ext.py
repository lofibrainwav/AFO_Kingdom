"""
Multimodal FANOUT-JOIN Extension - 병렬 브랜치 확장
TimelineState를 입력으로 VideoBranch + MusicBranch를 병렬로 생성하고 JOIN

ABSORB → GENERATE → FANOUT(VideoBranch + MusicBranch) → JOIN → RENDER
"""

import json
from typing import Any, Dict, List, TypedDict

from langgraph.graph import END, StateGraph

from AFO.multimodal.capcut_branch import capcut_edit_video
from AFO.multimodal.fusion_branch import fusion_composite
from AFO.multimodal.music_branch import music_branch_processor
from AFO.multimodal.timeline_state_generator import timeline_generator_node
from AFO.multimodal.video_branch import video_branch_processor


class MultimodalState(TypedDict):
    """확장된 멀티모달 상태 - 병렬 브랜치 지원"""

    raw_intent: str
    timeline: dict[str, Any]
    video_plan: dict[str, Any]  # VideoBranch 출력
    music_plan: dict[str, Any]  # MusicBranch 출력
    joined_plan: dict[str, Any]  # JOIN 결과
    fusion_plan: dict[str, Any]  # Fusion 결과
    capcut_plan: dict[str, Any]  # CapCut 결과


def video_branch_node(state: MultimodalState) -> dict[str, Any]:
    """
    VideoBranch: TimelineState를 비디오 계획으로 변환
    가져온 video_branch_processor를 사용하여 전문적인 파라미터 확장 수행
    """
    timeline = state.get("timeline", {})
    sections = timeline.get("sections", [])

    # 전문 프로세서 호출
    rendered_sections = video_branch_processor(sections)

    video_plan = {
        "total_duration": timeline.get("total_duration", "0:00"),
        "template_type": timeline.get("template_type", "standard"),
        "sections": rendered_sections,
    }

    return {"video_plan": video_plan}


def music_branch_node(state: MultimodalState) -> dict[str, Any]:
    """
    MusicBranch: TimelineState를 음악 계획으로 변환
    가져온 music_branch_processor를 사용하여 전문적인 파라미터 확장 수행
    """
    timeline = state.get("timeline", {})
    sections = timeline.get("sections", [])

    # 전문 프로세서 호출
    rendered_sections = music_branch_processor(sections)

    music_plan = {
        "total_duration": timeline.get("total_duration", "0:00"),
        "bpm": 128 if timeline.get("template_type") == "short" else 95,
        "sections": rendered_sections,
    }

    return {"music_plan": music_plan}


def join_node(state: MultimodalState) -> dict[str, Any]:
    """
    JOIN: VideoBranch + MusicBranch를 하나의 통합 계획으로 합류
    시간 기반 동기화로 동일한 타임라인에 결혼식처럼 묶기
    """
    video_plan = state.get("video_plan", {})
    music_plan = state.get("music_plan", {})
    timeline = state.get("timeline", {})

    # JOIN 로직: 시간 기반으로 비디오 + 음악 포인트 통합
    joined_sections = []

    video_sections = video_plan.get("sections", [])
    music_sections = music_plan.get("sections", [])

    # 동일한 시간 구간을 기준으로 JOIN (zip으로 동기화)
    for video_sec, music_sec in zip(video_sections, music_sections):
        if video_sec.get("time") == music_sec.get("time"):  # 시간 매칭 검증
            joined_section = {
                "time": video_sec.get("time"),
                "intent": video_sec.get("intent"),
                "video": video_sec.get("video_params", {}),
                "music": music_sec.get("music_params", {}),
                "description": video_sec.get("description"),
                "sync_status": "perfect_sync",  # 동기화 상태 표시
            }
            joined_sections.append(joined_section)

    joined_plan = {
        "total_duration": timeline.get("total_duration", "0:00"),
        "sections": joined_sections,
        "sync_method": "time_based_join",
        "branches_merged": ["video", "music"],
    }

    return {"joined_plan": joined_plan}


def fusion_node(state: MultimodalState) -> dict[str, Any]:
    """
    FUSION: DaVinci Resolve Fusion 컴포지팅 계획 생성
    """
    joined_plan = state.get("joined_plan", {})
    sections = joined_plan.get("sections", [])

    # 더미 입력 클립 리스트 생성 (실제 환경에서는 DB나 파일 시스템에서 가져옴)
    input_clips = [f"/assets/clips/clip_{i}.mp4" for i in range(len(sections))]

    # Fusion 컴포지팅 계획 생성 (Dry Run)
    result = fusion_composite(
        sections, input_clips, "/output/fusion_composite.mp4", dry_run=True
    )

    return {"fusion_plan": result}


def capcut_node(state: MultimodalState) -> dict[str, Any]:
    """
    CAPCUT: TikTok 스타일 비디오 편집 계획 생성
    """
    joined_plan = state.get("joined_plan", {})
    sections = joined_plan.get("sections", [])

    # CapCut 스타일 편집 계획 생성 (Dry Run)
    result = capcut_edit_video(
        sections,
        "/output/fusion_composite.mp4",
        "/output/final_tiktok_style.mp4",
        template="tiktok_trend",
        dry_run=True,
    )

    return {"capcut_plan": result}


def render_node(state: MultimodalState) -> dict[str, Any]:
    """
    RENDER: 통합된 멀티모달 계획을 출력
    세종/개발자/바이브 모드 지원
    """
    joined_plan = state.get("joined_plan", {})
    fusion_plan = state.get("fusion_plan", {})
    capcut_plan = state.get("capcut_plan", {})

    # 구조화된 출력
    output = {
        "status": "멀티모달 통합 파이프라인 생성 완료",
        "total_duration": joined_plan.get("total_duration", "0:00"),
        "joined_plan": joined_plan,
        "fusion_plan": fusion_plan,
        "capcut_plan": capcut_plan,
        "pipeline_stages": ["ABSORB", "GENERATE", "FANOUT", "JOIN", "FUSION", "CAPCUT"],
    }

    return {"output": json.dumps(output, indent=2, ensure_ascii=False)}


# 확장된 워크플로우 빌드
def build_multimodal_workflow() -> StateGraph:
    """멀티모달 FANOUT-JOIN 워크플로우 빌드"""
    workflow = StateGraph(MultimodalState)

    # 기존 노드
    workflow.add_node(
        "absorb", lambda state: {"raw_intent": state.get("raw_intent", "흥겨운 콘텐츠")}
    )
    workflow.add_node(
        "generate",
        lambda state: {
            "timeline": {
                "sections": [
                    {
                        "time": "0:00-0:15",
                        "intent": "intro",
                        "video": "fade_in",
                        "music": "slow_build",
                    },
                    {
                        "time": "0:15-0:30",
                        "intent": "hook",
                        "video": "text_overlay",
                        "music": "drop_beat",
                    },
                    {
                        "time": "0:30-0:45",
                        "intent": "content",
                        "video": "cut_sequence",
                        "music": "main_theme",
                    },
                    {
                        "time": "0:45-1:00",
                        "intent": "climax",
                        "video": "zoom_effect",
                        "music": "peak_energy",
                    },
                    {
                        "time": "1:00-1:15",
                        "intent": "outro",
                        "video": "fade_out",
                        "music": "resolve",
                    },
                ],
                "total_duration": "1:15",
            }
        },
    )

    # FANOUT 노드 (병렬)
    workflow.add_node("video_branch", video_branch_node)
    workflow.add_node("music_branch", music_branch_node)

    # JOIN 노드
    workflow.add_node("join", join_node)
    workflow.add_node("fusion", fusion_node)
    workflow.add_node("capcut", capcut_node)
    workflow.add_node("render", render_node)

    # 플로우 설정
    workflow.set_entry_point("absorb")
    workflow.add_edge("absorb", "generate")

    # FANOUT: 단일 입력 → 병렬 브랜치
    workflow.add_edge("generate", "video_branch")
    workflow.add_edge("generate", "music_branch")

    # JOIN: 병렬 브랜치 → 단일 출력
    workflow.add_edge("video_branch", "join")
    workflow.add_edge("music_branch", "join")
    workflow.add_edge("join", "fusion")
    workflow.add_edge("fusion", "capcut")
    workflow.add_edge("capcut", "render")
    workflow.add_edge("render", END)

    return workflow


# 워크플로우 컴파일
multimodal_workflow = build_multimodal_workflow()
multimodal_app = multimodal_workflow.compile()


def generate_multimodal_plan(intent: str = "흥겨운 콘텐츠") -> dict[str, Any]:
    """
    멀티모달 병렬 계획 생성 편의 함수

    Args:
        intent: 멀티모달 콘텐츠 의도

    Returns:
        통합된 멀티모달 계획 딕셔너리
    """
    initial_state = MultimodalState(
        raw_intent=intent,
        timeline={},
        video_plan={},
        music_plan={},
        joined_plan={},
        fusion_plan={},
        capcut_plan={},
    )

    result = multimodal_app.invoke(initial_state)

    # JSON 문자열을 딕셔너리로 변환하여 반환
    if isinstance(result.get("output"), str):
        return json.loads(result["output"])
    return result


if __name__ == "__main__":
    # 테스트 실행
    result = generate_multimodal_plan("신나는 댄스 음악 + 역동적인 비디오")
    print("멀티모달 병렬 계획 생성 결과:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
