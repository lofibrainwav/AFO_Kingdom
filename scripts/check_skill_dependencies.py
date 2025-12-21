#!/usr/bin/env python3
"""
스킬 의존성 체크 스크립트
Sequential Thinking Phase 2: 스킬별 필요한 패키지 확인
"""

import sys
from pathlib import Path


# packages/afo-core를 경로에 추가
core_path = Path(__file__).parent.parent / "packages" / "afo-core"
sys.path.insert(0, str(core_path))

from AFO.afo_skills_registry import register_core_skills


# Python 패키지 매핑 (스킬 의존성 → 실제 패키지명)
PACKAGE_MAPPING = {
    "openai_api": "openai",
    "transcript_mcp": "mcp",
    "postgresql": "psycopg2",
    "web3.py": "web3",
    "suno-api": "suno",  # sunoai 패키지는 import 시 suno
    "sentence-transformers": "sentence_transformers",
    "hcloud": "hcloud",
    "eth-account": "eth_account",
    "ai-analysis": None,  # 내부 모듈
    "react": None,  # 프론트엔드
    "iframe": None,  # 프론트엔드
    "git": None,  # 시스템 도구
    "docker": None,  # 시스템 도구
    "redis": "redis",
    "langchain": "langchain",
    "langgraph": "langgraph",
    "ragas": "ragas",
    "numpy": "numpy",
    "pandas": "pandas",
    "scipy": "scipy",
    "sympy": "sympy",
    "markdown": "markdown",
    "frontmatter": "frontmatter",  # python-frontmatter는 import 시 frontmatter
    "chromadb": "chromadb",
    "neo4j": "neo4j",
    "boto3": "boto3",
    "requests": "requests",
    "kafka": "kafka",  # kafka-python은 import 시 kafka
    "ruff": "ruff",
    "pytest": "pytest",
    "mcp": "mcp",
}


def check_package(package_name: str) -> tuple[bool, str | None]:
    """패키지 설치 여부 확인"""
    try:
        __import__(package_name)
        return True, None
    except ImportError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Unexpected error: {e}"


def main():
    """메인 함수"""
    print("=" * 80)
    print("🔍 AFO 왕국 스킬 의존성 체크")
    print("=" * 80)
    print()

    # 스킬 등록
    registry = register_core_skills()
    skills = registry.list_all()

    print(f"📋 등록된 스킬: {len(skills)}개\n")

    # 모든 스킬의 의존성 수집
    all_dependencies = set()
    for skill in skills:
        if skill.dependencies:
            all_dependencies.update(skill.dependencies)

    print(f"📦 스킬 의존성 총 {len(all_dependencies)}개\n")

    # 패키지 매핑 및 확인
    installed = []
    missing = []
    optional = []

    for dep in sorted(all_dependencies):
        package_name = PACKAGE_MAPPING.get(dep, dep)

        if package_name is None:
            optional.append(dep)
            print(f"ℹ️  {dep:30s} (시스템/내부 모듈)")
            continue

        is_installed, error = check_package(package_name)
        if is_installed:
            installed.append((dep, package_name))
            print(f"✅ {package_name:30s} ({dep})")
        else:
            missing.append((dep, package_name))
            print(f"❌ {package_name:30s} ({dep}) - {error}")

    print()
    print("=" * 80)
    print("📊 요약:")
    print(f"  ✅ 설치됨: {len(installed)}개")
    print(f"  ❌ 누락: {len(missing)}개")
    print(f"  ℹ️  선택적: {len(optional)}개")
    print("=" * 80)

    if missing:
        print()
        print("📦 설치 필요한 패키지:")
        packages_to_install = [pkg for _, pkg in missing]
        print("poetry add " + " ".join(packages_to_install))

    return len(missing) == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
