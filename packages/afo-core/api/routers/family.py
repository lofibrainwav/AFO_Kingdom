"""
Family Router
美 (Beauty): 모듈화 + 일관 네이밍
PDF 페이지 2: 모듈화 + 일관 네이밍
Phase 2: Family Hub OS - 데이터 영속성 + CRUD
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, BackgroundTasks

# Import Models
try:
    from AFO.api.models.family import Activity, FamilyHubSystem, FamilyMember

    MODELS_AVAILABLE = True
except ImportError:
    MODELS_AVAILABLE = False
    print("⚠️ Family Models not available")

router = APIRouter(prefix="/family", tags=["Family Hub"])

# Constants
DATA_FILE = Path("data/family_data.json")

# --- Persistence Layer (永: Eternity) ---


def load_family_data() -> dict:
    """JSON 파일에서 가족 데이터 로드"""
    if not DATA_FILE.exists():
        return {"members": [], "activities": [], "system": {"overall_happiness": 50.0}}

    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to load family data: {e}")
        return {"members": [], "activities": [], "system": {"overall_happiness": 50.0}}


def save_family_data(data: dict):
    """JSON 파일에 가족 데이터 저장 (비동기 처리 권장)"""
    try:
        # Ensure directory exists
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    except Exception as e:
        print(f"⚠️ Failed to save family data: {e}")


# --- Helper Functions ---


def calculate_happiness_impact(activity_type: str) -> float:
    """활동 유형에 따른 행복 영향도 계산 (善: Goodness)"""
    impact_map = {
        "Study": 2.0,  # 성장은 기쁨
        "Play": 3.0,  # 놀이는 활력
        "Rest": 1.0,  # 휴식은 충전
        "Work": 0.5,  # 일은 보람 (혹은 피로)
        "Argument": -5.0,  # 갈등은 고통
        "Meal": 2.0,  # 식사는 화목
        "PersonaSwitch": 0.1,  # 페르소나 전환은 새로운 활력
    }
    return impact_map.get(activity_type, 0.0)


# --- Endpoints ---


@router.get("/")
async def get_family_hub_status() -> dict[str, Any]:
    """
    Family Hub 상태 종합 조회 (Frontend: fetchFamilyStatus)
    Returns: FamilyHubResponse structure
    """
    data = load_family_data()
    members_list = data.get("members", [])

    # Convert members list to dict for frontend Record<string, FamilyMember>
    # Key by 'id' if available, else 'name'
    members_dict = {}
    total_trinity = 0.0
    member_count_with_score = 0

    for m in members_list:
        key = m.get("id", m.get("name", "unknown"))
        members_dict[key] = m

        # Calculate average trinity if pillars exist
        pillars = m.get("pillars", {})
        if pillars:
            # Average of 5 pillars
            score = sum(pillars.values()) / 5.0
            total_trinity += score
            member_count_with_score += 1

    # System happiness as fallback or component
    system_happiness = data.get("system", {}).get("overall_happiness", 50.0)

    # If no members have scores, use system happiness as proxy (normalized 0-1)
    if member_count_with_score > 0:
        avg_score = total_trinity / member_count_with_score
        # Normalize to 0-1 if assumes 100 scale?
        # Pillars usually 0-100.
        # Frontend trinity_score usually 0.0-1.0. Let's assume 0-100 and divide by 100.
        avg_trinity_score = avg_score / 100.0
    else:
        avg_trinity_score = system_happiness / 100.0

    return {
        "members": members_dict,
        "total_members": len(members_list),
        "average_trinity_score": avg_trinity_score,
    }


@router.get("/members")
async def list_members() -> dict[str, Any]:
    """가족 구성원 목록 조회"""
    data = load_family_data()
    return {"members": data.get("members", [])}


@router.post("/members")
async def update_member(member: dict) -> dict[str, Any]:
    """가족 구성원 추가/업데이트"""
    data = load_family_data()
    members = data.get("members", [])

    # Check if exists, update if so
    found = False
    for i, m in enumerate(members):
        if m["id"] == member["id"]:
            members[i] = member
            found = True
            break

    if not found:
        members.append(member)

    data["members"] = members
    save_family_data(data)

    return {"status": "success", "member": member}


@router.post("/activity")
async def log_activity(activity: dict, background_tasks: BackgroundTasks) -> dict[str, Any]:
    """
    새로운 활동 로그 기록 (孝: Serenity - 기록을 통한 안심)
    활동에 따라 행복 지수가 변동됨.
    """
    data = load_family_data()
    activities = data.get("activities", [])

    # Add timestamp/ID if missing
    if "timestamp" not in activity:
        activity["timestamp"] = datetime.now().isoformat()
    if "id" not in activity:
        activity["id"] = f"act_{len(activities) + 1}"

    # Calculate Impact
    impact = calculate_happiness_impact(activity.get("type", "Unknown"))
    activity["trinity_impact"] = impact

    activities.append(activity)

    # Update System Happiness
    current_happiness = data.get("system", {}).get("overall_happiness", 50.0)
    new_happiness = min(100.0, max(0.0, current_happiness + impact))

    if "system" not in data:
        data["system"] = {}
    data["system"]["overall_happiness"] = new_happiness

    data["activities"] = activities[-50:]  # Keep last 50 only (Rolling log)

    save_family_data(data)

    return {
        "status": "logged",
        "impact": impact,
        "new_happiness": new_happiness,
        "activity": activity,
    }


@router.get("/timeline")
async def get_timeline() -> dict[str, Any]:
    """최근 활동 타임라인 조회"""
    data = load_family_data()
    return {"activities": data.get("activities", [])}


@router.get("/happiness")
async def get_family_happiness() -> dict[str, Any]:
    """
    가족 행복 지표 조회 (美: Beauty)
    데이터 기반의 실제 행복 지수 반환
    """
    data = load_family_data()
    return {
        "happiness_score": data.get("system", {}).get("overall_happiness", 50.0),
        "active_members": len([m for m in data.get("members", []) if m.get("status") == "Active"]),
    }


@router.get("/health")
async def family_health() -> dict[str, Any]:
    """Family Hub 시스템 건강 상태 체크"""
    data = load_family_data()
    return {
        "status": "healthy",
        "message": "Family Hub OS v2.0 Online",
        "stats": {
            "members": len(data.get("members", [])),
            "activities_logged": len(data.get("activities", [])),
        },
    }
