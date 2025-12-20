"""
善 (Goodness) 에러 처리 유틸리티

AFO 왕국의 안전하고 윤리적인 에러 처리 패턴
"""

import functools
import logging
from collections.abc import Callable
from typing import Any, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class AFOError(Exception):
    """AFO 왕국 기본 예외 클래스"""

    def __init__(self, message: str, code: str = "AFO_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ValidationError(AFOError):
    """입력 검증 오류"""

    def __init__(self, message: str):
        super().__init__(message, code="VALIDATION_ERROR")


class ServiceUnavailableError(AFOError):
    """서비스 불가 오류"""

    def __init__(self, service: str, reason: str = ""):
        message = f"서비스 불가: {service}"
        if reason:
            message += f" ({reason})"
        super().__init__(message, code="SERVICE_UNAVAILABLE")


class ConfigurationError(AFOError):
    """설정 오류"""

    def __init__(self, key: str, reason: str = ""):
        message = f"설정 오류: {key}"
        if reason:
            message += f" ({reason})"
        super().__init__(message, code="CONFIG_ERROR")


def safe_execute(
    func: Callable[..., T],
    *args: Any,
    default: T | None = None,
    log_error: bool = True,
    reraise: bool = False,
    **kwargs: Any,
) -> T | None:
    """
    함수를 안전하게 실행 (善 패턴)

    Args:
        func: 실행할 함수
        *args: 위치 인자
        default: 실패 시 반환할 기본값
        log_error: 에러 로깅 여부
        reraise: 예외 재발생 여부
        **kwargs: 키워드 인자

    Returns:
        함수 결과 또는 기본값

    Example:
        >>> result = safe_execute(risky_function, default="fallback")
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if log_error:
            logger.error(f"[善] 안전 실행 실패: {func.__name__} - {e}")
        if reraise:
            raise
        return default


def with_fallback(primary: Callable[..., T], fallback: Callable[..., T]) -> Callable[..., T]:
    """
    폴백 전략 데코레이터 (善 패턴)

    Args:
        primary: 주 함수
        fallback: 폴백 함수

    Returns:
        래핑된 함수

    Example:
        >>> @with_fallback(get_from_cache, get_from_db)
        ... def get_data(): ...
    """

    @functools.wraps(primary)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            return primary(*args, **kwargs)
        except Exception as e:
            logger.warning(f"[善] 폴백 실행: {primary.__name__} → {fallback.__name__} ({e})")
            return fallback(*args, **kwargs)

    return wrapper


def validate_input(
    value: Any, name: str, validator: Callable[[Any], bool], message: str = ""
) -> Any:
    """
    입력 검증 (善 패턴)

    Args:
        value: 검증할 값
        name: 파라미터 이름
        validator: 검증 함수
        message: 실패 메시지

    Returns:
        검증된 값

    Raises:
        ValidationError: 검증 실패 시

    Example:
        >>> api_key = validate_input(key, "api_key", lambda k: k.startswith("sk-"))
    """
    if not validator(value):
        error_msg = message or f"{name} 검증 실패"
        logger.error(f"[善] 입력 검증 실패: {error_msg}")
        raise ValidationError(error_msg)
    return value


def require_not_none(value: T | None, name: str) -> T:
    """
    None 검증 (善 패턴)

    Args:
        value: 검증할 값
        name: 파라미터 이름

    Returns:
        검증된 값

    Raises:
        ValidationError: None인 경우

    Example:
        >>> user = require_not_none(get_user(id), "user")
    """
    if value is None:
        raise ValidationError(f"{name}은(는) 필수입니다")
    return value


def log_and_return_error(error: Exception, context: str = "") -> dict[str, Any]:
    """
    에러 로깅 및 표준 응답 생성 (善 패턴)

    Args:
        error: 발생한 예외
        context: 컨텍스트 정보

    Returns:
        표준 에러 응답 딕셔너리
    """
    error_code = getattr(error, "code", "UNKNOWN_ERROR")
    error_msg = str(error)

    logger.error(f"[善] {context}: {error_code} - {error_msg}")

    return {
        "success": False,
        "error": error_msg,
        "error_code": error_code,
        "context": context,
    }


# 에러 코드 상수 (眞 패턴: 타입 안전)
class ErrorCodes:
    """AFO 왕국 표준 에러 코드"""

    VALIDATION_ERROR = "VALIDATION_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    CONFIG_ERROR = "CONFIG_ERROR"
    AUTH_ERROR = "AUTH_ERROR"
    NOT_FOUND = "NOT_FOUND"
    INTERNAL_ERROR = "INTERNAL_ERROR"
