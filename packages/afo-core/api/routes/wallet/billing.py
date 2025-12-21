#!/usr/bin/env python3
"""
Wallet Billing Router - API 사용량 및 청구 관리
Strangler Fig Pattern (간결화 버전)
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException

from .models import API_PROVIDERS

# Create router
billing_router = APIRouter(prefix="/api/wallet/billing", tags=["Wallet Billing"])


@billing_router.get("/usage/{api_id}")
async def get_api_usage(api_id: str) -> dict[str, Any]:
    """
    **API 사용량 조회** - 특정 API의 사용량 및 청구 정보

    **Path Parameter**: api_id (API 식별자)
    **Response**: 사용량 정보
    """
    try:
        import sys

        api_server_module = sys.modules.get("AFO.api_server")
        if api_server_module is None:
            from AFO import api_server as api_server_module

        # 사용량 조회 로직
        # TODO: 실제 사용량 조회 구현
        return {
            "api_id": api_id,
            "usage": {"requests": 0, "tokens": 0, "cost": 0.0},
            "timestamp": datetime.now().isoformat(),
        }

    except ImportError:
        raise HTTPException(status_code=503, detail="Wallet billing not available") from None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get API usage: {e}") from e


@billing_router.get("/summary")
async def get_billing_summary() -> dict[str, Any]:
    """
    **청구 요약** - 전체 API 사용량 및 청구 요약

    **Response**: 청구 요약 정보
    """
    try:
        import sys

        api_server_module = sys.modules.get("AFO.api_server")
        if api_server_module is None:
            from AFO import api_server as api_server_module

        # 청구 요약 로직
        # TODO: 실제 청구 요약 구현
        return {
            "total_apis": len(API_PROVIDERS),
            "total_usage": {"requests": 0, "tokens": 0, "cost": 0.0},
            "timestamp": datetime.now().isoformat(),
        }

    except ImportError:
        raise HTTPException(status_code=503, detail="Wallet billing not available") from None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get billing summary: {e}") from e
