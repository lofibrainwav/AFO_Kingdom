#!/usr/bin/env python3
"""Context7 MCP Module
지식 그래프 기반 컨텍스트 검색 및 주입을 위한 MCP 도구
"""

import logging
import re
from pathlib import Path
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
        """지식 베이스 로드 (Metadata JSON 기반 동적 로딩)"""
        try:
            import os

            # Repo Root 찾기 (trinity-os 위치 기준)
            base_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
            )
            repo_root = Path(base_path)

            # 1. Metadata Load
            # Import local helper (Serenity)
            try:
                from context7_metadata import inject_meta_header, load_context7_metadata
            except ImportError:
                # Fallback for when running from different CWD
                try:
                    from trinity_os.servers.context7_metadata import (
                        inject_meta_header,
                        load_context7_metadata,
                    )
                except ImportError:
                    logger.error("Failed to import context7_metadata helper")
                    raise

            meta_map = load_context7_metadata(repo_root)

            # Default fallback files if metadata invalid ensuring Eternity
            files_to_load = list(meta_map.keys())
            if not files_to_load:
                logger.warning("Metadata empty/missing. Falling back to default list.")
                files_to_load = [
                    "AGENTS.md",
                    "docs/AFO_ROYAL_LIBRARY.md",
                    "docs/MCP_TOOLS_COMPLETE_DEFINITION.md",
                    "docs/SKILLS_REGISTRY_REFERENCE.md",
                ]
=======

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
>>>>>>> wip/ph20-01-post-work

            loaded_count = 0
            for rel_path in files_to_load:
                full_path = repo_root / rel_path
                if full_path.exists():
                    try:
                        content = full_path.read_text(encoding="utf-8", errors="replace")
                        meta = meta_map.get(rel_path)

                        doc_id = f"doc_{len(self.knowledge_base)}"
                        doc_type = "document"
                        title = full_path.name

                        if meta:
                            # Inject Header (Truth & Richness)
                            content = inject_meta_header(meta, content)
                            # Update Attributes from Metadata
                            doc_type = meta.type
                            title = (
                                meta.description[:50] if meta.description else full_path.name
                            )  # Use description start as title if available

                        self.knowledge_base.append({
                            "id": doc_id,
                            "type": doc_type,
                            "source": str(rel_path),
                            "content": content,
                            "title": title,
                            "keywords": self._extract_keywords(content),
                            "metadata": {
                                "category": meta.category if meta else None,
                                "tags": meta.tags if meta else [],
                                "description": meta.description if meta else None,
                                "keywords": meta.keywords if meta else [],
                            },
                        })
                        loaded_count += 1
                    except Exception as e:
                        logger.warning("Failed to read %s: %s", rel_path, e)
                else:
                    logger.warning("File not found: %s", rel_path)

            logger.info("Loaded %s items via Metadata Driven Loading", loaded_count)

            # 2. Add Core Knowledge (In-Memory)
            self._add_core_knowledge()

            # 3. Build Index
            self._build_index()
            logger.info(f"Knowledge base initialized with {len(self.knowledge_base)} items")

        except Exception as e:
            logger.error("Failed to load knowledge base: %s", e)
            raise

    def _load_document(self, filepath: str) -> None:
<<<<<<< HEAD
        """Deprecated: Logic moved to _load_knowledge_base"""
=======
        """문서 파일 로드"""
        try:
            path = Path(filepath)
            if path.exists():
                content = path.read_text(encoding="utf-8")
                self.knowledge_base.append(
                    {
                        "id": f"doc_{len(self.knowledge_base)}",
                        "type": "document",
                        "source": filepath,
                        "content": content,
                        "title": path.name,
                        "keywords": self._extract_keywords(content),
                    }
                )
            else:
                logger.warning(f"Document not found: {filepath}")
        except Exception as e:
            logger.error(f"Failed to load document {filepath}: {e}")
>>>>>>> wip/ph20-01-post-work

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
                "keywords": ["trinity", "철학", "5기둥", "眞善美孝永", "philosophy"],
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
                "keywords": ["mcp", "model context protocol", "json-rpc", "cursor", "ecosystem"],
            },
            {
                "id": "skills_registry",
                "type": "technical",
                "title": "Skills Registry 시스템 (19개 스킬 체계)",
                "content": """
                AFO Skills Registry 상세 사양:
                - 총 19개 스킬, 9개 카테고리로 분류
                - Strategic Command: skill_005_strategy_engine, skill_010_family_persona
                - RAG Systems: skill_002_ultimate_rag, skill_013_obsidian_librarian
                - Workflow Automation: 3개 스킬 (task_breakdown, orchestrator, expand_loop)
                - Health Monitoring: 3개 스킬 (system_health, trinity_monitor, error_detector)
                - Memory Management: skill_009_memory_optimizer
                - Analysis Evaluation: 4개 스킬 (code_quality, security_scan, performance_eval, user_experience)
                - Integration: 3개 스킬 (api_integration, data_pipeline, notification_system)
                - Metacognition: skill_019_self_learning
                - 각 스킬별 Trinity Score 평가 (眞善美孝永)
                - 실행 모드: SYNC, ASYNC, STREAMING, BACKGROUND
                - DRY_RUN 모드 및 안전 게이트 지원
                """,
<<<<<<< HEAD
                "keywords": [
                    "skills",
                    "registry",
                    "trinity",
                    "dry_run",
                    "실행",
                    "19개",
                    "카테고리",
                    "strategic",
                    "rag",
                    "workflow",
                    "monitoring",
                    "memory",
                    "analysis",
                    "integration",
                    "metacognition",
                ],
            },
            {
                "id": "mcp_protocol",
                "type": "technical",
                "title": "MCP Protocol (Model Context Protocol)",
                "content": """
                Model Context Protocol (MCP) 사양:
                - JSON-RPC 2.0 over STDIO 기반 통신 프로토콜
                - AI 모델과 도구 사이의 표준화된 인터페이스
                - 도구 호출, 결과 반환, 에러 처리 표준화
                - 안전한 샌드박스 환경에서 도구 실행
                - Cursor IDE, Claude Desktop 등 지원
                - AFO 왕국: 14개 핵심 도구 + 확장 가능성
                """,
                "keywords": [
                    "mcp",
                    "protocol",
                    "json-rpc",
                    "stdio",
                    "cursor",
                    "model context protocol",
                    "도구",
                    "tools",
                    "interface",
                ],
=======
                "keywords": ["skills", "registry", "trinity", "dry_run", "실행"],
>>>>>>> wip/ph20-01-post-work
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
                "keywords": ["sequential", "thinking", "단계별", "추론", "methodology"],
            },
        ]

        self.knowledge_base.extend(core_knowledge)

    def _extract_keywords(self, content: str) -> list[str]:
        """콘텐츠에서 키워드 추출 (개선된 버전)"""
        keywords = set()

        # 기본 키워드 리스트 (AFO 왕국 관련 추가)
        base_keywords = [
            # 기존 키워드들
            "trinity",
            "mcp",
            "skills",
            "api",
            "backend",
            "frontend",
            "database",
            "redis",
            "postgresql",
            "docker",
            "kubernetes",
            "monitoring",
            "metrics",
            "logging",
            "security",
            "auth",
            "cache",
            "session",
            "router",
            "middleware",
            "validation",
            "error",
            "handling",
            "async",
            "concurrency",
            "performance",
            "testing",
            "ci",
            "cd",
            "deployment",
            "scaling",
            # AFO 왕국 관련 키워드 추가
            "afo",
            "kingdom",
            "philosophy",
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
            "chancellor",
            "agents",
            "cursor",
            "claude",
            "codex",
            "grok",
            "sequential",
            "thinking",
            "context7",
            "orchestration",
        ]

        content_lower = content.lower()

        # 기본 키워드 매칭
        for keyword in base_keywords:
            if keyword in content_lower:
                keywords.add(keyword)

        # 동적 키워드 추출 - 단어 단위로 분리
        words = re.findall(r"\b\w+\b", content_lower)
        significant_words = [
            word
            for word in words
            if len(word) > 3
            and word
            not in {
                "that",
                "with",
                "have",
                "this",
                "will",
                "your",
                "from",
                "they",
                "know",
                "want",
                "been",
                "good",
                "much",
                "some",
                "time",
                "very",
                "when",
                "come",
                "here",
                "just",
                "like",
                "long",
                "make",
                "many",
                "over",
                "such",
                "take",
                "than",
                "them",
                "well",
                "were",
                "what",
                "where",
                "which",
                "while",
                "who",
                "why",
                "would",
            }
        ]

        # 의미 있는 단어들 추가 (최대 10개)
        for word in significant_words[:10]:
            if len(word) >= 4:  # 4글자 이상만
                keywords.add(word)

        # 기존 패턴 추출 유지
        patterns = [
            r"#+\s*([^\n]+)",  # 헤더들
            r"\*\*([^*]+)\*\*",  # 볼드 텍스트
            r"`([^`]+)`",  # 코드
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches[:5]:  # 최대 5개로 줄임
                clean_match = match.strip().lower()
                if len(clean_match) > 2:
                    keywords.add(clean_match)

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
<<<<<<< HEAD
        """
        쿼리에 기반한 컨텍스트 검색
=======
        """쿼리에 기반한 컨텍스트 검색
>>>>>>> wip/ph20-01-post-work

        Args:
            query: 검색 쿼리
            domain: 검색 도메인 (general, technical, philosophy 등)

        Returns:
            관련 컨텍스트들
<<<<<<< HEAD
=======

>>>>>>> wip/ph20-01-post-work
        """
        # 쿼리 분석
        query_keywords = self._extract_keywords(query)
        query_lower = query.lower()

        # 관련 문서 찾기
        _relevant_docs = []
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
<<<<<<< HEAD
            results.append({
                "id": item["id"],
                "title": item["title"],
                "type": item["type"],
                "relevance_score": score,
                "preview": item["content"][:200] + "..."
                if len(item["content"]) > 200
                else item["content"],
                "source": item.get("source", "knowledge_base"),
                "keywords": item.get("keywords", []),
            })
=======
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
>>>>>>> wip/ph20-01-post-work

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
                "knowledge_base_size": len(self.knowledge_base),
            },
        }

    def add_knowledge(self, knowledge_item: dict[str, Any]) -> str:
        """새로운 지식 항목 추가"""
        knowledge_item["id"] = f"custom_{len(self.knowledge_base)}"
        knowledge_item["keywords"] = self._extract_keywords(
            knowledge_item.get("content", "") + " " + knowledge_item.get("title", "")
        )

        self.knowledge_base.append(knowledge_item)

        # 색인 업데이트
        self._build_index()

        return knowledge_item["id"]

    def get_knowledge_stats(self) -> dict[str, Any]:
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
            "indexed_keywords": len(self.knowledge_index),
        }
