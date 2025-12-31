"""
티켓 생성기: MD 파싱 + 매칭 결과를 바탕으로 티켓 자동 생성
MD→티켓 자동화의 최종 컴포넌트
"""

from datetime import datetime
from pathlib import Path

from .matching_engine import MatchingResult
from .md_parser import ParsedMD


class TicketGenerator:
    """
    MD 파싱 결과를 기반으로 티켓을 자동 생성하는 클래스
    TICKETS.md 업데이트와 개별 티켓 파일 생성을 담당
    """

    def __init__(self, tickets_dir: str = "tickets", tickets_md: str = "TICKETS.md"):
        self.tickets_dir = Path(tickets_dir)
        self.tickets_md = Path(tickets_md)
        self.tickets_dir.mkdir(exist_ok=True)

    def generate_ticket(
        self,
        parsed_md: ParsedMD,
        matching_result: MatchingResult,
        priority: str = "medium",
        complexity: int = 5,
    ) -> str:
        """
        파싱된 MD와 매칭 결과를 바탕으로 티켓 생성

        Args:
            parsed_md: 파싱된 MD 데이터
            matching_result: 매칭 엔진 결과
            priority: 티켓 우선순위 (high, medium, low)
            complexity: 티켓 복잡도 (1-10)

        Returns:
            str: 생성된 티켓 ID
        """
        # 티켓 ID 생성
        ticket_id = self._generate_ticket_id()

        # 티켓 데이터 구성
        ticket_data = self._build_ticket_data(
            ticket_id, parsed_md, matching_result, priority, complexity
        )

        # 티켓 파일 생성
        ticket_file = self.tickets_dir / f"{ticket_id}.md"
        self._write_ticket_file(ticket_file, ticket_data)

        # TICKETS.md 업데이트
        self._update_tickets_md(ticket_data)

        return ticket_id

    def _generate_ticket_id(self) -> str:
        """다음 티켓 ID 생성"""
        if not self.tickets_dir.exists():
            return "TICKET-001"

        # 기존 티켓 파일들 찾기
        ticket_files = list(self.tickets_dir.glob("TICKET-*.md"))
        if not ticket_files:
            return "TICKET-001"

        # 가장 높은 번호 찾기
        max_num = 0
        for ticket_file in ticket_files:
            try:
                num_str = ticket_file.stem.replace("TICKET-", "")
                num = int(num_str)
                max_num = max(max_num, num)
            except ValueError:
                continue

        return "04d"

    def _build_ticket_data(
        self,
        ticket_id: str,
        parsed_md: ParsedMD,
        matching_result: MatchingResult,
        priority: str,
        complexity: int,
    ) -> dict:
        """티켓 데이터 구성"""
        now = datetime.now().isoformat()

        # Trinity Score 계산 (간단 버전)
        trinity_score = self._calculate_trinity_score(parsed_md, matching_result)

        # 의존성 추정
        dependencies = self._infer_dependencies(parsed_md, matching_result)

        # 상태 결정
        status = "pending"  # 기본값

        ticket_data = {
            "id": ticket_id,
            "title": self._generate_title(parsed_md),
            "summary": parsed_md.goal,
            "status": status,
            "priority": priority,
            "complexity": complexity,
            "created_at": now,
            "updated_at": now,
            "goal": parsed_md.goal,
            "files_to_create": parsed_md.files_to_create or [],
            "files_to_update": parsed_md.files_to_update or [],
            "raw_notes": parsed_md.raw_notes,
            "constraints": parsed_md.constraints or [],
            "matching_candidates": [
                {
                    "module": candidate.module.path,
                    "similarity": candidate.similarity_score,
                    "reason": candidate.match_reason,
                }
                for candidate in matching_result.candidates[:5]  # 상위 5개만
            ],
            "best_match": (
                {
                    "module": matching_result.best_match.module.path,
                    "similarity": matching_result.best_match.similarity_score,
                    "reason": matching_result.best_match.match_reason,
                }
                if matching_result.best_match
                else None
            ),
            "recommendations": matching_result.recommendations,
            "trinity_score": trinity_score,
            "estimated_dependencies": dependencies,
            "acceptance_criteria": self._generate_acceptance_criteria(parsed_md),
        }

        return ticket_data

    def _generate_title(self, parsed_md: ParsedMD) -> str:
        """티켓 제목 생성"""
        goal = parsed_md.goal.strip()

        # 목표에서 핵심 동사 + 목적어 추출 시도
        if len(goal) > 80:
            # 너무 길면 줄임
            goal = goal[:77] + "..."

        return goal

    def _calculate_trinity_score(
        self, parsed_md: ParsedMD, matching_result: MatchingResult
    ) -> dict[str, float]:
        """Trinity Score 계산 (간단 버전)"""
        # 眞 (Truth): 기술적 정확성 - 매칭 점수 기반
        truth_score = min(matching_result.confidence_score * 100, 100)

        # 善 (Goodness): 윤리/안정성 - 제약사항 준수도 기반
        goodness_score = 85.0  # 기본값
        if parsed_md.constraints:
            goodness_score = 95.0  # 제약사항이 명시적이면 높음

        # 美 (Beauty): 단순함/우아함 - 파일 수 기반
        total_files = len(parsed_md.files_to_create or []) + len(parsed_md.files_to_update or [])
        beauty_score = max(100 - (total_files * 5), 60)  # 파일이 많을수록 복잡도 증가

        # 孝 (Serenity): 형님 마찰 제거 - 자동화 수준 기반
        serenity_score = 90.0  # MD→티켓 자동화이므로 높음

        # 永 (Eternity): 지속성 - 문서화 품질 기반
        eternity_score = 85.0  # 구조화된 티켓 생성이므로 높음

        # 가중 평균 계산
        weights = {
            "truth": 0.35,
            "goodness": 0.35,
            "beauty": 0.20,
            "serenity": 0.08,
            "eternity": 0.02,
        }
        total_score = (
            truth_score * weights["truth"]
            + goodness_score * weights["goodness"]
            + beauty_score * weights["beauty"]
            + serenity_score * weights["serenity"]
            + eternity_score * weights["eternity"]
        )

        return {
            "truth": truth_score,
            "goodness": goodness_score,
            "beauty": beauty_score,
            "serenity": serenity_score,
            "eternity": eternity_score,
            "total": total_score,
        }

    def _infer_dependencies(
        self, parsed_md: ParsedMD, matching_result: MatchingResult
    ) -> list[str]:
        """의존성 추정"""
        dependencies = []

        # 매칭된 모듈들의 의존성 수집
        for candidate in matching_result.candidates[:3]:  # 상위 3개만
            dependencies.extend(candidate.module.dependencies)

        # 키워드 기반 의존성 예측
        from .matching_engine import MatchingEngine
        from .skeleton_index import SkeletonIndex

        # 임시 스켈레톤 인덱스 생성 (의존성 예측용)
        temp_index = SkeletonIndex(packages={}, services={}, configs={}, docs={}, last_updated="")
        engine = MatchingEngine(temp_index)

        # 키워드 추출 (매칭 엔진 로직 재사용)
        all_text = f"{parsed_md.goal} {parsed_md.raw_notes}"
        all_files = (parsed_md.files_to_create or []) + (parsed_md.files_to_update or [])
        for file in all_files:
            all_text += f" {file}"

        from .md_parser import MDParser

        parser = MDParser()
        keywords = parser.extract_keywords(all_text)

        predicted_deps = engine._predict_dependencies_from_keywords(keywords)
        dependencies.extend(predicted_deps)

        # 중복 제거 및 필터링
        unique_deps = list(set(dependencies))
        # 불필요한 내부 의존성 필터링
        filtered_deps = [dep for dep in unique_deps if not dep.startswith("internal")]

        return filtered_deps[:10]  # 최대 10개

    def _generate_acceptance_criteria(self, parsed_md: ParsedMD) -> list[str]:
        """승인 기준 자동 생성"""
        criteria = []

        # 기본 기준
        criteria.append("요구사항과 동작이 정확히 일치")
        criteria.append("관련 게이트 통과(lint/type-check/tests)")
        criteria.append("최소 변경(불필요한 포맷/리팩터 없음)")

        # 파일별 기준
        if parsed_md.files_to_create:
            criteria.append(f"새 파일 {len(parsed_md.files_to_create)}개 정상 생성")

        if parsed_md.files_to_update:
            criteria.append(f"기존 파일 {len(parsed_md.files_to_update)}개 정상 수정")

        # 제약사항 기준
        if parsed_md.constraints:
            criteria.append("모든 제약사항 준수")

        return criteria

    def _write_ticket_file(self, ticket_file: Path, ticket_data: dict):
        """티켓 파일 작성"""
        content = self._format_ticket_content(ticket_data)

        with open(ticket_file, "w", encoding="utf-8") as f:
            f.write(content)

    def _format_ticket_content(self, data: dict) -> str:
        """티켓 파일 내용 포맷팅"""
        content = f"""# 🎫 {data["id"]}: {data["title"]}

**우선순위**: {data["priority"].upper()}
**상태**: {data["status"].upper()}
**담당**: 자동 할당
**복잡도**: {data["complexity"]}/10
**Trinity Score**: {data["trinity_score"]["total"]:.1f}/100

## 🎯 목표 (Goal)

{data["goal"]}

## 📋 작업 내용

### 파일 작업
"""

        # 파일 생성
        if data["files_to_create"]:
            content += "\n**생성할 파일:**\n"
            for file in data["files_to_create"]:
                content += f"- {file}\n"

        # 파일 수정
        if data["files_to_update"]:
            content += "\n**수정할 파일:**\n"
            for file in data["files_to_update"]:
                content += f"- {file}\n"

        # 원본 노트
        if data["raw_notes"]:
            content += f"""
### 상세 내용

{data["raw_notes"]}
"""

        # 제약사항
        if data["constraints"]:
            content += """
### 제약사항
"""
            for constraint in data["constraints"]:
                content += f"- {constraint}\n"

        # 매칭 결과
        if data["best_match"]:
            content += f"""
## 🔍 기존 구현 매칭

**최고 매칭**: `{data["best_match"]["module"]}`
**유사도**: {data["best_match"]["similarity"]:.2f}
**매칭 이유**: {data["best_match"]["reason"]}
"""

        # 추천사항
        if data["recommendations"]:
            content += """
## 💡 추천사항
"""
            for rec in data["recommendations"]:
                content += f"- {rec}\n"

        # Trinity Score 상세
        content += f"""
## 📊 Trinity Score 상세

- **眞 (Truth)**: {data["trinity_score"]["truth"]:.1f} - 기술적 정확성
- **善 (Goodness)**: {data["trinity_score"]["goodness"]:.1f} - 윤리·안정성
- **美 (Beauty)**: {data["trinity_score"]["beauty"]:.1f} - 단순함·우아함
- **孝 (Serenity)**: {data["trinity_score"]["serenity"]:.1f} - 형님 마찰 제거
- **永 (Eternity)**: {data["trinity_score"]["eternity"]:.1f} - 지속성·문서화

**총점**: {data["trinity_score"]["total"]:.1f}/100
"""

        # 의존성
        if data["estimated_dependencies"]:
            content += """
## 🔗 예상 의존성
"""
            for dep in data["estimated_dependencies"][:5]:  # 상위 5개만
                content += f"- {dep}\n"

        # 승인 기준
        content += """
## ✅ Acceptance Criteria
"""
        for criterion in data["acceptance_criteria"]:
            content += f"- [ ] {criterion}\n"

        # 작업 로그
        content += f"""
## 📝 작업 로그

- **시작일**: {data["created_at"][:10]}
- **예상 소요시간**: {self._estimate_duration(data["complexity"])}
- **Trinity Score**: {data["trinity_score"]["total"]:.1f}/100

---
*자동 생성됨: MD→티켓 자동화 시스템*
"""

        return content

    def _estimate_duration(self, complexity: int) -> str:
        """복잡도를 기반으로 예상 소요시간 추정"""
        if complexity <= 3:
            return "2-4시간"
        elif complexity <= 6:
            return "4-8시간"
        elif complexity <= 8:
            return "1-2일"
        else:
            return "2-3일"

    def _update_tickets_md(self, ticket_data: dict):
        """TICKETS.md 파일 업데이트"""
        if not self.tickets_md.exists():
            # 새 파일 생성
            content = self._create_initial_tickets_md()
        else:
            # 기존 파일 읽기
            with open(self.tickets_md, encoding="utf-8") as f:
                content = f.read()

        # 새 티켓 추가
        new_entry = self._format_ticket_entry(ticket_data)

        # 티켓 목록 섹션 찾기
        lines = content.split("\n")
        ticket_list_start = -1

        for i, line in enumerate(lines):
            if line.startswith("## 🎫 티켓 목록") or line.startswith("## 티켓 목록"):
                ticket_list_start = i + 1
                break

        if ticket_list_start == -1:
            # 티켓 목록 섹션이 없으면 추가
            content += "\n## 🎫 티켓 목록\n\n"
            content += new_entry
        else:
            # 기존 티켓 목록에 추가
            lines.insert(ticket_list_start, new_entry)
            content = "\n".join(lines)

        # 파일 저장
        with open(self.tickets_md, "w", encoding="utf-8") as f:
            f.write(content)

    def _create_initial_tickets_md(self) -> str:
        """초기 TICKETS.md 내용 생성"""
        return """# 🎫 티켓 시스템

AFO 왕국의 작업 관리 시스템입니다.

## 🎯 개요

- **총 티켓 수**: 자동 계산
- **진행률**: 자동 계산
- **Trinity Score 평균**: 자동 계산

## 🎫 티켓 목록

"""

    def _format_ticket_entry(self, ticket_data: dict) -> str:
        """티켓 목록용 엔트리 포맷팅"""
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(
            ticket_data["priority"], "⚪"
        )

        status_emoji = {
            "pending": "⏳",
            "in_progress": "🔄",
            "completed": "✅",
            "cancelled": "❌",
            "deferred": "⏯️",
        }.get(ticket_data["status"], "❓")

        return (
            f"- {priority_emoji} {status_emoji} **{ticket_data['id']}**: {ticket_data['title']}\n"
            f"  - 복잡도: {ticket_data['complexity']}/10, Trinity: {ticket_data['trinity_score']['total']:.1f}\n"
            f"  - 생성일: {ticket_data['created_at'][:10]}\n\n"
        )


def main():
    """CLI 테스트"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python ticket_generator.py <md_file>")
        return

    md_file = sys.argv[1]

    try:
        # MD 파싱
        from .matching_engine import MatchingEngine
        from .md_parser import MDParser
        from .skeleton_index import SkeletonIndexer

        with open(md_file, encoding="utf-8") as f:
            content = f.read()

        # 파싱
        parser = MDParser()
        parsed_md = parser.parse_md(content)

        # 골격 인덱스
        indexer = SkeletonIndexer()
        try:
            skeleton_index = indexer.load_index()
        except:
            skeleton_index = indexer.scan_folders()
            indexer.save_index(skeleton_index)

        # 매칭
        engine = MatchingEngine(skeleton_index)
        matching_result = engine.find_candidates(parsed_md)

        # 티켓 생성
        generator = TicketGenerator()
        ticket_id = generator.generate_ticket(parsed_md, matching_result)

        print(f"티켓 생성 완료: {ticket_id}")
        print(f"파일 위치: tickets/{ticket_id}.md")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
