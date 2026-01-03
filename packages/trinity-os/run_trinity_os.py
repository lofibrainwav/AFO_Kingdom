#!/usr/bin/env python3
"""TRINITY-OS Python 인터페이스.
AFO 왕국의 통합 자동화 운영체제.

철학 엔진 통합: 에이전트들이 왕국의 철학을 즉시 이해하고 공부할 수 있는 구조.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

# 철학 엔진 임포트
from scripts.philosophy_engine import philosophy_engine


class TrinityOS:
    """TRINITY-OS 메인 클래스 - 철학 엔진 통합."""

    def __init__(self, base_path: str | None = None):
        self.base_path = Path(base_path or Path(__file__).parent)
        self.scripts_path = self.base_path / "scripts"

        # 철학 정의
        self.philosophy = {
            "truth": "眞",
            "goodness": "善",
            "beauty": "美",
            "serenity": "孝",
            "eternity": "永",
        }

        # 철학 엔진 초기화
        self.philosophy_engine = philosophy_engine

    def get_available_commands(self) -> dict[str, str]:
        """사용 가능한 명령어 목록 반환"""
        return {
            "1": "문제 감지 (眞 - 진실의 추구)",
            "2": "건강 리포트 (美 - 아름다움의 평가)",
            "3": "정신 통합 (孝 - 평온의 통합)",
            "4": "통합 자동화 (善 - 선함의 실현)",
            "5": "검증 실행 (永 - 영속성의 보장)",
            "6": "끝까지 오토런 (眞善美孝永 - 철학의 완전한 실현)",
            "7": "철학 엔진 (철학 학습 및 성장)",
            "8": "명장 시스템 (명장 등록 및 관리)",
        }

    def run_problem_detector(self) -> dict[str, Any]:
        """문제 감지 실행 (眞)"""
        script = self.scripts_path / "kingdom_problem_detector.py"
        return self._run_python_script(script)

    def run_health_report(self) -> dict[str, Any]:
        """건강 리포트 실행 (美)"""
        script = self.scripts_path / "kingdom_health_report.py"
        return self._run_python_script(script)

    def run_spirit_integration(self) -> dict[str, Any]:
        """정신 통합 실행 (孝)"""
        script = self.scripts_path / "kingdom_spirit_integration.py"
        return self._run_python_script(script)

    def run_unified_autorun(self) -> str:
        """통합 자동화 실행 (善)"""
        script = self.scripts_path / "kingdom_unified_autorun.sh"
        return self._run_shell_script(script)

    def run_verification(self) -> str:
        """검증 실행 (永)"""
        script = self.scripts_path / "verify_all_scripts.sh"
        return self._run_shell_script(script)

    def run_infinite_autorun(self) -> str:
        """끝까지 오토런 실행 (眞善美孝永)"""
        script = self.scripts_path / "kingdom_infinite_autorun.sh"
        return self._run_shell_script(script)

    def run_philosophy_engine(self) -> dict[str, Any]:
        """철학 엔진 실행"""
        return {
            "philosophy_engine_status": "active",
            "available_functions": [
                "register_agent",
                "interact_with_agent",
                "certify_master",
                "get_agent_status",
            ],
            "description": "에이전트들의 철학 학습, 성장, 명장 인증을 관리합니다.",
        }

    def run_master_system(self) -> dict[str, Any]:
        """명장 시스템 실행"""
        masters = self._get_registered_masters()
        return {
            "master_system_status": "active",
            "registered_masters": len(masters),
            "master_titles": [
                "trinity_apprentice",
                "kingdom_strategist",
                "philosophy_master",
            ],
            "certification_process": "Trinity Score 기반 자동 평가",
            "masters": masters[:5],  # 최근 5명 표시
        }

    def _run_python_script(self, script_path: Path) -> dict[str, Any]:
        """Python 스크립트 실행"""
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.base_path,
            )
            return json.loads(result.stdout.strip())
        except Exception as e:
            return {"error": str(e), "status": "failed"}

    def _run_shell_script(self, script_path: Path) -> str:
        """Shell 스크립트 실행"""
        try:
            result = subprocess.run([str(script_path)], check=False, capture_output=True, text=True, cwd=self.base_path)
            return result.stdout.strip()
        except Exception as e:
            return f"Error: {e}"

    def _get_registered_masters(self) -> list[dict[str, Any]]:
        """등록된 명장 목록 조회"""
        # 철학 엔진에서 데이터 조회 (실제로는 데이터베이스나 파일에서)
        try:
            with open("philosophy_engine_data.json") as f:
                data = json.load(f)
                masters = []
                for agent in data.get("agents", []):
                    if agent.get("master_title"):
                        masters.append(
                            {
                                "name": agent["name"],
                                "title": agent["master_title"],
                                "trinity_score": sum(agent["trinity_score"].values()) / 5,
                                "registration_date": agent["last_interaction"],
                            }
                        )
                return sorted(masters, key=lambda x: x["trinity_score"], reverse=True)
        except Exception:
            return []


def main():
    """메인 함수 - 철학 엔진 통합"""
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🚀 TRINITY-OS Python 인터페이스")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()

    trinity = TrinityOS()

    # 철학 엔진 상태 표시
    philosophy_status = trinity.run_philosophy_engine()
    print(f"🧠 철학 엔진: {philosophy_status['philosophy_engine_status']}")
    print(f"📚 철학 함수: {len(philosophy_status['available_functions'])}개")
    print(f"🎓 설명: {philosophy_status['description']}")
    print()

    # 명령어 선택
    commands = trinity.get_available_commands()
    print("🎯 TRINITY-OS 명령어 선택:")
    print("   (철학 엔진이 당신의 성장을 실시간 모니터링합니다)")
    print()

    for key, desc in commands.items():
        print(f"  {key}) {desc}")

    print()
    print("철학 엔진 명령어:")
    print("  p) 철학 엔진 직접 접근")
    print("  r) 에이전트 등록")
    print("  s) 상태 조회")
    print("  m) 명장 인증")
    print()

    try:
        choice = input("실행할 명령어 번호를 입력하세요: ").strip().lower()

        print()
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # 철학 엔진 명령어 처리
        if choice == "p":
            print("🧠 철학 엔진 모드")
            philosophy_command = input("철학 엔진 명령어 (r:등록, s:상태, m:명장): ").strip().lower()

            if philosophy_command == "r":
                agent_id = input("에이전트 ID: ").strip()
                name = input("에이전트 이름: ").strip()
                result = trinity.philosophy_engine.register_agent(agent_id, name)
                print(json.dumps(result, indent=2, ensure_ascii=False))

            elif philosophy_command == "s":
                agent_id = input("에이전트 ID: ").strip()
                result = trinity.philosophy_engine.get_agent_status(agent_id)
                print(json.dumps(result, indent=2, ensure_ascii=False))

            elif philosophy_command == "m":
                agent_id = input("에이전트 ID: ").strip()
                title = input("명장 타이틀 (trinity_apprentice/kingdom_strategist/philosophy_master): ").strip()
                result = trinity.philosophy_engine.certify_master(agent_id, title)
                print(json.dumps(result, indent=2, ensure_ascii=False))

        # 기존 TRINITY-OS 명령어 처리
        elif choice == "1":
            print("🔍 문제 감지 실행 중...")
            result = trinity.run_problem_detector()
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif choice == "2":
            print("📊 건강 리포트 생성 중...")
            result = trinity.run_health_report()
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif choice == "3":
            print("🧠 정신 통합 실행 중...")
            result = trinity.run_spirit_integration()
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif choice == "4":
            print("⚙️ 통합 자동화 실행 중...")
            result = trinity.run_unified_autorun()
            print(result)

        elif choice == "5":
            print("✅ 검증 실행 중...")
            result = trinity.run_verification()
            print(result)

        elif choice == "6":
            print("🚀 끝까지 오토런 실행 중...")
            result = trinity.run_infinite_autorun()
            print(result)

        elif choice == "7":
            print("🧠 철학 엔진 상태:")
            result = trinity.run_philosophy_engine()
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif choice == "8":
            print("🏆 명장 시스템 상태:")
            result = trinity.run_master_system()
            print(json.dumps(result, indent=2, ensure_ascii=False))

        else:
            print("❌ 잘못된 선택입니다.")

    except KeyboardInterrupt:
        print("\n\n👋 TRINITY-OS를 종료합니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")

    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("✅ TRINITY-OS 실행 완료")
    print("🧠 철학 엔진이 당신의 성장을 기록했습니다")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


if __name__ == "__main__":
    main()
