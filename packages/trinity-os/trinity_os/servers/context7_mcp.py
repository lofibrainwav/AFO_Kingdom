from datetime import datetime


class Context7MCP:
    """
    Context7 Tool (Knowledge Injector)
    Provides pinned context and documentation retrieval for the AFO Kingdom.
    """

    # Mock Knowledge Base (In production, this would be a Vector DB or Doc Store)
    KNOWLEDGE_BASE = {
        "AFO_ARCHITECTURE": """
        AFO Kingdom Architecture (The Body):
        - Brain: Chancellor (LangGraph) - Decision & Strategy
        - Soul: Trinity (5 Pillars) - Philosophy & Ethics
        - Heart: Auth (Security) - Protection & Access
        - Liver: Users (Management) - Identity & History
        - Stomach: Intake (Data Parsing) - Digestion & Processing
        - Mask: Personas (Interface) - Communication & Style
        - Spleen: Family Hub (Happiness) - Well-being & Stability
        """,
        "TRINITY_PHILOSOPHY": """
        Trinity 5 Pillars (The Soul):
        1. Truth (眞, 35%): Technical Certainty, Logic, Facts. (Scholar: Jegalyang)
        2. Goodness (善, 35%): Ethics, Safety, Risk Management. (Scholar: Samayi)
        3. Beauty (美, 20%): Aesthetics, UX, Simplicity. (Scholar: Juyu)
        4. Serenity (孝, 8%): Peace of Mind, Friction Reduction. (Role: Chancellor)
        5. Eternity (永, 2%): Sustainability, Legacy, Long-term view. (Role: Chancellor)
        
        Governance:
        - Trinity Score = Weighted Sum of 5 Pillars.
        - Auto-Run Gate: Requires Score > 90 AND Risk < 10.
        """,
        "SIXXON_BODY": """
        Sixxon (The Physical Manifestation):
        - Core Framework: FastAPI (Backend), Next.js 14+ (Frontend)
        - Infrastructure: Docker, Kubernetes (Orchestration)
        - Database: PostgreSQL (Memory), Redis (Fast Access)
        - AI Engine: AfoUltimateMCPServer (Neurology)
        - Auth System: Sixxon Auth Recapture (Codex)
        - Design System: Glassmorphism, Brutalism, "Cute" UI (Aesthetics)
        """,
        "MCP_PROTOCOL": """
        MCP (Master Control Program) utilizes JSON-RPC 2.0 over stdio.
        Unified Server: afo_ultimate_mcp_server.py
        Tools: shell_execute, read_file, write_file, kingdom_health, calculate_trinity_score, verify_fact, cupy_weighted_sum, sequential_thinking, retrieve_context
        """,
        "API_ENDPOINTS": """
        AFO Kingdom Soul Engine API - 49개 엔드포인트:
        - Health & System: GET /, GET /health, GET /api/system/metrics
        - Chancellor: POST /chancellor/invoke, GET /chancellor/health
        - Skills Registry: GET /api/skills/list, POST /api/skills/{skill_id}/execute
        - 5 Pillars: GET /api/5pillars/current, POST /api/5pillars/live
        - RAG: POST /api/crag
        - Family Hub: GET /family/, GET /family/members, POST /family/activity
        - Authentication: POST /api/auth/login, POST /api/auth/verify
        - Users: GET /api/users/{user_id}, POST /api/users, PUT /api/users/{user_id}
        - Personas: GET /api/personas/current, POST /api/personas/switch
        - Chat: POST /message, GET /providers, GET /stats
        - Julie CPA: GET /api/julie/status, GET /api/julie/dashboard
        - Wallet: POST /browser/save-token, GET /browser/extraction-script
        
        모든 엔드포인트는 실행 시 眞善美孝永 Trinity Score를 반환합니다.
        상세 참조: docs/API_ENDPOINTS_REFERENCE.md
        """,
        "SKILLS_REGISTRY": """
        AFO Kingdom Skills Registry - 19개 스킬:
        - Strategic Command: skill_005_strategy_engine, skill_010_family_persona
        - RAG Systems: skill_002_ultimate_rag, skill_019_hybrid_graphrag
        - Workflow Automation: skill_001_youtube_spec_gen, skill_011_dev_tool_belt, skill_015_suno_composer
        - Health Monitoring: skill_003_health_monitor, skill_017_data_pipeline, skill_018_docker_recovery
        - Memory Management: skill_013_obsidian_librarian
        - Analysis Evaluation: skill_004_ragas_evaluator, skill_006_ml_metacognition, skill_008_soul_refine, skill_009_advanced_cosine
        - Integration: skill_007_multi_cloud, skill_012_mcp_tool_bridge, skill_014_strangler_integrator, skill_016_web3_manager
        - Metacognition: skill_015_vibe_coder
        
        모든 스킬은 眞善美孝 철학 점수를 가지며, API를 통해 실행 가능합니다.
        상세 참조: docs/SKILLS_REGISTRY_REFERENCE.md
        """,
        "DEPLOYMENT": """
        AFO Kingdom 배포 가이드:
        - Docker Compose: packages/afo-core/docker-compose.yml 사용
        - Kubernetes: helm/afo-chart 사용
        - 환경 변수: .env 파일 또는 환경 변수로 설정
        - 헬스 체크: GET /health 엔드포인트 사용
        - 모니터링: Prometheus 메트릭, 로그 스트리밍
        
        주요 서비스:
        - Backend (Soul Engine): Port 8010
        - Frontend (Dashboard): Port 3000
        - PostgreSQL: Port 15432
        - Redis: Port 6379
        - Qdrant: Port 6333
        
        상세 참조: docs/DEPLOYMENT_GUIDE.md
        """,
        "CONFIGURATION": """
        AFO Kingdom 설정 가이드:
        - 데이터베이스: POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
        - Redis: REDIS_URL
        - Qdrant: QDRANT_URL
        - API Keys: OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY
        - AntiGravity: ENVIRONMENT, AUTO_DEPLOY, DRY_RUN_DEFAULT
        - MCP: MCP_SERVER_URL, WORKSPACE_ROOT
        - Soul Engine: SOUL_ENGINE_URL, API_PORT
        
        설정 우선순위: 환경 변수 > 환경별 설정 파일 > 기본값
        상세 참조: docs/CONFIGURATION_GUIDE.md
        """,
        "TROUBLESHOOTING": """
        AFO Kingdom 문제 해결 가이드:
        - 포트 충돌: lsof -i :8010으로 확인, 프로세스 종료
        - 데이터베이스 연결 실패: PostgreSQL 연결 확인, Docker 컨테이너 확인
        - Redis 연결 실패: redis-cli ping으로 확인
        - 의존성 설치 실패: pip install -r requirements.txt 재실행
        - MCP 서버 연결 실패: Cursor MCP 설정 확인, PYTHONPATH 확인
        - Trinity Score 계산 오류: SSOT 파일 확인, Trinity Score 엔진 확인
        
        디버깅: 로그 확인, 헬스 체크, 환경 변수 확인
        상세 참조: docs/TROUBLESHOOTING.md
        """,
        "DOCUMENTATION": """
        AFO Kingdom 문서화 완료 상태:
        - 핵심 시스템 문서화: 100% 완료 (5개 시스템)
        - 통합 참조 문서: 100% 완료 (5개 문서)
        - 운영 가이드: 100% 완료 (3개 가이드)
        - 총 문서 수: 37개
        - 새로 생성된 문서: 9개 (2,796줄, 55.3 KB)
        
        주요 문서:
        - API_ENDPOINTS_REFERENCE.md: 49개 엔드포인트 문서화
        - SKILLS_REGISTRY_REFERENCE.md: 19개 스킬 문서화
        - DEPLOYMENT_GUIDE.md: Docker, Kubernetes 배포 가이드
        - CONFIGURATION_GUIDE.md: 환경 변수 및 설정 가이드
        - TROUBLESHOOTING.md: 문제 해결 가이드
        
        검증 완료: Sequential Thinking 10단계 분석 완료
        상세 참조: docs/DOCUMENTATION_COMPLETE_VERIFICATION.md
        """,
        "OBSIDIAN_LIBRARIAN": """
        AFO Obsidian Librarian (skill_013_obsidian_librarian):
        - 왕국의 지식 관리 시스템
        - 옵시디언 vault 읽기/쓰기
        - Daily Notes 관리
        - 양방향 링크 생성
        - 철학 점수: 眞 96%, 善 98%, 美 95%, 孝 99%
        
        옵시디언 RAG 시스템:
        - ObsidianLoader: Markdown 문서 로드 및 메타데이터 파싱
        - Qdrant 벡터 DB 인덱싱
        - LangGraph RAG 파이프라인
        - 자동 동기화 (sync_obsidian_vault.py)
        
        경로: packages/afo-core/scripts/rag/
        상세 참조: packages/afo-core/docs/afo/OBSIDIAN_RAG_GOT_COMPLETE.md
        """,
        "ROYAL_LIBRARY": """
        AFO 왕국의 사서 (Royal Library) - 41가지 원칙:
        
        제1서: 손자병법 (12선) - 眞 70% / 孝 30%
        1. 지피지기 (Rule #0): Context7과 DB 조회 필수
        2. 상병벌모: 기존 라이브러리 활용 우선
        3. 병자궤도야: DRY_RUN 기본값 True
        4. 병귀신속: 비동기 처리 (asyncio, Celery)
        5. 도천지장법: Trinity Score 5기둥 정렬 체크
        6. 정병: 표준 패턴 준수 후 오버라이딩
        7. 허실: Profiling & Optimization
        8. 구변: try-except-else-finally 분기
        9. 용간: 로그 및 모니터링 (logger.info, Sentry)
        10. 화공: confirm_dangerous_action() 게이트
        11. 졸속: MVP 배포 우선
        12. 부전이굴: Cron Job, Background Service
        
        제2서: 삼국지 (12선) - 永 60% / 善 40%
        13. 도원결의: Interface 통일, Shared Context
        14. 삼고초려: Retry(max_attempts=3, backoff=exponential)
        15. 공성계: Graceful Degradation, Skeleton UI
        16. 제갈량의 초선차전: pip install, External API
        17. 연환계: Pipeline Pattern, LangGraph Node Linking
        18. 미인계: Abstract complexity behind UI
        19. 칠종칠금: Write -> Critique -> Refine Loop
        20. 적벽대전 동남풍: Scheduled Tasks
        21. 고육지계: Circuit Breaker
        22. 한실 부흥: Linting, Convention Check
        23. 천하삼분: Modular Architecture
        24. 백제성 탁고: Checkpoint Saving, State Persistence
        
        제3서: 군주론 (9선) - 善 50% / 眞 50%
        25. 사랑보다 두려움: Strict Typing, Validation
        26. 비르투와 포르투나: Exception Handling
        27. 여우와 사자: Algorithm Selection
        28. 증오 피하기: UX Optimization
        29. 무장한 예언자: Executable Code Only
        30. 잔인함의 효율적 사용: Garbage Collection, Resource Cleanup
        31. 국가 유지: Health Checks, High Availability
        32. 현명한 조언자: Model Router
        33. 결과가 수단을 정당화: Creative Solution w/ High Safety
        
        제4서: 전쟁론 (8선) - 眞 60% / 孝 40%
        34. 전장의 안개: Null Check, Data Validation
        35. 마찰: Complexity Estimation
        36. 중심: Root Cause Analysis
        37. 공세 종말점: Resource Monitoring
        38. 지휘 통일: Singleton Pattern, Locking
        39. 병력 절약: Token/Compute Optimization
        40. 전쟁의 목적: Clear Objectives
        41. 평화의 조건: Stable State
        
        상세 참조: docs/AFO_ROYAL_LIBRARY.md
        """,
    }

    @staticmethod
    def retrieve_context(query: str, domain: str = "general") -> dict:
        """
        Retrieve context based on query keywords.
        """
        results = []
        query_upper = query.upper()

        # Architecture queries
        if "ARCH" in query_upper or "STRUCT" in query_upper:
            results.append(Context7MCP.KNOWLEDGE_BASE["AFO_ARCHITECTURE"])

        # Trinity Philosophy queries
        if "TRINITY" in query_upper or "PHILOSOPHY" in query_upper or "SCORE" in query_upper or "SOUL" in query_upper:
            results.append(Context7MCP.KNOWLEDGE_BASE["TRINITY_PHILOSOPHY"])

        # Sixxon Body queries
        if "SIXXON" in query_upper or "BODY" in query_upper:
            results.append(Context7MCP.KNOWLEDGE_BASE["SIXXON_BODY"])

        # MCP Protocol queries
        if "MCP" in query_upper or "TOOL" in query_upper:
            results.append(Context7MCP.KNOWLEDGE_BASE["MCP_PROTOCOL"])

        # API Endpoints queries
        if "API" in query_upper or "ENDPOINT" in query_upper or "ROUTE" in query_upper:
            results.append(Context7MCP.KNOWLEDGE_BASE["API_ENDPOINTS"])

        # Skills Registry queries
        if "SKILL" in query_upper or "REGISTRY" in query_upper:
            results.append(Context7MCP.KNOWLEDGE_BASE["SKILLS_REGISTRY"])

        # Deployment queries
        deploy_keywords = ["DEPLOY", "DOCKER", "KUBERNETES", "배포", "컨테이너"]
        if any(kw in query_upper for kw in deploy_keywords) or any(kw in query for kw in ["배포", "컨테이너"]):
            results.append(Context7MCP.KNOWLEDGE_BASE["DEPLOYMENT"])

        # Configuration queries
        config_keywords = ["CONFIG", "SETTING", "ENV", "환경", "설정"]
        if any(kw in query_upper for kw in config_keywords) or any(kw in query for kw in ["환경", "설정"]):
            results.append(Context7MCP.KNOWLEDGE_BASE["CONFIGURATION"])

        # Troubleshooting queries
        troubleshoot_keywords = ["TROUBLESHOOT", "DEBUG", "ERROR", "문제", "해결", "디버그"]
        if any(kw in query_upper for kw in troubleshoot_keywords) or any(
            kw in query for kw in ["문제", "해결", "디버그"]
        ):
            results.append(Context7MCP.KNOWLEDGE_BASE["TROUBLESHOOTING"])

        # Documentation queries
        doc_keywords = ["DOC", "DOCUMENT", "문서", "문서화"]
        if any(kw in query_upper for kw in doc_keywords) or any(kw in query for kw in ["문서", "문서화"]):
            results.append(Context7MCP.KNOWLEDGE_BASE["DOCUMENTATION"])

        # Obsidian Librarian queries
        obsidian_keywords = ["OBSIDIAN", "LIBRARIAN", "사서", "옵시디언", "VAULT"]
        if any(kw in query_upper for kw in obsidian_keywords) or any(
            kw in query for kw in ["옵시디언", "사서", "vault"]
        ):
            results.append(Context7MCP.KNOWLEDGE_BASE["OBSIDIAN_LIBRARIAN"])

        # Royal Library queries
        royal_keywords = ["ROYAL", "LIBRARY", "사서", "원칙", "헌법", "손자", "삼국지", "군주론", "전쟁론"]
        if any(kw in query_upper for kw in royal_keywords) or any(
            kw in query for kw in ["사서", "원칙", "헌법", "손자병법", "삼국지", "군주론", "전쟁론"]
        ):
            results.append(Context7MCP.KNOWLEDGE_BASE["ROYAL_LIBRARY"])

        if not results:
            return {
                "found": False,
                "message": f"No specific context found for '{query}'.",
                "timestamp": datetime.now().isoformat(),
            }

        combined_context = "\n---\n".join(results)

        # Calculate Trinity Metadata (Truth Impact)
        truth_score = 10 if results else 0

        return {
            "found": True,
            "context": combined_context.strip(),
            "domain": domain,
            "metadata": {"truth_impact": truth_score, "source": "Context7 Internal DB"},
        }
