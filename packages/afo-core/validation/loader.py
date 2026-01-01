"""
모듈 로딩 책임 모듈 (SOLID: 단일 책임 원칙)

이 모듈은 코드 검증 시스템의 모듈 로딩 기능을 담당합니다.
- code_review_node.py 파일 탐색 및 로딩
- 모듈 검증 및 안전한 임포트
"""

import importlib.util
from pathlib import Path


def load_review_module(root: Path = Path(".")) -> tuple:
    """
    code_review_node 모듈을 안전하게 로딩합니다.

    Args:
        root: 검색 시작 디렉토리

    Returns:
        tuple: (loaded_module, module_path)

    Raises:
        FileNotFoundError: code_review_node.py를 찾을 수 없는 경우
        ImportError: 모듈 로딩 실패 시
    """
    # code_review_node.py 파일 탐색
    hits = list(root.rglob("code_review_node.py"))
    if not hits:
        raise FileNotFoundError("code_review_node.py not found in project")

    target = hits[0]
    print(f"Found code_review_node.py at: {target}")

    # 모듈 스펙 생성 및 검증
    spec = importlib.util.spec_from_file_location("code_review_node", str(target))
    if spec is None:
        raise ImportError(f"Could not create module spec for {target}")

    # 모듈 로딩
    try:
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore
        return mod, target
    except Exception as e:
        raise ImportError(f"Failed to load module {target}: {e}")


def validate_module_interface(mod) -> dict:
    """
    로딩된 모듈의 인터페이스를 검증합니다.

    Args:
        mod: 로딩된 모듈 객체

    Returns:
        dict: 검증 결과
    """
    interfaces = {
        "has_CodeReviewCoordinator": hasattr(mod, "CodeReviewCoordinator"),
        "has_code_review_node": hasattr(mod, "code_review_node"),
        "has_execute": hasattr(mod, "execute"),
        "has_simple_syntax_check": hasattr(mod, "simple_syntax_check"),
    }

    # 사용 가능한 인터페이스 카운트
    available_count = sum(interfaces.values())

    return {
        "interfaces": interfaces,
        "available_count": available_count,
        "is_valid": available_count > 0,
    }
