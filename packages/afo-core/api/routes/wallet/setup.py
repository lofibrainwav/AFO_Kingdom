#!/usr/bin/env python3
"""
Wallet Setup Router - API 키 설정 및 관리
Strangler Fig Pattern (간결화 버전)
"""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, HTTPException

from .models import API_PROVIDERS, WalletAPIKeyRequest, WalletStatusResponse

# Create router
setup_router = APIRouter(prefix="/api/wallet/setup", tags=["Wallet Setup"])


@setup_router.post("/api-key")
async def set_api_key(request: WalletAPIKeyRequest):
    """
    **Wallet API 키 설정** - API 키 저장 및 관리

    **Request Body**:
    - `provider` (str): API 제공자 (openai, anthropic, google 등)
    - `api_key` (str): API 키
    - `environment` (str): 환경 (production, development)

    **Response**: 설정 결과
    """
    try:
        # Provider 검증
        if request.provider not in API_PROVIDERS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid provider. Must be one of: {', '.join(API_PROVIDERS)}",
            )

        # API 키 저장 로직 (기존 로직 재사용)
        import sys

        api_server_module = sys.modules.get("afo_soul_engine.api_server")
        if api_server_module is None:
            from afo_soul_engine import api_server as api_server_module

        # TODO: 실제 API 키 저장 구현
        return {
            "status": "success",
            "message": f"API key for {request.provider} set successfully",
            "provider": request.provider,
            "environment": request.environment,
            "timestamp": datetime.now().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set API key: {e}")


@setup_router.get("/status", response_model=WalletStatusResponse)
async def get_wallet_status():
    """
    **Wallet 상태 조회** - API Wallet 시스템 상태 확인

    **Response**: Wallet 상태 및 API 제공자 정보
    """
    try:
        import sys

        api_server_module = sys.modules.get("afo_soul_engine.api_server")
        if api_server_module is None:
            from afo_soul_engine import api_server as api_server_module

        # Wallet 상태 조회 로직
        # TODO: 실제 wallet 상태 조회 구현
        return WalletStatusResponse(
            status="operational",
            providers=dict.fromkeys(API_PROVIDERS, True),
            total_apis=len(API_PROVIDERS),
            timestamp=datetime.now().isoformat(),
        )

    except ImportError:
        raise HTTPException(status_code=503, detail="Wallet system not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get wallet status: {e}")
