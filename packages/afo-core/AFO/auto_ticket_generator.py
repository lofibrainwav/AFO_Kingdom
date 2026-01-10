#!/usr/bin/env python3
"""
TICKET-101: Auto-Ticket Generator
Phase 25 자율 확장 첫 번째 병기
MD 파일을 스캔 → Context7 검색 → 티켓 자동 생성
"""

import hashlib
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import redis
from loguru import logger
from pydantic import BaseModel, Field

# 왕국 내부 모듈 (실제 경로에 맞게 조정됨)
try:
    from AFO.config.settings import get_settings
    from AFO.context7.client import Context7Client
    from AFO.trinity.metrics import calculate_trinity_impact
except ImportError:
    # Fallback/Mock for standalone execution or testing if modules are missing
    logger.warning("AFO modules not found. Using mocks for bootstrapping.")

    class Context7Client:
        def search(self, query, top_k, min_score_threshold):
            return []

    def calculate_trinity_impact(title, goal, related_docs):
        return {"overall": 0.0, "details": "Mock impact"}

    class Settings:
        REDIS_HOST = "localhost"
        REDIS_PORT = 6379
        PROJECT_ROOT = os.getcwd()

    def get_settings():
        return Settings()


settings = get_settings()

# Redis 연결 (핫 캐시 전용)
try:
    r = redis.Redis(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True
    )
except Exception:
    logger.warning("Redis connection failed. Caching disabled.")
    r = None

CACHE_TTL = 300  # 5분


class Ticket(BaseModel):
    """자동 생성될 티켓 모델"""

    id: str = Field(..., description="PH25-XXX 형식")
    title: str
    priority: str = Field(..., pattern="^(HIGH|MEDIUM|LOW)$")
    description: str
    goal: str
    trinity_impact: dict[str, Any]  # 眞善美孝永 점수 영향도
    dependencies: list[str] = []
    estimated_hours: float = 4.0
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    status: str = "PENDING"


class AutoTicketGenerator:
    """MD → 티켓 자동 변환 엔진"""

    def __init__(self):
        self.context7 = Context7Client()
        self.base_dir = Path(settings.PROJECT_ROOT) / "docs" / "tickets"
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _compute_ticket_id(self, title: str) -> str:
        """제목 기반 결정론적 ID 생성"""
        hash_obj = hashlib.sha256(title.encode())
        short_hash = hash_obj.hexdigest()[:8]
        return f"PH25-{short_hash.upper()}"

    def _extract_sections(self, md_content: str) -> dict[str, str]:
        """MD 파일에서 주요 섹션 추출"""
        sections = {}
        current_section = None
        content_lines = []

        for line in md_content.splitlines():
            if line.strip().startswith("# "):
                if current_section and content_lines:
                    sections[current_section] = "\n".join(content_lines).strip()
                current_section = line.strip()[2:].strip()
                content_lines = []
            elif current_section:
                content_lines.append(line)

        if current_section and content_lines:
            sections[current_section] = "\n".join(content_lines).strip()

        return sections

    def _search_context7_for_keywords(self, keywords: list[str]) -> list[dict]:
        """Context7에서 관련 문서 검색"""
        if not r:
            return self.context7.search(
                query=" ".join(keywords), top_k=5, min_score_threshold=0.22
            )

        cache_key = f"ctx7:keywords:{':'.join(sorted(keywords))}"
        try:
            cached = r.get(cache_key)
            if cached:
                logger.info("Context7 cache hit")
                return json.loads(cached)
        except Exception:
            pass

        results = self.context7.search(
            query=" ".join(keywords), top_k=5, min_score_threshold=0.22
        )

        # 캐시 저장
        try:
            if r:
                r.setex(cache_key, CACHE_TTL, json.dumps(results))
        except Exception:
            pass

        return results

    def generate_ticket_from_md(
        self, md_path: str, dry_run: bool = True
    ) -> tuple[bool, Ticket | None]:
        """
        핵심 실행 함수
        :param md_path: 입력 .md 파일 경로
        :param dry_run: True면 실제 파일 쓰기 안 함
        :return: (성공여부, 생성된 티켓)
        """
        try:
            path = Path(md_path)
            if not path.exists():
                logger.error(f"파일 없음: {md_path}")
                return False, None

            content = path.read_text(encoding="utf-8")
            sections = self._extract_sections(content)

            # 필수 섹션 체크
            # Relaxed check: if no explicit sections, treat whole file as description
            if not sections:
                title = path.stem.replace("-", " ").title()
                goal = "Parsed from filename"
                description = content[:500]
            else:
                title = sections.get("제목", path.stem.replace("-", " ").title())
                goal = sections.get("GOAL", "")
                description = sections.get("설명", goal[:300] + "...")

            # 키워드 추출 → Context7 검색
            keywords = re.findall(r"[A-Za-z0-9_-]{4,}", title + " " + goal)
            keywords = list(set(keywords))[:8]  # 최대 8개
            related_docs = self._search_context7_for_keywords(keywords)

            # Trinity 영향도 계산
            trinity_impact = calculate_trinity_impact(
                title=title, goal=goal, related_docs=related_docs
            )

            ticket = Ticket(
                id=self._compute_ticket_id(title),
                title=title,
                priority=(
                    "HIGH" if trinity_impact.get("overall", 0) > 0.85 else "MEDIUM"
                ),
                description=description,
                goal=goal,
                trinity_impact=trinity_impact,
                dependencies=(
                    [doc["file"] for doc in related_docs[:3]] if related_docs else []
                ),
            )

            # Dry Run 모드면 여기서 끝
            if dry_run:
                logger.info(
                    f"[DRY_RUN] 티켓 생성 준비 완료: {ticket.id} - {ticket.title}"
                )
                return True, ticket

            # 실제 저장 (WET)
            ticket_path = self.base_dir / f"{ticket.id}.json"
            ticket_path.write_text(ticket.model_dump_json(indent=2), encoding="utf-8")
            logger.success(f"티켓 생성 완료: {ticket_path}")

            return True, ticket

        except Exception as e:
            logger.exception(f"티켓 생성 실패: {md_path}")
            return False, None


# CLI 진입점 (one-copy-paste용)
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Phase 25 - Auto Ticket Generator")
    parser.add_argument("md_file", type=str, help="처리할 .md 파일 경로")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="실행하지 않고 시뮬레이션만",
    )
    parser.add_argument(
        "--no-dry-run", dest="dry_run", action="store_false", help="실제 실행"
    )

    args = parser.parse_args()

    generator = AutoTicketGenerator()
    success, ticket = generator.generate_ticket_from_md(
        args.md_file, dry_run=args.dry_run
    )

    if success and ticket:
        print("\n" + "=" * 60)
        print(f"생성된 티켓 (ID: {ticket.id})")
        print(f"제목     : {ticket.title}")
        print(f"우선순위 : {ticket.priority}")
        print(f"Trinity 영향도 : {ticket.trinity_impact}")
        print("=" * 60 + "\n")
    else:
        print("티켓 생성 실패 또는 DRY_RUN 모드")
