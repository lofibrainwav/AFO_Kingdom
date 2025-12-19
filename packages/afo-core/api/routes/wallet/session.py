#!/usr/bin/env python3
"""
Wallet Session Router - 세션 관리 및 추출
Strangler Fig Pattern (간결화 버전)
"""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, HTTPException

from .models import API_PROVIDERS, WalletSessionRequest

# Create router
session_router = APIRouter(prefix="/api/wallet/session", tags=["Wallet Session"])


@session_router.get("/{session_id}")
async def get_wallet_session(session_id: str):
    """
    **Wallet 세션 조회** - 특정 세션 정보 조회

    **Path Parameter**: session_id (세션 식별자)
    **Response**: 세션 정보
    """
    try:
        import sys

        api_server_module = sys.modules.get("AFO.api_server")
        if api_server_module is None:
            from AFO import api_server as api_server_module

        # 세션 조회 로직
        # TODO: 실제 세션 조회 구현
        return {
            "session_id": session_id,
            "status": "active",
            "timestamp": datetime.now().isoformat(),
        }

    except ImportError:
        raise HTTPException(status_code=503, detail="Wallet session not available") from None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get wallet session: {e}") from e


@session_router.post("/extract")
async def extract_wallet_session(request: WalletSessionRequest):
    """
    **Wallet 세션 추출** - 브라우저 세션에서 API 키 추출

    **Request Body**:
    - `session_id` (str): 세션 ID
    - `provider` (str, optional): API 제공자

    **Response**: 추출된 API 키 정보
    """
    try:
        # Provider 검증 (있는 경우)
        if request.provider and request.provider not in API_PROVIDERS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid provider. Must be one of: {', '.join(API_PROVIDERS)}",
            )

        import sys

        api_server_module = sys.modules.get("AFO.api_server")
        if api_server_module is None:
            from AFO import api_server as api_server_module

        # 세션 추출 로직
        # TODO: 실제 세션 추출 구현
        return {
            "status": "success",
            "session_id": request.session_id,
            "provider": request.provider or "unknown",
            "extracted": True,
            "timestamp": datetime.now().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract wallet session: {e}") from e
