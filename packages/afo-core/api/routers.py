"""
AFO Kingdom API Router Registration

Centralized router registration system for organized API management.
"""

from fastapi import FastAPI

from AFO.api.compat import (
    aicpa_router,
    auth_router,
    # Phase-specific routers
    budget_router,
    chancellor_router,
    council_router,
    education_system_router,
    finance_router,
    got_router,
    grok_stream_router,
    # Core routers
    health_router,
    learning_log_router,
    learning_pipeline,
    matrix_router,
    modal_data_router,
    multi_agent_router,
    n8n_router,
    personas_router,
    # Feature routers
    pillars_router,
    rag_query_router,
    root_router,
    serenity_router,
    skills_router,
    ssot_router,
    strangler_router,
    streams_router,
    system_health_router,
    trinity_policy_router,
    trinity_sbt_router,
    users_router,
    voice_router,
    wallet_router,
)


def setup_routers(app: FastAPI) -> None:
    """Setup and register all API routers in organized manner."""

    # Core system routers
    _register_core_routers(app)

    # Feature routers
    _register_feature_routers(app)

    # Phase-specific routers
    _register_phase_routers(app)

    # Legacy and fallback routers
    _register_legacy_routers(app)


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
        app.include_router(matrix_router, prefix="/api", tags=["Matrix Stream (Phase 10)"])


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
        app.include_router(strangler_router, prefix="/api/strangler", tags=["Strangler Fig"])

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

    # Education and modal systems
    if education_system_router:
        app.include_router(
            education_system_router, prefix="/api/education", tags=["Education System"]
        )

    if modal_data_router:
        app.include_router(modal_data_router, prefix="/api/modal", tags=["Modal Data"])

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
            app.include_router(learning_pipeline, prefix="/api", tags=["AI Self-Improvement"])
            print("🧠 Learning Pipeline Router 등록 완료 (Phase 26: 사마휘 자율 학습)")
    except Exception as e:
        print(f"⚠️ Learning Pipeline Router 등록 실패: {e}")

    # Phase 27: Project Serenity
    try:
        if serenity_router:
            app.include_router(serenity_router, prefix="/api", tags=["Serenity (GenUI)"])
            print("🎨 Serenity Router 등록 완료 (Phase 27: 프로젝트 제네시스)")
    except Exception as e:
        print(f"⚠️ Serenity Router 등록 실패: {e}")

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
        print("✅ 승상 API 라우터 등록 완료 (LangGraph Optimized: Chancellor + 3 Strategists)")


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
            skills_routes = [r for r in all_routes_after if "skills" in r["path"].lower()]
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
                skill_like_routes = [r for r in all_routes_after if "skill" in r["path"].lower()]
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
        from AFO.api.routes.comprehensive_health import router as comprehensive_health_router

        app.include_router(comprehensive_health_router)
        print("✅ Comprehensive Health Check 라우터 등록 완료 (조기 등록)")
    except ImportError:
        try:
            from api.routes.comprehensive_health import router as comprehensive_health_router

            app.include_router(comprehensive_health_router)
            print("✅ Comprehensive Health Check 라우터 등록 완료 (fallback, 조기 등록)")
        except Exception as e:
            print(f"⚠️ Comprehensive Health Check 라우터 등록 실패 (조기 등록): {e}")

    # Intake API
    try:
        from afo_soul_engine.routers.intake import router as intake_router

        app.include_router(intake_router)
        print("✅ Intake API 라우터 등록 완료 (조기 등록)")
    except ImportError:
        try:
            from AFO.afo_soul_engine.routers.intake import router as intake_router

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
            from api.routers.family import router as family_router

            app.include_router(family_router)
            app.include_router(family_router, prefix="/api")
            print(
                "✅ Family Hub API 라우터 등록 완료 (Phase 2: Family Hub OS - fallback) - /family and /api/family"
            )
        except Exception as e:
            print(f"⚠️ Family Hub API 라우터 등록 건너뜀 (로드 실패: {e})")
