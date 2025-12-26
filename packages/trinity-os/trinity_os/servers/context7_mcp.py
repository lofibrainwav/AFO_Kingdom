#!/usr/bin/env python3
"""
Context7 MCP Module
지식 그래프 기반 컨텍스트 검색 및 주입을 위한 MCP 도구
"""

import json
import logging
from typing import Dict, Any, List, Optional, Set
from pathlib import Path
import re

logger = logging.getLogger(__name__)

class Context7MCP:
    """
    Context7 MCP - 지식 그래프 기반 컨텍스트 관리
    AFO 왕국의 지식 베이스에서 관련 컨텍스트를 검색하고 주입
    """

    def __init__(self):
        self.knowledge_base: List[Dict[str, Any]] = []
        self.knowledge_index: Dict[str, Set[int]] = {}
        self._load_knowledge_base()

    def _load_knowledge_base(self) -> None:
        """지식 베이스 로드"""
        try:
            # AFO 왕국의 핵심 문서들 로드 - 절대 경로로 찾기
            import os
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))

            knowledge_sources = [
                os.path.join(base_path, "AGENTS.md"),
                os.path.join(base_path, "docs/AFO_ROYAL_LIBRARY.md"),
                os.path.join(base_path, "docs/AFO_CHANCELLOR_GRAPH_SPEC.md"),
                os.path.join(base_path, "docs/AFO_EVOLUTION_LOG.md"),
                os.path.join(base_path, "docs/AFO_FRONTEND_ARCH.md"),
                os.path.join(base_path, "docs/CURSOR_MCP_SETUP.md")
            ]

            loaded_count = 0
            for source in knowledge_sources:
                if self._load_document(source):
                    loaded_count += 1

            logger.info(f"Loaded {loaded_count} out of {len(knowledge_sources)} knowledge sources")

            # 추가 지식 항목들
            self._add_core_knowledge()

            # 색인 구축
            self._build_index()
            logger.info(f"Knowledge base initialized with {len(self.knowledge_base)} items")

        except Exception as e:
            logger.error(f"Failed to load knowledge base: {e}")
            raise

    def _load_document(self, filepath: str) -> None:
        """문서 파일 로드"""
        try:
            path = Path(filepath)
            if path.exists():
                content = path.read_text(encoding='utf-8')
                self.knowledge_base.append({
                    "id": f"doc_{len(self.knowledge_base)}",
                    "type": "document",
                    "source": filepath,
                    "content": content,
                    "title": path.name,
                    "keywords": self._extract_keywords(content)
                })
            else:
                logger.warning(f"Document not found: {filepath}")
        except Exception as e:
            logger.error(f"Failed to load document {filepath}: {e}")

    def _add_core_knowledge(self) -> None:
        """핵심 지식 항목들 추가"""
        core_knowledge = [
            {
                "id": "trinity_philosophy",
                "type": "philosophy",
                "title": "Trinity 철학 (眞善美孝永)",
                "content": """
                AFO 왕국의 5기둥 철학:
                - 眞 (Truth): 기술적 확실성, 타입 안전성, 테스트 무결성
                - 善 (Goodness): 윤리·안정성, 비용 최적화, 안전 게이트
                - 美 (Beauty): 구조적 단순함, 모듈화, 일관된 API/UI
                - 孝 (Serenity): 평온·연속성, 인지 부하 최소화
                - 永 (Eternity): 재현 가능성, 문서화, 버전·결정 기록
                """,
                "keywords": ["trinity", "철학", "5기둥", "眞善美孝永", "philosophy"]
            },
            {
                "id": "mcp_ecosystem",
                "type": "technical",
                "title": "MCP 생태계",
                "content": """
                Model Context Protocol (MCP) 생태계:
                - JSON-RPC 2.0 over STDIO 기반 통신
                - Cursor IDE 통합 지원
                - 도구 기반 확장성
                - 안전한 실행 환경
                """,
                "keywords": ["mcp", "model context protocol", "json-rpc", "cursor", "ecosystem"]
            },
            {
                "id": "skills_registry",
                "type": "technical",
                "title": "Skills Registry 시스템",
                "content": """
                AFO Skills Registry:
                - 31개 지능적 기능 제공
                - Trinity Score 기반 실행
                - DRY_RUN 모드 지원
                - 실시간 상태 모니터링
                """,
                "keywords": ["skills", "registry", "trinity", "dry_run", "실행"]
            },
            {
                "id": "sequential_thinking",
                "type": "methodology",
                "title": "Sequential Thinking 방법론",
                "content": """
                단계별 사고 방법론:
                - 체계적인 문제 해결
                - 진실성과 평온성 평가
                - 사고 과정 기록 및 분석
                - Trinity Score 기반 품질 관리
                """,
                "keywords": ["sequential", "thinking", "단계별", "추론", "methodology"]
            }
        ]

        self.knowledge_base.extend(core_knowledge)

    def _extract_keywords(self, content: str) -> List[str]:
        """콘텐츠에서 키워드 추출"""
        keywords = set()

        # 한글 키워드 추출
        korean_keywords = [
            "trinity", "mcp", "skills", "api", "backend", "frontend",
            "database", "redis", "postgresql", "docker", "kubernetes",
            "monitoring", "metrics", "logging", "security", "auth",
            "cache", "session", "router", "middleware", "validation",
            "error", "handling", "async", "concurrency", "performance",
            "testing", "ci", "cd", "deployment", "scaling"
        ]

        # 영어 키워드 추출
        english_keywords = [
            "trinity", "mcp", "skills", "api", "backend", "frontend",
            "database", "redis", "postgresql", "docker", "kubernetes",
            "monitoring", "metrics", "logging", "security", "auth",
            "cache", "session", "router", "middleware", "validation",
            "error", "handling", "async", "concurrency", "performance",
            "testing", "ci", "cd", "deployment", "scaling"
        ]

        content_lower = content.lower()

        for keyword in korean_keywords + english_keywords:
            if keyword in content_lower:
                keywords.add(keyword)

        # 주요 용어들 추출
        patterns = [
            r'#+\s*([^\n]+)',  # 헤더들
            r'\*\*([^*]+)\*\*',  # 볼드 텍스트
            r'`([^`]+)`',  # 코드
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches[:10]:  # 최대 10개까지만
                if len(match.strip()) > 2:
                    keywords.add(match.strip().lower())

        return list(keywords)

    def _build_index(self) -> None:
        """지식 베이스 색인 구축"""
        self.knowledge_index = {}

        for idx, item in enumerate(self.knowledge_base):
            keywords = item.get("keywords", [])
            for keyword in keywords:
                if keyword not in self.knowledge_index:
                    self.knowledge_index[keyword] = set()
                self.knowledge_index[keyword].add(idx)

    def retrieve_context(self, query: str, domain: str = "general") -> Dict[str, Any]:
        """
        쿼리에 기반한 컨텍스트 검색

        Args:
            query: 검색 쿼리
            domain: 검색 도메인 (general, technical, philosophy 등)

        Returns:
            관련 컨텍스트들
        """

        # 쿼리 분석
        query_keywords = self._extract_keywords(query)
        query_lower = query.lower()

        # 관련 문서 찾기
        relevant_docs = []
        scores = {}

        for keyword in query_keywords:
            if keyword in self.knowledge_index:
                for doc_idx in self.knowledge_index[keyword]:
                    if doc_idx not in scores:
                        scores[doc_idx] = 0
                    scores[doc_idx] += 1

        # 추가 텍스트 매칭
        for idx, item in enumerate(self.knowledge_base):
            content_lower = item.get("content", "").lower()
            title_lower = item.get("title", "").lower()

            if query_lower in content_lower or query_lower in title_lower:
                if idx not in scores:
                    scores[idx] = 0
                scores[idx] += 2  # 텍스트 매칭은 더 높은 점수

        # 도메인 필터링
        if domain != "general":
            filtered_scores = {}
            for idx, score in scores.items():
                item = self.knowledge_base[idx]
                if item.get("type") == domain:
                    filtered_scores[idx] = score
            scores = filtered_scores

        # 상위 결과 추출 (최대 5개)
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]

        results = []
        for doc_idx, score in sorted_docs:
            item = self.knowledge_base[doc_idx]
            results.append({
                "id": item["id"],
                "title": item["title"],
                "type": item["type"],
                "relevance_score": score,
                "preview": item["content"][:200] + "..." if len(item["content"]) > 200 else item["content"],
                "source": item.get("source", "knowledge_base"),
                "keywords": item.get("keywords", [])
            })

        # Trinity Score 평가
        truth_impact = min(len(results) * 0.1, 1.0)  # 결과 수에 따른 진실성
        serenity_impact = 0.8 if results else 0.2  # 컨텍스트 제공으로 인한 평온성

        return {
            "query": query,
            "domain": domain,
            "total_results": len(results),
            "results": results,
            "metadata": {
                "truth_impact": truth_impact,
                "serenity_impact": serenity_impact,
                "search_method": "keyword_matching",
                "knowledge_base_size": len(self.knowledge_base)
            }
        }

    def add_knowledge(self, knowledge_item: Dict[str, Any]) -> str:
        """새로운 지식 항목 추가"""
        knowledge_item["id"] = f"custom_{len(self.knowledge_base)}"
        knowledge_item["keywords"] = self._extract_keywords(
            knowledge_item.get("content", "") + " " + knowledge_item.get("title", "")
        )

        self.knowledge_base.append(knowledge_item)

        # 색인 업데이트
        self._build_index()

        return knowledge_item["id"]

    def get_knowledge_stats(self) -> Dict[str, Any]:
        """지식 베이스 통계 반환"""
        types = {}
        sources = {}

        for item in self.knowledge_base:
            item_type = item.get("type", "unknown")
            types[item_type] = types.get(item_type, 0) + 1

            source = item.get("source", "unknown")
            sources[source] = sources.get(source, 0) + 1

        return {
            "total_items": len(self.knowledge_base),
            "types": types,
            "sources": sources,
            "indexed_keywords": len(self.knowledge_index)
        }