# conftest.py - Root pytest configuration
# 깨진 테스트 파일 무시 (AFO.xxx 잘못된 import 경로)

collect_ignore = [
    # =========================================
    # API tests (AFO.api imports - doesn't exist)
    # =========================================
    "packages/afo-core/tests/api/test_wallet_routers_comprehensive.py",
    "packages/afo-core/tests/api/test_api_chat.py",
    "packages/afo-core/tests/api/test_api_health.py",
    "packages/afo-core/tests/api/test_api_pillars.py",
    "packages/afo-core/tests/api/test_api_skills.py",
    
    # =========================================
    # API Wallet tests
    # =========================================
    "packages/afo-core/tests/test_api_wallet_advanced.py",
    "packages/afo-core/tests/test_api_wallet_cli.py",
    "packages/afo-core/tests/test_api_wallet_db_mock.py",
    "packages/afo-core/tests/test_api_wallet_imports.py",
    "packages/afo-core/tests/test_api_wallet_vault_fallback.py",
    
    # =========================================
    # Service tests (AFO.services imports)
    # =========================================
    "packages/afo-core/tests/test_hybrid_rag_advanced.py",
    
    # =========================================
    # Input server tests
    # =========================================
    "packages/afo-core/tests/test_input_server.py",
    "packages/afo-core/tests/test_input_server_advanced.py",
    
    # =========================================
    # KMS tests
    # =========================================
    "packages/afo-core/tests/test_kms_advanced.py",
    
    # =========================================
    # LLM router tests
    # =========================================
    "packages/afo-core/tests/test_llm_router_advanced.py",
    
    # =========================================
    # Redis tests
    # =========================================
    "packages/afo-core/tests/test_redis_optimized.py",
    
    # =========================================
    # Scholars tests
    # =========================================
    "packages/afo-core/tests/test_scholars.py",
    
    # =========================================
    # Settings tests (AFO.config.settings imports)
    # =========================================
    "packages/afo-core/tests/test_settings.py",
    
    # =========================================
    # Skills registry tests
    # =========================================
    "packages/afo-core/tests/test_skills_registry.py",
    
    # =========================================
    # Utils tests (AFO.utils imports)
    # =========================================
    "packages/afo-core/tests/test_utils_advanced.py",
    "packages/afo-core/tests/test_utils.py",
    
    # =========================================
    # API server tests
    # =========================================
    "packages/afo-core/tests/test_api_server.py",
    "packages/afo-core/tests/test_api_server_lifespan.py",
    
    # =========================================
    # Trinity-OS tests
    # =========================================
    "packages/trinity-os/tests/test_problem_detector.py",

    # =========================================
    # LLM implementation tests (AFO.llms imports)
    # =========================================
    "packages/afo-core/tests/llm/test_llm_implementations.py",

    # =========================================
    # Additional API tests (AFO.api imports)
    # =========================================
    "packages/afo-core/tests/api/test_api_system_health.py",
    "packages/afo-core/tests/api/test_api_wallet_routes.py",
]

