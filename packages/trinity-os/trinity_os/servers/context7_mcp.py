#!/usr/bin/env python3
"""Context7 MCP Module
지식 그래프 기반 컨텍스트 검색 및 주입을 위한 MCP 도구
"""

import logging
from typing import Any


logger = logging.getLogger(__name__)


class Context7MCP:
    """Context7 MCP - 지식 그래프 기반 컨텍스트 관리
    AFO 왕국의 지식 베이스에서 관련 컨텍스트를 검색하고 주입
    """

    def __init__(self):
        self.knowledge_base: list[dict[str, Any]] = []
        self.knowledge_index: dict[str, set[int]] = {}
        self._load_knowledge_base()

    def _load_knowledge_base(self) -> None:
        """지식 베이스 로드"""
        try:
            import os

            # trinity-os 폴더에서 AFO_Kingdom 루트까지 올라감
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

            knowledge_sources = [
                os.path.join(base_path, "AGENTS.md"),
                os.path.join(base_path, "docs/AFO_ROYAL_LIBRARY.md"),
                os.path.join(base_path, "docs/AFO_CHANCELLOR_GRAPH_SPEC.md"),
                os.path.join(base_path, "docs/AFO_EVOLUTION_LOG.md"),
                os.path.join(base_path, "docs/AFO_FRONTEND_ARCH.md"),
                os.path.join(base_path, "docs/CURSOR_MCP_SETUP.md"),
            ]

            loaded_count = 0
            for source_path in knowledge_sources:
                if os.path.exists(source_path):
                    try:
                        with open(source_path, encoding="utf-8", errors="replace") as f:
                            content = f.read()

                        doc_id = f"doc_{len(self.knowledge_base)}"
                        self.knowledge_base.append(
                            {
                                "id": doc_id,
                                "type": "document",
                                "source": source_path,
                                "content": content,
                                "title": os.path.basename(source_path),
                                "keywords": self._extract_keywords(content),
                            }
                        )
                        loaded_count += 1
                    except Exception as e:
                        logger.warning("Failed to read %s: %s", source_path, e)

            logger.info("Loaded %s items", loaded_count)
            self._add_core_knowledge()
            self._build_index()

        except Exception as e:
            logger.error("Failed to load knowledge base: %s", e)
            raise

    def _add_core_knowledge(self) -> None:
        """핵심 지식 항목들 추가"""
        core_knowledge = [
            {
                "id": "trinity_philosophy",
                "type": "philosophy",
                "title": "Trinity 철학 (眞善美孝永)",
                "content": "AFO 왕국의 5기둥 철학: 眞 (Truth), 善 (Goodness), 美 (Beauty), 孝 (Serenity), 永 (Eternity)",
                "keywords": ["trinity", "철학", "5기둥", "眞善美孝永", "philosophy"],
            },
        ]
        self.knowledge_base.extend(core_knowledge)

    def _extract_keywords(self, content: str) -> list[str]:
        """콘텐츠에서 키워드 추출"""
        keywords = set()

        base_keywords = [
            "trinity",
            "mcp",
            "skills",
            "api",
            "backend",
            "frontend",
            "afo",
            "kingdom",
            "眞",
            "善",
            "美",
            "孝",
            "永",
            "truth",
            "goodness",
            "beauty",
            "serenity",
            "eternity",
        ]

        content_lower = content.lower()
        for keyword in base_keywords:
            if keyword in content_lower:
                keywords.add(keyword)

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

    def retrieve_context(self, query: str, domain: str = "general") -> dict[str, Any]:
        """쿼리에 기반한 컨텍스트 검색"""
        query_keywords = self._extract_keywords(query)
        scores = {}

        for keyword in query_keywords:
            if keyword in self.knowledge_index:
                for doc_idx in self.knowledge_index[keyword]:
                    scores[doc_idx] = scores.get(doc_idx, 0) + 1

        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]
        results = []
        for doc_idx, score in sorted_docs:
            item = self.knowledge_base[doc_idx]
            results.append(
                {
                    "id": item["id"],
                    "title": item["title"],
                    "type": item["type"],
                    "relevance_score": score,
                    "preview": item["content"][:200] + "..." if len(item["content"]) > 200 else item["content"],
                    "source": item.get("source", "knowledge_base"),
                    "keywords": item.get("keywords", []),
                }
            )

        return {
            "query": query,
            "domain": domain,
            "total_results": len(results),
            "results": results,
            "metadata": {
                "search_method": "keyword_matching",
                "knowledge_base_size": len(self.knowledge_base),
            },
        }

    def get_knowledge_stats(self) -> dict[str, Any]:
        """지식 베이스 통계 반환"""
        types = {}
        for item in self.knowledge_base:
            item_type = item.get("type", "unknown")
            types[item_type] = types.get(item_type, 0) + 1

        return {
            "total_items": len(self.knowledge_base),
            "types": types,
            "indexed_keywords": len(self.knowledge_index),
        }
