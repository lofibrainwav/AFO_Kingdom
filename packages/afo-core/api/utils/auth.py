# Trinity Score: 90.0 (Established by Chancellor)
"""Auth Utilities
JWT 토큰 생성/검증 및 비밀번호 해시 처리
"""

import hashlib
import hmac
import secrets
import time
from datetime import datetime, timedelta
from typing import Any

# JWT 라이브러리 (PyJWT 사용, 없으면 기본 구현)
try:
    import jwt

    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False

# 비밀번호 해시 라이브러리 (passlib 사용, 없으면 기본 구현)
try:
    from passlib.context import CryptContext

    PASSWORD_HASH_AVAILABLE = True
except ImportError:
    PASSWORD_HASH_AVAILABLE = False

# 환경 변수에서 시크릿 키 가져오기
import os

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "afo-kingdom-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# 비밀번호 해시 컨텍스트
if PASSWORD_HASH_AVAILABLE:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
else:
    pwd_context = None


def hash_password(password: str) -> str:
    """비밀번호 해시 생성

    Args:
        password: 평문 비밀번호

    Returns:
        해시된 비밀번호

    """
    if pwd_context:
        return str(pwd_context.hash(password))
    else:
        # Fallback: SHA-256 + salt (프로덕션에서는 사용하지 말 것)
        salt = secrets.token_hex(16)
        return f"{salt}:{hashlib.sha256((password + salt).encode()).hexdigest()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """비밀번호 검증

    Args:
        plain_password: 평문 비밀번호
        hashed_password: 해시된 비밀번호

    Returns:
        검증 결과

    """
    if pwd_context:
        return bool(pwd_context.verify(plain_password, hashed_password))
    else:
        # Fallback: SHA-256 검증
        try:
            salt, password_hash = hashed_password.split(":", 1)
            computed_hash = hashlib.sha256((plain_password + salt).encode()).hexdigest()
            return hmac.compare_digest(computed_hash, password_hash)
        except Exception:
            return False


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """JWT 액세스 토큰 생성

    Args:
        data: 토큰에 포함할 데이터 (예: {"sub": username})
        expires_delta: 만료 시간 (None이면 기본값 사용)

    Returns:
        JWT 토큰 문자열

    """
    if JWT_AVAILABLE:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)

        to_encode.update({"exp": expire, "iat": datetime.utcnow()})

        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return str(encoded_jwt)
    else:
        # Fallback: 간단한 토큰 생성 (프로덕션에서는 사용하지 말 것)
        username = data.get("sub", "unknown")
        timestamp = int(time.time())
        token_data = f"{username}:{timestamp}:{JWT_SECRET_KEY}"
        token_hash = hashlib.sha256(token_data.encode()).hexdigest()
        return f"fallback_token_{username}_{timestamp}_{token_hash[:16]}"


def verify_token(token: str) -> dict[str, Any] | None:
    """JWT 토큰 검증 (眞: Truth - 정확한 예외 처리)

    Args:
        token: JWT 토큰 문자열

    Returns:
        토큰 페이로드 (검증 성공 시) 또는 None (실패 시)

    Raises:
        None (예외는 내부에서 처리하여 None 반환)

    """
    if JWT_AVAILABLE:
        try:
            payload: dict[str, Any] = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            # 善: 명확한 만료 에러 처리
            return None
        except jwt.InvalidTokenError as e:
            # 善: 잘못된 토큰 에러 처리 (디버깅용 로깅)
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(f"Invalid token error: {e}")
            return None
        except Exception as e:
            # 善: 예상치 못한 에러 처리 (디버깅용 로깅)
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Token verification error: {e}")
            return None
    else:
        # Fallback: 간단한 토큰 검증
        try:
            if not token.startswith("fallback_token_"):
                return None

            parts = token.replace("fallback_token_", "").split("_")
            if len(parts) < 2:
                return None

            username = parts[0]
            timestamp = int(parts[1])

            # 토큰 만료 시간 체크 (24시간)
            if time.time() - timestamp > JWT_EXPIRATION_HOURS * 3600:
                return None

            # 토큰 해시 검증
            token_data = f"{username}:{timestamp}:{JWT_SECRET_KEY}"
            expected_hash = hashlib.sha256(token_data.encode()).hexdigest()[:16]
            if parts[2] != expected_hash:
                return None

            return {"sub": username, "exp": timestamp + JWT_EXPIRATION_HOURS * 3600}
        except Exception:
            return None
