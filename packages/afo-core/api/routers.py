"""
AFO Kingdom API Router Registration (아름다운 코드 적용)

Trinity Score 기반 아름다운 코드로 구현된 중앙 집중식 라우터 등록 시스템.
모듈화, 타입 안전성, 문서화를 통해 유지보수성과 확장성을 보장.

Author: AFO Kingdom Development Team
Date: 2025-12-24
Version: 2.0.0 (Beautiful Code Edition)
"""

from __future__ import annotations

import logging

from AFO.api.compat import (aicpa_router, auth_router, budget_router,
                            chancellor_router, chat_router, council_router,
                            education_system_router, finance_router,
                            got_router, grok_stream_router, health_router,
                            learning_log_router, learning_pipeline,
                            matrix_router, modal_data_router,
                            multi_agent_router, n8n_router, personas_router,
                            pillars_router, rag_query_router, root_router,
                            serenity_router, skills_router, ssot_router,
                            strangler_router, streams_router,
                            system_health_router, trinity_policy_router,
                            trinity_sbt_router, users_router, voice_router,
                            wallet_router)
from fastapi import FastAPI

# Strangler Fig compatibility router
try:
    from AFO.api.routers.compat import router as compat_router
except ImportError:
    compat_router = None

logger = logging.getLogger(__name__)


class AFORouterManager:
    """
    AFO Kingdom Router Manager (아름다운 코드 적용)

    Trinity Score 기반 라우터 관리를 통해 체계적이고 아름다운 API 구조를 유지.
    각 라우터 그룹을 별도 메서드로 분리하여 단일 책임 원칙 준수.

    Attributes:
        app: FastAPI 애플리케이션 인스턴스
        registered_routers: 등록된 라우터 수 카운터
    """

    def __init__(self, app: FastAPI) -> None:
        """Initialize router manager with FastAPI app.

        Args:
            app: FastAPI application instance
        """
        self.app = app
        self.registered_routers = 0
        logger.info("AFO Router Manager initialized with beautiful code principles")

    def setup_all_routers(self) -> None:
        """Setup and register all API routers in organized manner.

        Trinity Score: 美 (Beauty) - 체계적이고 아름다운 라우터 구성
        """
        logger.info("Starting router registration process...")

        # Core system routers (highest priority)
        self._register_core_routers()

        # Feature routers (business logic)
        self._register_feature_routers()

        # Phase-specific routers (incremental development)
        self._register_phase_routers()

        # Legacy and compatibility routers (last resort)
        self._register_legacy_routers()

        logger.info(
            f"Router registration completed. Total: {self.registered_routers} routers"
        )

    def _register_core_routers(self) -> None:
        """Register core system routers (Health, Root, Streams).

        Trinity Score: 眞 (Truth) - 시스템 핵심 기능 우선 등록
        """
        logger.debug("Registering core system routers...")

        # Health and root endpoints
        self._safe_register_router(root_router, tags=["Core"])
        self._safe_register_router(health_router, tags=["Core"])

        # Matrix streams (must be mounted before other routers)
        self._safe_register_router(
            streams_router, prefix="/api/stream", tags=["Matrix Stream"]
        )
        self._safe_register_router(
            matrix_router, prefix="/api", tags=["Matrix Stream (Phase 10)"]
        )

    def _register_feature_routers(self) -> None:
        """Register feature-specific routers (Business Logic).

        Trinity Score: 善 (Goodness) - 비즈니스 로직 체계적 구성
        """
        logger.debug("Registering feature routers...")

        # 5 Pillars system
        self._safe_register_router(pillars_router, tags=["5 Pillars"])

        # System health and monitoring
        self._safe_register_router(system_health_router, tags=["System Health"])

        # Multi-agent and AI systems
        self._safe_register_router(multi_agent_router)
        self._safe_register_router(
            got_router, prefix="/api/got", tags=["Graph of Thought"]
        )
        self._safe_register_router(
            n8n_router, prefix="/api/n8n", tags=["N8N Integration"]
        )

        # API and financial systems
        self._safe_register_router(wallet_router, tags=["API Wallet"])
        self._safe_register_router(trinity_policy_router, tags=["trinity"])
        self._safe_register_router(trinity_sbt_router, prefix="/api", tags=["trinity"])

        # User management systems
        self._safe_register_router(users_router, tags=["肝 시스템 - 사용자 관리"])
        self._safe_register_router(auth_router, tags=["心 시스템 - 인증"])

        # Communication systems
        self._safe_register_router(chat_router, prefix="/api/chat", tags=["Chat"])

        # Education and data systems
        self._safe_register_router(
            education_system_router, prefix="/api/education", tags=["Education System"]
        )
        self._safe_register_router(
            modal_data_router, prefix="/api/modal", tags=["Modal Data"]
        )

        # Advanced AI systems
        self._safe_register_router(
            rag_query_router, prefix="/api", tags=["Brain Organ (RAG)"]
        )
        self._safe_register_router(personas_router, tags=["Phase 2: Family Hub OS"])

    def _register_phase_routers(self) -> None:
        """Register phase-specific routers (Incremental Development).

        Trinity Score: 永 (Eternity) - 단계적 개발 지원으로 장기적 유지보수성 확보
        """
        logger.debug("Registering phase-specific routers...")

        # Phase 12-13: Business Intelligence
        self._safe_register_router(budget_router, tags=["Phase 12"])
        self._safe_register_router(
            aicpa_router, prefix="/api", tags=["AICPA Agent Army"]
        )

        # Phase 16-18: Autonomous Learning
        self._safe_register_router(learning_log_router, tags=["Phase 16"])
        self._safe_register_router(grok_stream_router, tags=["Phase 18"])

        # Phase 23-27: Advanced AI
        self._safe_register_router(
            voice_router, prefix="/api", tags=["Voice Interface"]
        )
        self._safe_register_router(
            council_router, prefix="/api", tags=["Council of Minds"]
        )
        self._safe_register_router(
            learning_pipeline, prefix="/api", tags=["AI Self-Improvement"]
        )
        self._safe_register_router(
            serenity_router, prefix="/api", tags=["Serenity (GenUI)"]
        )

        # Philosophical Copilot (眞善美孝永 철학 실시간 모니터링)
        try:
            from AFO.api.routes.philosophical_copilot import \
                router as philosophical_copilot_router

            self._safe_register_router(
                philosophical_copilot_router, tags=["철학적 Copilot"]
            )
        except ImportError:
            logger.warning("Philosophical Copilot Router not available")

        # Chancellor and streaming systems
        self._safe_register_router(chancellor_router, tags=["LangGraph Optimized"])
        try:
            from AFO.api.routes.system_stream import \
                router as system_stream_router

            self._safe_register_router(system_stream_router, tags=["SSE 스트리밍"])
        except ImportError:
            logger.warning("System Stream Router not available")

        # Additional systems
        self._safe_register_router(finance_router)
        self._safe_register_router(ssot_router)

    def _register_legacy_routers(self) -> None:
        """Register legacy and compatibility routers.

        Trinity Score: 孝 (Serenity) - 레거시 호환성으로 마찰 최소화
        """
        logger.debug("Registering legacy routers...")

        # Skills API (Critical for functionality)
        self._register_skills_router()

        # Comprehensive health and monitoring
        self._register_comprehensive_health()

        # Management APIs
        self._register_management_apis()

        # Compatibility routers
        self._register_compatibility_routers()

    def _register_skills_router(self) -> None:
        """Register Skills API router with enhanced error handling."""
        if not skills_router:
            logger.warning("Skills router not available")
            return

        try:
            routes_before = len([r for r in self.app.routes if hasattr(r, "path")])
            self.app.include_router(
                skills_router, prefix="/api/skills", tags=["Skills"]
            )
            routes_after = len([r for r in self.app.routes if hasattr(r, "path")])
            self.registered_routers += routes_after - routes_before
            logger.info(
                f"Skills API registered successfully ({routes_after - routes_before} routes)"
            )
        except Exception as e:
            logger.error(f"Skills router registration failed: {e}")

    def _register_comprehensive_health(self) -> None:
        """Register comprehensive health check router."""
        try:
            from AFO.api.routes.comprehensive_health import \
                router as comprehensive_health_router

            self._safe_register_router(comprehensive_health_router, tags=["Health"])
        except ImportError:
            logger.warning("Comprehensive Health Check Router not available")

    def _register_management_apis(self) -> None:
        """Register management and utility APIs."""
        # MCP Tools, Integrity Check, Git Status
        management_routers = [
            ("AFO.api.routes.mcp_tools", "MCP Tools"),
            ("AFO.api.routes.integrity_check", "Integrity Check"),
            ("AFO.api.routes.git_status", "Git Status"),
        ]

        for module_path, name in management_routers:
            try:
                module = __import__(module_path, fromlist=["router"])
                router = module.router
                self._safe_register_router(router, tags=[name])
            except (ImportError, AttributeError) as e:
                logger.warning(f"{name} router not available: {e}")

    def _register_compatibility_routers(self) -> None:
        """Register compatibility and legacy routers."""
        # Intake API
        try:
            from AFO.afo_soul_engine.routers.intake import \
                router as intake_router

            self._safe_register_router(intake_router, tags=["Intake"])
        except ImportError:
            logger.warning("Intake API router not available")

        # GenUI Engine
        try:
            from AFO.api.routers.gen_ui import router as gen_ui_router

            self._safe_register_router(gen_ui_router, tags=["GenUI"])
        except ImportError:
            logger.warning("GenUI Engine not available")

        # Family Hub
        try:
            from AFO.api.routers.family import router as family_router

            self._safe_register_router(family_router, tags=["Family Hub"])
            self._safe_register_router(
                family_router, prefix="/api", tags=["Family Hub"]
            )
        except ImportError:
            logger.warning("Family Hub router not available")

        # Cache Metrics
        try:
            from AFO.api.routers.cache import router as cache_router

            self._safe_register_router(cache_router, tags=["Cache Metrics"])
        except ImportError:
            logger.warning("Cache Metrics router not available")

        # Julie Royal
        try:
            from AFO.api.routers.julie_royal import \
                router as julie_royal_router

            self._safe_register_router(julie_royal_router, tags=["Julie Royal"])
        except ImportError:
            logger.warning("Julie Royal router not available")

        # Strangler Fig Compatibility
        if compat_router:
            self._safe_register_router(
                compat_router, prefix="/api", tags=["Strangler Fig"]
            )

    def _safe_register_router(
        self, router: object | None, prefix: str = "", tags: list[str] | None = None
    ) -> None:
        """Safely register a router with error handling.

        Args:
            router: Router object to register
            prefix: URL prefix for the router
            tags: Tags for API documentation
        """
        if not router:
            return

        try:
            routes_before = len([r for r in self.app.routes if hasattr(r, "path")])
            if prefix and tags:
                self.app.include_router(router, prefix=prefix, tags=tags)
            elif prefix:
                self.app.include_router(router, prefix=prefix)
            elif tags:
                self.app.include_router(router, tags=tags)
            else:
                self.app.include_router(router)

            routes_after = len([r for r in self.app.routes if hasattr(r, "path")])
            self.registered_routers += routes_after - routes_before

        except Exception as e:
            logger.error(f"Router registration failed: {e}")


# Global function for backward compatibility
def setup_routers(app: FastAPI) -> None:
    """Setup all routers using the beautiful RouterManager.

    Args:
        app: FastAPI application instance
    """
    manager = AFORouterManager(app)
    manager.setup_all_routers()


def _register_core_routers(app: FastAPI) -> None:
    """Register core system routers."""
    # Health and root endpoints
    if root_router:
        app.include_router(root_router)
        print("✅ Root 라우터 등록 완료")

    if health_router:
        app.include_router(health_router)
        print("✅ Health 라우터 등록 완료")

    # Matrix streams (must be mounted before other routers)
    if streams_router:
        app.include_router(streams_router, prefix="/api/stream", tags=["Matrix Stream"])

    if matrix_router:
        app.include_router(
            matrix_router, prefix="/api", tags=["Matrix Stream (Phase 10)"]
        )


def _register_feature_routers(app: FastAPI) -> None:
    """Register feature-specific routers."""
    # 5 Pillars system
    if pillars_router:
        app.include_router(pillars_router, tags=["5 Pillars"])

    # System health
    if system_health_router:
        app.include_router(system_health_router, tags=["System Health"])

    # Multi-agent system
    if multi_agent_router:
        app.include_router(multi_agent_router)
        print("✅ Multi-Agent 라우터 등록 완료")

    # Strangler fig pattern
    if strangler_router:
        app.include_router(
            strangler_router, prefix="/api/strangler", tags=["Strangler Fig"]
        )

    # Graph of Thought
    if got_router:
        app.include_router(got_router, prefix="/api/got", tags=["Graph of Thought"])

    # N8N integration
    if n8n_router:
        app.include_router(n8n_router, prefix="/api/n8n", tags=["N8N Integration"])

    # API Wallet
    if wallet_router:
        app.include_router(wallet_router, tags=["API Wallet"])

    # Trinity systems
    if trinity_policy_router:
        app.include_router(trinity_policy_router, tags=["trinity"])
        print("✅ Trinity Policy API 라우터 등록 완료")

    if trinity_sbt_router:
        app.include_router(trinity_sbt_router, prefix="/api", tags=["trinity"])
        print("✅ Trinity SBT API 라우터 등록 완료")

    # User management
    if users_router:
        app.include_router(users_router)
        print("✅ Users API 라우터 등록 완료 (肝 시스템 - 사용자 관리)")

    if auth_router:
        app.include_router(auth_router)
        print("✅ Auth API 라우터 등록 완료 (心 시스템 - 인증)")

    # Chat API
    if chat_router:
        app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])
        print("✅ Chat API 라우터 등록 완료")

    # Education and modal systems
    if education_system_router:
        app.include_router(
            education_system_router, prefix="/api/education", tags=["Education System"]
        )

    if modal_data_router:
        app.include_router(modal_data_router, prefix="/api/modal", tags=["Modal Data"])

    # Advanced RAG (GraphRAG)
    if rag_query_router:
        app.include_router(rag_query_router, prefix="/api", tags=["Brain Organ (RAG)"])
        print("✅ GraphRAG API 라우터 등록 완료 (Brain Organ)")

    # Personas system
    if personas_router:
        app.include_router(personas_router)
        print(
            "✅ Personas API 라우터 등록 완료 (Phase 2: Family Hub OS - TRINITY-OS 페르소나 통합)"
        )


def _register_phase_routers(app: FastAPI) -> None:
    """Register phase-specific routers."""
    # Phase 12: Budget tracking
    try:
        if budget_router:
            app.include_router(budget_router)
            print("✅ Budget Router 등록 완료 (Phase 12 확장)")
    except Exception as e:
        print(f"⚠️ Budget Router 등록 실패: {e}")

    # Phase 13: AICPA Agent Army
    try:
        if aicpa_router:
            app.include_router(aicpa_router, prefix="/api", tags=["AICPA Agent Army"])
            print("✅ AICPA Router 등록 완료 (Phase 13: 에이전트 군단)")
    except Exception as e:
        print(f"⚠️ AICPA Router 등록 실패: {e}")

    # Phase 16: Autonomous Agents
    try:
        if learning_log_router:
            app.include_router(learning_log_router)
            print("✅ Learning Log Router 등록 완료 (Phase 16-4: 자율 학습 루프)")
    except Exception as e:
        print(f"⚠️ Learning Log Router 등록 실패: {e}")

    # Phase 18: Grok Real-time Stream
    try:
        if grok_stream_router:
            app.include_router(grok_stream_router)
            print("✅ Grok Stream Router 등록 완료 (Phase 18: 왕국의 맥박)")
    except Exception as e:
        print(f"⚠️ Grok Stream Router 등록 실패: {e}")

    # Phase 24: Voice Interface
    try:
        if voice_router:
            app.include_router(voice_router, prefix="/api", tags=["Voice Interface"])
            print("🎙️ Voice Router 등록 완료 (Phase 24: Commander's Voice)")
    except Exception as e:
        print(f"⚠️ Voice Router 등록 실패: {e}")

    # Phase 23: Multi-Model Intelligence
    try:
        if council_router:
            app.include_router(council_router, prefix="/api", tags=["Council of Minds"])
            print("🧠 Council Router 등록 완료 (Phase 23: 지혜의 의회)")
    except Exception as e:
        print(f"⚠️ Council Router 등록 실패: {e}")

    # Phase 26: AI Self-Improvement
    try:
        if learning_pipeline:
            app.include_router(
                learning_pipeline, prefix="/api", tags=["AI Self-Improvement"]
            )
            print("🧠 Learning Pipeline Router 등록 완료 (Phase 26: 사마휘 자율 학습)")
    except Exception as e:
        print(f"⚠️ Learning Pipeline Router 등록 실패: {e}")

    # Phase 27: Project Serenity
    try:
        if serenity_router:
            app.include_router(
                serenity_router, prefix="/api", tags=["Serenity (GenUI)"]
            )
            print("🎨 Serenity Router 등록 완료 (Phase 27: 프로젝트 제네시스)")
    except Exception as e:
        print(f"⚠️ Serenity Router 등록 실패: {e}")

    # 철학적 Copilot Dashboard (眞善美孝永 철학의 실시간 조화 모니터링)
    try:
        from AFO.api.routes.philosophical_copilot import \
            router as philosophical_copilot_router

        app.include_router(philosophical_copilot_router, tags=["철학적 Copilot"])
        print(
            "🎯 철학적 Copilot Router 등록 완료 (제갈량의 전략 + 관우의 검증 + 여포의 맥박)"
        )
    except Exception as e:
        print(f"⚠️ 철학적 Copilot Router 등록 실패: {e}")

    # Additional RAG and query routers
    if rag_query_router:
        app.include_router(rag_query_router, prefix="/api", tags=["RAG (Phase 12)"])

    if finance_router:
        app.include_router(finance_router)

    if ssot_router:
        app.include_router(ssot_router)

    # Chancellor (Strategy Engine)
    if chancellor_router:
        app.include_router(chancellor_router)
        print(
            "✅ 승상 API 라우터 등록 완료 (LangGraph Optimized: Chancellor + 3 Strategists)"
        )

    # System Stream Routes (SSE 실시간 스트리밍)
    try:
        from AFO.api.routes.system_stream import router as system_stream_router

        app.include_router(system_stream_router)
        print("✅ System Stream Router 등록 완료 (왕국의 신경계 SSE 스트리밍)")
    except Exception as e:
        print(f"⚠️ System Stream Router 등록 실패: {e}")

    # Operation Gwanggaeto: Julie Royal Tax (Goodness)
    try:
        from AFO.api.routers.julie_royal import router as julie_royal_router

        app.include_router(julie_royal_router)
        print("✅ Julie Royal Router 등록 완료 (Operation Gwanggaeto: Tax Truth 2025)")
    except Exception as e:
        print(f"⚠️ Julie Royal Router 등록 실패: {e}")


def _register_legacy_routers(app: FastAPI) -> None:
    """Register legacy and compatibility routers."""
    # Debug: Check current routes before Skills registration
    existing_routes_before = len([r for r in app.routes if hasattr(r, "path")])
    print(f"🔍 Routes before Skills registration: {existing_routes_before}")

    # Skills API - Critical for AFO Kingdom functionality
    print(f"🔍 Skills router object: {skills_router}")
    print(f"🔍 Skills router is None: {skills_router is None}")

    if skills_router:
        try:
            print(f"🔍 Skills router has {len(skills_router.routes)} internal routes")
            for route in skills_router.routes:
                if hasattr(route, "path"):
                    print(f"   - Internal route: {route.path}")

            app.include_router(skills_router, prefix="/api/skills", tags=["Skills"])
            print("✅ Skills API 라우터 등록 완료 (손발 연결)")

            # Debug: Check ALL routes after Skills registration
            all_routes_after = []
            for route in app.routes:
                if hasattr(route, "path"):
                    route_info = {
                        "path": route.path,
                        "methods": list(getattr(route, "methods", set())),
                        "name": getattr(route, "name", "unknown"),
                    }
                    all_routes_after.append(route_info)

            existing_routes_after = len(all_routes_after)
            skills_routes = [
                r for r in all_routes_after if "skills" in r["path"].lower()
            ]
            print(f"🔍 Total routes after Skills registration: {existing_routes_after}")
            print(f"🔍 Skills routes found: {len(skills_routes)}")

            # Check for conflicts - routes with similar paths
            api_routes = [r for r in all_routes_after if r["path"].startswith("/api/")]
            print(f"🔍 Total API routes: {len(api_routes)}")
            for route in api_routes:
                print(f"   - API route: {route['path']} {route['methods']}")

            if skills_routes:
                for route in skills_routes:
                    print(f"   ✅ Skills route: {route['path']} {route['methods']}")
            else:
                print("❌ No skills routes found after registration!")
                # Check if any routes contain 'skill' (typo check)
                skill_like_routes = [
                    r for r in all_routes_after if "skill" in r["path"].lower()
                ]
                if skill_like_routes:
                    print("🔍 Routes containing 'skill':")
                    for route in skill_like_routes:
                        print(f"   - {route['path']} {route['methods']}")

        except Exception as e:
            print(f"❌ Skills router registration failed: {e}")
            import traceback

            traceback.print_exc()
    else:
        print("❌ Skills router is falsy - not registering")

    # Comprehensive Health Check (integrated)
    try:
        from AFO.api.routes.comprehensive_health import \
            router as comprehensive_health_router

        app.include_router(comprehensive_health_router)
        print("✅ Comprehensive Health Check 라우터 등록 완료 (조기 등록)")
    except ImportError:
        try:
            from AFO.api.routes.comprehensive_health import \
                router as comprehensive_health_router

            app.include_router(comprehensive_health_router)
            print(
                "✅ Comprehensive Health Check 라우터 등록 완료 (fallback, 조기 등록)"
            )
        except Exception as e:
            print(f"⚠️ Comprehensive Health Check 라우터 등록 실패 (조기 등록): {e}")

    # MCP Tools Management API
    try:
        from AFO.api.routes.mcp_tools import router as mcp_tools_router

        app.include_router(mcp_tools_router)
        print("✅ MCP Tools Management 라우터 등록 완료")
    except ImportError:
        try:
            from AFO.api.routes.mcp_tools import router as mcp_tools_router

            app.include_router(mcp_tools_router)
            print("✅ MCP Tools Management 라우터 등록 완료 (fallback)")
        except Exception as e:
            print(f"⚠️ MCP Tools Management 라우터 등록 실패: {e}")

    # Integrity Check API
    try:
        from AFO.api.routes.integrity_check import \
            router as integrity_check_router

        app.include_router(integrity_check_router)
        print("✅ Integrity Check 라우터 등록 완료")
    except ImportError:
        try:
            from AFO.api.routes.integrity_check import \
                router as integrity_check_router

            app.include_router(integrity_check_router)
            print("✅ Integrity Check 라우터 등록 완료 (fallback)")
        except Exception as e:
            print(f"⚠️ Integrity Check 라우터 등록 실패: {e}")

    # Git Status API
    try:
        from AFO.api.routes.git_status import router as git_status_router

        app.include_router(git_status_router)
        print("✅ Git Status 라우터 등록 완료")
    except ImportError:
        try:
            from AFO.api.routes.git_status import router as git_status_router

            app.include_router(git_status_router)
            print("✅ Git Status 라우터 등록 완료 (fallback)")
        except Exception as e:
            print(f"⚠️ Git Status 라우터 등록 실패: {e}")

    # Intake API
    try:
        from afo_soul_engine.routers.intake import router as intake_router

        app.include_router(intake_router)
        print("✅ Intake API 라우터 등록 완료 (조기 등록)")
    except ImportError:
        try:
            from AFO.afo_soul_engine.routers.intake import \
                router as intake_router

            app.include_router(intake_router)
            print("✅ Intake API 라우터 등록 완료 (fallback, 조기 등록)")
        except Exception as e:
            print(f"⚠️ Intake API 라우터 등록 건너뜀 (조기 등록, 로드 실패: {e})")

    # GenUI (Phase 9)
    try:
        from AFO.api.routers.gen_ui import router as gen_ui_router

        app.include_router(gen_ui_router)
        print("✅ GenUI Engine activated (Phase 9: Serenity)")
    except Exception as e:
        print(f"⚠️ GenUI Engine load failed: {e}")

    # Family Hub (Phase 2)
    try:
        from AFO.api.routers.family import router as family_router

        app.include_router(family_router)
        app.include_router(family_router, prefix="/api")
        print(
            "✅ Family Hub API 라우터 등록 완료 (Phase 2: Family Hub OS - 美: 모듈화 + 일관 네이밍) - /family and /api/family"
        )
    except ImportError:
        try:
            from AFO.api.routers.family import router as family_router

            app.include_router(family_router)
            app.include_router(family_router, prefix="/api")
            print(
                "✅ Family Hub API 라우터 등록 완료 (Phase 2: Family Hub OS - fallback) - /family and /api/family"
            )
        except Exception as e:
            print(f"⚠️ Family Hub API 라우터 등록 건너뜀 (로드 실패: {e})")

    # Phase 6B: Cache Metrics
    try:
        from AFO.api.routers.cache import router as cache_router

        app.include_router(cache_router)
        print("✅ Cache Metrics Router 등록 완료 (Phase 6B)")
    except Exception as e:
        print(f"⚠️ Cache Metrics Router 등록 실패: {e}")

    # Strangler Fig Compatibility Router
    if compat_router:
        app.include_router(compat_router, prefix="/api", tags=["Strangler Fig"])
        print("✅ Strangler Fig Compatibility Router 등록 완료 (Prefix: /api/compat)")
