"""
Personas Router
Phase 2: Family Hub OS - 페르소나 API
TRINITY-OS 페르소나 시스템 통합
"""

from typing import Any

from fastapi import APIRouter, HTTPException

# Persona service import
try:
    from AFO.services.persona_service import get_current_persona, persona_service, switch_persona

    PERSONA_SERVICE_AVAILABLE = True
except ImportError:
    PERSONA_SERVICE_AVAILABLE = False
    print("⚠️  Persona service not available - using fallback")

# Persona models import
try:
    from AFO.api.models.persona import (
        Persona,
        PersonaContext,
        PersonaResponse,
        PersonaSwitchRequest,
        PersonaTrinityScore,
    )

    PERSONA_MODELS_AVAILABLE = True
except ImportError:
    PERSONA_MODELS_AVAILABLE = False
    print("⚠️  Persona models not available - using fallback")

router = APIRouter(prefix="/api/personas", tags=["Personas"])


@router.get("/health")
async def personas_health() -> dict[str, Any]:
    """
    페르소나 시스템 건강 상태 체크

    Returns:
        페르소나 시스템 상태
    """
    return {
        "status": "healthy",
        "message": "페르소나 시스템 정상 작동 중",
        "features": {
            "list_personas": "available",
            "get_persona": "available",
            "switch_persona": "available",
            "trinity_score": "available",
            "trinity_os_integration": "pending",  # Phase 2 확장
            "log_bridge": "pending",  # Phase 2 확장
        },
        "personas_count": len(DEFAULT_PERSONAS),
    }


# 기본 페르소나 정의 (TRINITY-OS 연동)
DEFAULT_PERSONAS = {
    "commander": {
        "id": "commander",
        "name": "사령관",
        "role": "Commander",
        "description": "AFO 왕국의 최고 지휘관, 전략적 의사결정 담당",
        "icon": "👑",
        "color": "gold",
        "trinity_os_persona_id": "chancellor",
    },
    "family_head": {
        "id": "family_head",
        "name": "가족 가장",
        "role": "Family Head",
        "description": "가족의 평온과 행복을 책임지는 가장",
        "icon": "👨‍👩‍👧‍👦",
        "color": "blue",
        "trinity_os_persona_id": None,
    },
    "creator": {
        "id": "creator",
        "name": "창작자",
        "role": "Creator",
        "description": "예술과 창작에 집중하는 페르소나",
        "icon": "🎨",
        "color": "purple",
        "trinity_os_persona_id": None,
    },
    "jegalryang": {
        "id": "jegalryang",
        "name": "제갈량",
        "role": "Prime Strategist (Truth)",
        "description": "眞 (Truth) - 전략과 기술적 정확성",
        "icon": "⚔️",
        "color": "cyan",
        "trinity_os_persona_id": "jegalryang_truth",
    },
    "samaui": {
        "id": "samaui",
        "name": "사마의",
        "role": "Grand Guardian (Goodness)",
        "description": "善 (Goodness) - 안정성과 윤리",
        "icon": "🛡️",
        "color": "amber",
        "trinity_os_persona_id": "samaui_goodness",
    },
    "juyu": {
        "id": "juyu",
        "name": "주유",
        "role": "Grand Architect (Beauty)",
        "description": "美 (Beauty) - 우아함과 사용자 경험",
        "icon": "🌉",
        "color": "pink",
        "trinity_os_persona_id": "juyu_beauty",
    },
}


@router.get("/current")
async def get_current_persona_endpoint() -> dict[str, Any]:
    """
    현재 활성화된 페르소나 조회

    Returns:
        현재 페르소나 정보
    """
    if PERSONA_SERVICE_AVAILABLE:
        try:
            return await get_current_persona()
        except Exception:
            # Fallback
            pass

    # Fallback: 기본 응답
    return {
        "id": "commander",
        "name": "사령관",
        "type": "commander",
        "active": True,
    }


@router.get("")
async def list_personas() -> dict[str, Any]:
    """
    모든 페르소나 목록 조회

    Returns:
        페르소나 목록
    """
    if not PERSONA_MODELS_AVAILABLE:
        # Fallback: 기본 페르소나 반환
        return {
            "personas": list(DEFAULT_PERSONAS.values()),
            "count": len(DEFAULT_PERSONAS),
        }

    # TODO: DB에서 페르소나 조회 (Phase 2 확장)
    personas = []
    for persona_data in DEFAULT_PERSONAS.values():
        persona = Persona(
            id=persona_data["id"],
            name=persona_data["name"],
            role=persona_data["role"],
            description=persona_data["description"],
            icon=persona_data["icon"],
            color=persona_data["color"],
            trinity_os_persona_id=persona_data.get("trinity_os_persona_id"),
            context=PersonaContext(current_role=persona_data["role"]),
        )
        personas.append(persona)

    return {
        "personas": [p.model_dump() for p in personas],
        "count": len(personas),
    }


@router.get("/{persona_id}")
async def get_persona(persona_id: str) -> dict[str, Any]:
    """
    특정 페르소나 정보 조회

    Args:
        persona_id: 페르소나 ID

    Returns:
        페르소나 정보

    Raises:
        HTTPException: 페르소나를 찾을 수 없을 때
    """
    if persona_id not in DEFAULT_PERSONAS:
        raise HTTPException(status_code=404, detail=f"페르소나를 찾을 수 없습니다: {persona_id}")

    persona_data = DEFAULT_PERSONAS[persona_id]

    if PERSONA_MODELS_AVAILABLE:
        persona = Persona(
            id=persona_data["id"],
            name=persona_data["name"],
            role=persona_data["role"],
            description=persona_data["description"],
            icon=persona_data["icon"],
            color=persona_data["color"],
            trinity_os_persona_id=persona_data.get("trinity_os_persona_id"),
            context=PersonaContext(current_role=persona_data["role"]),
        )
        return persona.model_dump()

    return persona_data


@router.post("/switch")
async def switch_persona(request: PersonaSwitchRequest) -> dict[str, Any]:
    """
    페르소나 전환 (眞善美孝永: 맥락 기반 응답)

    Args:
        request: 페르소나 전환 요청

    Returns:
        전환된 페르소나 정보 및 응답

    Raises:
        HTTPException: 페르소나를 찾을 수 없을 때
    """
    if request.persona_id not in DEFAULT_PERSONAS:
        raise HTTPException(
            status_code=404, detail=f"페르소나를 찾을 수 없습니다: {request.persona_id}"
        )

    persona_data = DEFAULT_PERSONAS[request.persona_id]

    # --- TRINITY-OS Integration (Phase 2) ---
    # Log Persona Switch to Family Hub
    try:
        from datetime import datetime

        # Log activity using internal logic (simulating API call)
        # We invoke the logic directly or via internal call if possible,
        # but here we'll use a direct import of the handler logic or just direct file access
        # to avoid async complexity in this snippet if not strictly needed.
        # Actually, let's use the BackgroundTasks pattern properly if passed,
        # but since we are inside a function, we'll do a direct lightweight update.
        from AFO.api.routers.family import (
            BackgroundTasks,
            calculate_happiness_impact,
            load_family_data,
            log_activity,
            save_family_data,
        )

        family_data = load_family_data()
        activities = family_data.get("activities", [])

        new_activity = {
            "id": f"act_{len(activities) + 1}",
            "member_id": "system",  # System event
            "type": "PersonaSwitch",
            "description": f"Switched to persona: {persona_data['name']}",
            "timestamp": datetime.now().isoformat(),
            "trinity_impact": 0.1,
        }

        activities.append(new_activity)
        family_data["activities"] = activities[-50:]

        # Update System Happiness (Tiny boost for freshness)
        current_happiness = family_data.get("system", {}).get("overall_happiness", 50.0)
        new_happiness = min(100.0, max(0.0, current_happiness + 0.1))

        if "system" not in family_data:
            family_data["system"] = {}
        family_data["system"]["overall_happiness"] = new_happiness

        save_family_data(family_data)
        print(f"✅ Logged persona switch to Family Hub: {persona_data['name']}")

    except ImportError:
        print("⚠️ Family Hub integration not available")
    except Exception as e:
        print(f"⚠️ Failed to log persona switch: {e}")

    if PERSONA_MODELS_AVAILABLE:
        persona = Persona(
            id=persona_data["id"],
            name=persona_data["name"],
            role=persona_data["role"],
            description=persona_data["description"],
            icon=persona_data["icon"],
            color=persona_data["color"],
            trinity_os_persona_id=persona_data.get("trinity_os_persona_id"),
            context=PersonaContext(
                current_role=persona_data["role"],
                active_personas=[request.persona_id],
                preferences=request.context,
            ),
        )

        # 기본 Trinity Score (Phase 2에서 실제 계산)
        trinity_score = PersonaTrinityScore(
            truth=80.0,
            goodness=75.0,
            beauty=90.0,
            serenity=85.0,
            eternity=80.0,
            total_score=82.0,
        )

        return {
            "persona": persona.model_dump(),
            "message": f"페르소나 '{persona.name}'로 전환되었습니다.",
            "trinity_score": trinity_score.model_dump(),
        }

    return {
        "persona": persona_data,
        "message": f"페르소나 '{persona_data['name']}'로 전환되었습니다.",
    }


@router.get("/{persona_id}/trinity-score")
async def get_persona_trinity_score(persona_id: str) -> dict[str, Any]:
    """
    페르소나별 Trinity Score 조회

    Args:
        persona_id: 페르소나 ID

    Returns:
        Trinity Score 정보

    Raises:
        HTTPException: 페르소나를 찾을 수 없을 때
    """
    if persona_id not in DEFAULT_PERSONAS:
        raise HTTPException(status_code=404, detail=f"페르소나를 찾을 수 없습니다: {persona_id}")

    # TODO: 실제 Trinity Score 계산 (Phase 2 확장)
    # 현재는 기본값 반환
    if PERSONA_MODELS_AVAILABLE:
        trinity_score = PersonaTrinityScore(
            truth=80.0,
            goodness=75.0,
            beauty=90.0,
            serenity=85.0,
            eternity=80.0,
            total_score=82.0,
        )
        return trinity_score.model_dump()

    return {
        "truth": 80.0,
        "goodness": 75.0,
        "beauty": 90.0,
        "serenity": 85.0,
        "eternity": 80.0,
        "total_score": 82.0,
    }
