#!/usr/bin/env python3
"""
Phase 4: SBOM (Software Bill of Materials) 생성 스크립트
眞善美孝永 5기둥 철학에 의거한 의존성 투명성 확보

이 스크립트는 AFO 왕국의 모든 의존성을 SBOM 형식으로 생성합니다.
- CycloneDX 형식 지원
- 보안 취약점 스캔 연동
- CI/CD 파이프라인 통합
"""

import sys
from pathlib import Path


try:
    from cyclonedx.output import OutputFormat, get_instance
    from cyclonedx_py.parser.environment import EnvironmentParser
    from cyclonedx_py.parser.requirements import RequirementsParser

    CYCLONEDX_AVAILABLE = True
except ImportError as e:
    CYCLONEDX_AVAILABLE = False
    print(f"⚠️  cyclonedx-python-lib not available: {e}")
    print("   Install with: pip install cyclonedx-python-lib")


def generate_sbom_from_requirements(requirements_path: Path, output_path: Path) -> bool:
    """requirements.txt에서 SBOM 생성"""
    if not CYCLONEDX_AVAILABLE:
        return False

    try:
        parser = RequirementsParser(requirements_file_path=requirements_path)
        bom = parser.parse()

        # JSON 출력
        json_output = get_instance(bom=bom, output_format=OutputFormat.JSON)
        json_output.output_to_file(output_path.with_suffix(".json"), allow_overwrite=True)

        # XML 출력
        xml_output = get_instance(bom=bom, output_format=OutputFormat.XML)
        xml_output.output_to_file(output_path.with_suffix(".xml"), allow_overwrite=True)

        print(f"✅ SBOM generated: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to generate SBOM from {requirements_path}: {e}")
        return False


def generate_sbom_from_environment(output_path: Path) -> bool:
    """현재 Python 환경에서 SBOM 생성"""
    if not CYCLONEDX_AVAILABLE:
        return False

    try:
        parser = EnvironmentParser()
        bom = parser.parse()

        # JSON 출력
        json_output = get_instance(bom=bom, output_format=OutputFormat.JSON)
        json_output.output_to_file(output_path.with_suffix(".json"), allow_overwrite=True)

        # XML 출력
        xml_output = get_instance(bom=bom, output_format=OutputFormat.XML)
        xml_output.output_to_file(output_path.with_suffix(".xml"), allow_overwrite=True)

        print(f"✅ SBOM generated from environment: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to generate SBOM from environment: {e}")
        return False


def main() -> int:
    """메인 함수"""
    print("=" * 80)
    print("🏰 AFO Kingdom - SBOM (Software Bill of Materials) 생성")
    print("=" * 80)
    print()

    if not CYCLONEDX_AVAILABLE:
        print("❌ cyclonedx-python-lib이 설치되지 않았습니다.")
        print("   설치: pip install cyclonedx-python-lib")
        return 1

    # 출력 디렉토리 생성
    output_dir = Path("sbom")
    output_dir.mkdir(exist_ok=True)

    # 1. requirements.txt 파일들에서 SBOM 생성
    requirements_files = [
        Path("packages/afo-core/requirements.txt"),
        Path("packages/trinity-os/requirements.txt"),
        Path("packages/afo-core/requirements_minimal.txt"),
    ]

    success_count = 0
    for req_file in requirements_files:
        if req_file.exists():
            output_path = output_dir / f"{req_file.stem}_sbom"
            if generate_sbom_from_requirements(req_file, output_path):
                success_count += 1

    # 2. 현재 환경에서 SBOM 생성 (종합)
    env_output = output_dir / "environment_sbom"
    if generate_sbom_from_environment(env_output):
        success_count += 1

    print()
    print("=" * 80)
    if success_count > 0:
        print(f"✅ SBOM 생성 완료: {success_count}개 파일")
        print(f"   출력 디렉토리: {output_dir.absolute()}")
    else:
        print("❌ SBOM 생성 실패")
        return 1

    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
