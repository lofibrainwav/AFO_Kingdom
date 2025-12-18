#!/usr/bin/env python3
"""
TRINITY-OS Problem Detector Tests
"""

import json
import subprocess
import sys
from pathlib import Path


def test_problem_detector():
    """문제 감지 스크립트 테스트"""
    script_path = Path(__file__).parent.parent / "scripts" / "kingdom_problem_detector.py"

    # 스크립트 존재 확인
    assert script_path.exists(), f"Script not found: {script_path}"

    # 실행 가능 확인
    result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True, timeout=30)

    # 실행 성공 확인
    assert result.returncode == 0, f"Script failed with return code {result.returncode}"

    # JSON 출력 확인
    try:
        data = json.loads(result.stdout.strip())
        assert "total_problems" in data, "Missing total_problems in output"
        assert "summary" in data, "Missing summary in output"
        assert isinstance(data["total_problems"], int), "total_problems should be integer"
    except json.JSONDecodeError as e:
        raise AssertionError(f"Invalid JSON output: {e}")

    print("✅ Problem detector test passed")


def test_health_report():
    """건강 리포트 스크립트 테스트"""
    script_path = Path(__file__).parent.parent / "scripts" / "kingdom_health_report.py"

    assert script_path.exists(), f"Script not found: {script_path}"

    result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True, timeout=30)

    assert result.returncode == 0, f"Script failed with return code {result.returncode}"

    try:
        data = json.loads(result.stdout.strip())
        assert "overall_score" in data, "Missing overall_score in output"
        assert "balanced" in data, "Missing balanced in output"
        assert isinstance(data["overall_score"], (int, float)), "overall_score should be numeric"
    except json.JSONDecodeError as e:
        raise AssertionError(f"Invalid JSON output: {e}")

    print("✅ Health report test passed")


def test_spirit_integration():
    """정신 통합 스크립트 테스트"""
    script_path = Path(__file__).parent.parent / "scripts" / "kingdom_spirit_integration.py"

    assert script_path.exists(), f"Script not found: {script_path}"

    result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True, timeout=30)

    assert result.returncode == 0, f"Script failed with return code {result.returncode}"

    try:
        data = json.loads(result.stdout.strip())
        assert "constitution_status" in data, "Missing constitution_status in output"
    except json.JSONDecodeError as e:
        raise AssertionError(f"Invalid JSON output: {e}")

    print("✅ Spirit integration test passed")


if __name__ == "__main__":
    test_problem_detector()
    test_health_report()
    test_spirit_integration()
    print("\n🎉 All tests passed!")
