"""
Auth Router
Phase 3: 인증 라우터 (心 시스템 - 인증)
JWT 토큰 및 비밀번호 해시 지원
"""

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

# Auth utilities import
try:
    from AFO.api.utils.auth import (
        create_access_token,
        hash_password,
        verify_password,
        verify_token,
    )

    AUTH_UTILS_AVAILABLE = True
except ImportError:
    try:
        import sys
        from pathlib import Path

        _CORE_ROOT = Path(__file__).resolve().parent.parent.parent
        if str(_CORE_ROOT) not in sys.path:
            sys.path.insert(0, str(_CORE_ROOT))
        from api.utils.auth import (
            create_access_token,
            hash_password,
            verify_password,
            verify_token,
        )

        AUTH_UTILS_AVAILABLE = True
    except ImportError:
        AUTH_UTILS_AVAILABLE = False
        print("⚠️  Auth utilities not available - using fallback")

router = APIRouter(prefix="/api/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    """로그인 요청 모델"""

    username: str = Field(..., min_length=1, max_length=50, description="사용자명")
    password: str = Field(..., min_length=1, description="비밀번호")


class LoginResponse(BaseModel):
    """로그인 응답 모델"""

    access_token: str = Field(..., description="액세스 토큰")
    token_type: str = Field(default="bearer", description="토큰 타입")
    expires_in: int = Field(default=3600, description="토큰 만료 시간 (초)")


class TokenResponse(BaseModel):
    """토큰 검증 응답 모델"""

    valid: bool = Field(..., description="토큰 유효성")
    username: str | None = Field(default=None, description="사용자명")


@router.post("/login")
async def login(request: LoginRequest) -> dict[str, Any]:
    """
    사용자 로그인

    Args:
        request: 로그인 요청

    Returns:
        액세스 토큰 및 인증 정보

    Raises:
        HTTPException: 인증 실패 시
    """
    # TODO: 실제 DB 조회 구현 (현재는 기본 검증)
    # 실제로는 DB에서 사용자 조회 및 비밀번호 해시 검증 필요

    if not request.username or not request.password:
        raise HTTPException(status_code=401, detail="사용자명 또는 비밀번호가 올바르지 않습니다.")

    # TODO: DB에서 사용자 조회
    # user = await get_user_by_username(request.username)
    # if not user or not verify_password(request.password, user.hashed_password):
    #     raise HTTPException(status_code=401, detail="인증 실패")

    # 임시: 기본 검증 (실제로는 DB 조회 필요)
    # 여기서는 모든 사용자를 허용 (프로덕션에서는 제거)

    # JWT 토큰 생성
    if AUTH_UTILS_AVAILABLE:
        token_data = {"sub": request.username, "username": request.username}
        access_token = create_access_token(data=token_data)
    else:
        # Fallback: 임시 토큰
        access_token = f"temp_token_{request.username}_{hash(request.password)}"

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 3600 * 24,  # 24시간
    }


@router.post("/verify")
async def verify_token_endpoint(
    token: str = Query(..., description="검증할 토큰"),
) -> dict[str, Any]:
    """
    토큰 검증 (眞善美: Truth + Goodness + Beauty)

    Args:
        token: 검증할 토큰

    Returns:
        토큰 유효성 및 사용자 정보

    Raises:
        HTTPException: 토큰 형식 오류 시 401 (善: 명확한 에러 응답)
    """
    # 眞: 입력 검증
    if not token or not token.strip():
        raise HTTPException(status_code=401, detail="토큰이 제공되지 않았습니다.")

    # 善: Graceful degradation - 예외 처리
    try:
        # JWT 토큰 검증
        if AUTH_UTILS_AVAILABLE:
            from AFO.api.utils.auth import verify_token as verify_token_func

            payload = verify_token_func(token)

            if payload:
                username = payload.get("sub") or payload.get("username")
                return {
                    "valid": True,
                    "username": username,
                    "exp": payload.get("exp"),
                }
            else:
                # 善: 명확한 실패 응답 (401 대신 200 with valid=False)
                return {
                    "valid": False,
                    "username": None,
                    "detail": "토큰이 만료되었거나 유효하지 않습니다.",
                }
        else:
            # Fallback: 임시 토큰 검증
            if not token.startswith("temp_token_"):
                return {
                    "valid": False,
                    "username": None,
                    "detail": "토큰 형식이 올바르지 않습니다.",
                }

            try:
                parts = token.replace("temp_token_", "").split("_")
                username = parts[0] if parts else None

                return {
                    "valid": True,
                    "username": username,
                }
            except Exception as e:
                # 善: 예외 처리
                return {
                    "valid": False,
                    "username": None,
                    "detail": f"토큰 파싱 오류: {e!s}",
                }
    except Exception as e:
        # 善: 예상치 못한 에러 처리 (500 방지)
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"Token verification endpoint error: {e}")

        # 美: 우아한 에러 응답
        raise HTTPException(
            status_code=500, detail=f"토큰 검증 중 서버 오류가 발생했습니다: {e!s}"
        ) from e


@router.get("/health")
async def auth_health() -> dict[str, Any]:
    """
    인증 시스템 건강 상태 체크

    Returns:
        인증 시스템 상태
    """
    return {
        "status": "healthy",
        "message": "인증 시스템 정상 작동 중",
        "features": {
            "login": "available",
            "token_verification": "available",
            "jwt": "available" if AUTH_UTILS_AVAILABLE else "pending",
            "password_hashing": "available" if AUTH_UTILS_AVAILABLE else "pending",
        },
    }
