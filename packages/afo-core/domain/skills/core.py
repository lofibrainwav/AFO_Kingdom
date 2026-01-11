# Trinity Score: 90.0 (Established by Chancellor)
"""
AFO Core Skills (domain/skills/core.py)

Registry of built-in skills for the AFO Kingdom.
"""

from __future__ import annotations

import os
from typing import cast

from .models import (
    AFOSkillCard,
    ExecutionMode,
    MCPConfig,
    PhilosophyScore,
    SkillCategory,
    SkillIOSchema,
    SkillParameter,
)
from .registry import SkillRegistry


def _get_mcp_server_url() -> str | None:
    """Helper to get MCP server URL from environment"""
    try:
        from AFO.config.settings import get_settings

        settings = get_settings()
        return cast(
            str | None, getattr(settings, "MCP_SERVER_URL", os.getenv("MCP_SERVER_URL"))
        )
    except Exception:  # nosec
        return os.getenv("MCP_SERVER_URL")


def register_core_skills() -> SkillRegistry:
    """Register AFO's core built-in skills"""
    registry = SkillRegistry()

    # Skill 1: YouTube to n8n Spec Generator
    skill_001 = AFOSkillCard(
        skill_id="skill_001_youtube_spec_gen",
        name="YouTube to n8n Spec Generator",
        description="Converts YouTube tutorial transcripts to executable n8n workflow specifications using GPT-4o-mini",
        category=SkillCategory.WORKFLOW_AUTOMATION,
        tags=["youtube", "n8n", "spec-generation", "llm", "workflow"],
        version="1.0.0",
        capabilities=[
            "youtube_transcript_extraction",
            "llm_spec_generation",
            "n8n_workflow_creation",
            "error_handling",
        ],
        dependencies=["openai_api", "transcript_mcp"],
        execution_mode=ExecutionMode.ASYNC,
        endpoint=None,
        estimated_duration_ms=15000,
        input_schema=SkillIOSchema(
            parameters=[
                SkillParameter(
                    name="youtube_url",
                    type="string",
                    description="YouTube video URL",
                    required=True,
                ),
                SkillParameter(
                    name="transcript_base",
                    type="string",
                    description="Transcript MCP server base URL",
                    required=False,
                    default=_get_mcp_server_url(),
                ),
            ],
            example={"youtube_url": "https://www.youtube.com/watch?v=abc123"},
        ),
        output_schema=SkillIOSchema(
            parameters=[
                SkillParameter(
                    name="node_spec",
                    type="dict",
                    description="n8n node specification JSON",
                    required=True,
                )
            ]
        ),
        philosophy_scores=PhilosophyScore(
            truth=95, goodness=90, beauty=92, serenity=88
        ),
        mcp_config=MCPConfig(
            mcp_server_url=cast(str, _get_mcp_server_url()),
            capabilities=["transcript_extraction"],
        ),
        documentation_url="https://github.com/lofibrainwav/AFO/blob/main/docs/skills/youtube-spec-gen.md",
    )

    # Skill 2: Ultimate RAG
    skill_002 = AFOSkillCard(
        skill_id="skill_002_ultimate_rag",
        name="Ultimate RAG (Hybrid CRAG + Self-RAG)",
        description="Hybrid Corrective RAG + Self-RAG implementation with Lyapunov-proven convergence",
        category=SkillCategory.RAG_SYSTEMS,
        tags=["rag", "crag", "self-rag", "hybrid", "lyapunov"],
        version="2.0.0",
        capabilities=[
            "corrective_rag",
            "self_rag",
            "lyapunov_convergence",
            "multi_hop_reasoning",
        ],
        dependencies=["openai_api", "langchain"],
        execution_mode=ExecutionMode.STREAMING,
        estimated_duration_ms=3000,
        input_schema=SkillIOSchema(
            parameters=[
                SkillParameter(
                    name="query", type="string", description="User query", required=True
                ),
                SkillParameter(
                    name="top_k",
                    type="int",
                    description="Number of documents to retrieve",
                    required=False,
                    default=5,
                    validation_rules={"min": 1, "max": 20},
                ),
            ]
        ),
        philosophy_scores=PhilosophyScore(
            truth=98, goodness=95, beauty=90, serenity=92
        ),
        documentation_url="https://github.com/lofibrainwav/AFO/blob/main/afo_soul_engine/hybrid_crag_selfrag.py",
    )

    # Skill 3: 11-Organ Health Monitor
    skill_003 = AFOSkillCard(
        skill_id="skill_003_health_monitor",
        name="11-Organ Health Monitor",
        description="Monitors 11 critical AFO system organs (五臟六腑) and generates health reports",
        category=SkillCategory.HEALTH_MONITORING,
        tags=["health", "monitoring", "五臟六腑", "diagnostics"],
        version="1.5.0",
        capabilities=[
            "redis_health_check",
            "postgresql_health_check",
            "chromadb_health_check",
            "api_server_health_check",
            "n8n_health_check",
            "comprehensive_report",
        ],
        dependencies=["redis", "postgresql", "docker"],
        execution_mode=ExecutionMode.SYNC,
        estimated_duration_ms=500,
        philosophy_scores=PhilosophyScore(
            truth=100, goodness=100, beauty=95, serenity=100
        ),
        documentation_url="https://github.com/lofibrainwav/AFO/blob/main/afo_soul_engine/auto_health_monitor.py",
    )

    # Skill 4: Ragas Evaluator
    skill_004 = AFOSkillCard(
        skill_id="skill_004_ragas_evaluator",
        name="Ragas RAG Quality Evaluator",
        description="Evaluates RAG quality using 4 metrics: Faithfulness, Relevancy, Precision, Recall",
        category=SkillCategory.ANALYSIS_EVALUATION,
        tags=["ragas", "evaluation", "metrics", "quality"],
        version="1.2.0",
        capabilities=[
            "faithfulness_scoring",
            "answer_relevancy_scoring",
            "context_precision_scoring",
            "context_recall_scoring",
        ],
        dependencies=["ragas", "openai_api"],
        execution_mode=ExecutionMode.ASYNC,
        estimated_duration_ms=5000,
        philosophy_scores=PhilosophyScore(
            truth=99, goodness=92, beauty=88, serenity=85
        ),
    )

    # Skill 5: Strategy Engine (LangGraph)
    skill_005 = AFOSkillCard(
        skill_id="skill_005_strategy_engine",
        name="LangGraph Strategy Engine",
        description="4-stage command triage and orchestration using LangGraph with Redis checkpointing",
        category=SkillCategory.STRATEGIC_COMMAND,
        tags=["langgraph", "orchestration", "strategy", "triage"],
        version="2.3.0",
        capabilities=[
            "command_parsing",
            "command_triage",
            "strategy_determination",
            "redis_checkpointing",
            "stateful_conversations",
        ],
        dependencies=["langgraph", "redis"],
        execution_mode=ExecutionMode.ASYNC,
        estimated_duration_ms=1000,
        philosophy_scores=PhilosophyScore(
            truth=96, goodness=94, beauty=93, serenity=95
        ),
        documentation_url="https://github.com/lofibrainwav/AFO/blob/main/afo_soul_engine/strategy_engine.py",
    )

    # Skill 6: ML Metacognition Upgrade
    skill_006 = AFOSkillCard(
        skill_id="skill_006_ml_metacognition",
        name="ML Metacognition Upgrade (Phase 3)",
        description="Self-reflection enhancement with user feedback loop and sympy 2nd derivative optimization",
        category=SkillCategory.ANALYSIS_EVALUATION,
        tags=["metacognition", "optimization", "feedback", "phase3"],
        version="3.0.0",
        capabilities=[
            "feedback_integration",
            "convexity_proof",
            "gap_reduction",
            "10_iteration_loop",
        ],
        dependencies=["sympy", "numpy"],
        execution_mode=ExecutionMode.SYNC,
        estimated_duration_ms=2000,
        philosophy_scores=PhilosophyScore(
            truth=95, goodness=94, beauty=92, serenity=93
        ),
    )

    # Skill 8: Soul Refine
    skill_008 = AFOSkillCard(
        skill_id="skill_008_soul_refine",
        name="Soul Refine (Vibe Alignment)",
        description="Vibe coding and taste alignment using cosine similarity and philosophy balance",
        category=SkillCategory.ANALYSIS_EVALUATION,
        tags=["vibe", "alignment", "soul", "taste", "philosophy"],
        version="1.0.0",
        capabilities=[
            "cosine_similarity",
            "vibe_alignment",
            "philosophy_refinement",
            "soul_purity_calculation",
        ],
        dependencies=["numpy"],
        execution_mode=ExecutionMode.SYNC,
        estimated_duration_ms=1000,
        philosophy_scores=PhilosophyScore(
            truth=94, goodness=95, beauty=97, serenity=96
        ),
    )

    # Skill 9: Advanced Cosine Similarity
    skill_009 = AFOSkillCard(
        skill_id="skill_009_advanced_cosine",
        name="Advanced Cosine Similarity (4 Techniques)",
        description="4 advanced cosine similarity techniques: Weighted, Sparse, Embedding, sqrt (stability 10% ↑)",
        category=SkillCategory.ANALYSIS_EVALUATION,
        tags=["cosine", "advanced", "weighted", "sparse", "embedding", "sqrt", "taste"],
        version="1.0.0",
        capabilities=[
            "weighted_cosine",
            "sparse_cosine_scipy",
            "embedding_cosine_bert",
            "sqrt_cosine_stability",
        ],
        dependencies=["scipy", "sentence-transformers"],
        execution_mode=ExecutionMode.SYNC,
        estimated_duration_ms=1200,
        philosophy_scores=PhilosophyScore(
            truth=97, goodness=96, beauty=93, serenity=95
        ),
    )

    # Skill 10: Family Persona Manager
    skill_010 = AFOSkillCard(
        skill_id="skill_010_family_persona",
        name="Family Persona Manager",
        description="Manages the AFO Family personas (Yeongdeok, Sima Yi, Zhuge Liang) and their interactions",
        category=SkillCategory.STRATEGIC_COMMAND,
        tags=["family", "persona", "roleplay", "interaction"],
        version="1.0.0",
        capabilities=[
            "persona_loading",
            "dialogue_generation",
            "relationship_management",
            "family_meeting",
        ],
        dependencies=["openai_api"],
        execution_mode=ExecutionMode.SYNC,
        estimated_duration_ms=500,
        philosophy_scores=PhilosophyScore(
            truth=92, goodness=94, beauty=96, serenity=95
        ),
    )

    # Skill 11: Verify Full Stack
    skill_011 = AFOSkillCard(
        skill_id="skill_011_verify_full_stack",
        name="Verify Full Stack Integrity",
        description="Comprehensive system health check for all AFO components (DB, Redis, API, Dashboard)",
        category=SkillCategory.HEALTH_MONITORING,
        tags=["verification", "health", "fullstack", "system"],
        version="1.0.0",
        capabilities=[
            "full_stack_verification",
            "trinity_score_check",
            "component_status_report",
        ],
        dependencies=["redis", "postgresql", "docker"],
        execution_mode=ExecutionMode.ASYNC,
        estimated_duration_ms=2000,
        philosophy_scores=PhilosophyScore(
            truth=99, goodness=98, beauty=90, serenity=95
        ),
    )

    # Skill 11 ALT: DevTool Belt
    skill_011_alt = AFOSkillCard(
        skill_id="skill_011_dev_tool_belt",
        name="AFO DevTool Belt",
        description="Essential development tools for agents: Linting, Testing, Git, and Docker management",
        category=SkillCategory.WORKFLOW_AUTOMATION,
        tags=["devtools", "lint", "test", "git", "docker", "maintenance"],
        version="1.0.0",
        capabilities=[
            "run_linter",
            "run_tests",
            "git_commit",
            "docker_restart",
            "system_health_check",
        ],
        dependencies=["ruff", "pytest", "git", "docker"],
        execution_mode=ExecutionMode.SYNC,
        estimated_duration_ms=2000,
        philosophy_scores=PhilosophyScore(
            truth=98, goodness=95, beauty=90, serenity=97
        ),
    )

    # Skill 12: MCP Tool Bridge
    skill_012 = AFOSkillCard(
        skill_id="skill_012_mcp_tool_bridge",
        name="MCP Tool Bridge",
        description="Universal bridge to connect and utilize any external MCP server tools",
        category=SkillCategory.INTEGRATION,
        tags=["mcp", "integration", "tools", "bridge", "universal"],
        version="1.0.0",
        capabilities=[
            "list_mcp_resources",
            "list_mcp_tools",
            "call_mcp_tool",
            "read_mcp_resource",
        ],
        dependencies=["mcp"],
        execution_mode=ExecutionMode.ASYNC,
        estimated_duration_ms=1000,
        philosophy_scores=PhilosophyScore(
            truth=95, goodness=99, beauty=96, serenity=94
        ),
        mcp_config=MCPConfig(
            mcp_version="2024.11.1", capabilities=["tools", "resources"]
        ),
    )

    # Skill 13: Obsidian Librarian
    skill_013 = AFOSkillCard(
        skill_id="skill_013_obsidian_librarian",
        name="AFO Obsidian Librarian",
        description="Manages the Kingdom's Knowledge in Obsidian. Reads/Writes notes, and creates links.",
        category=SkillCategory.MEMORY_MANAGEMENT,
        tags=["obsidian", "knowledge", "library", "markdown", "notes"],
        version="1.0.0",
        capabilities=[
            "read_note",
            "write_note",
            "search_notes",
            "append_daily_log",
            "link_notes",
            "get_backlinks",
        ],
        dependencies=["markdown", "frontmatter"],
        execution_mode=ExecutionMode.SYNC,
        estimated_duration_ms=500,
        philosophy_scores=PhilosophyScore(
            truth=96, goodness=98, beauty=95, serenity=99
        ),
    )

    # Skill 14: Strangler Fig Integrator
    skill_014 = AFOSkillCard(
        skill_id="skill_014_strangler_integrator",
        name="Strangler Fig Integrator",
        description="Unifies isolated services (n8n, LangFlow) into the Gateway (Port 3000).",
        category=SkillCategory.INTEGRATION,
        tags=["strangler", "integration", "frontend", "n8n", "langflow"],
        version="1.0.0",
        capabilities=["proxy_service", "check_integration_health", "iframe_bridge"],
        dependencies=["react", "iframe"],
        execution_mode=ExecutionMode.SYNC,
        estimated_duration_ms=200,
        philosophy_scores=PhilosophyScore(
            truth=95, goodness=99, beauty=94, serenity=98
        ),
    )

    # Skill 15: Suno AI Composer
    skill_015 = AFOSkillCard(
        skill_id="skill_015_suno_composer",
        name="Suno AI Music Composer",
        description="Generates music and lyrics using Suno AI. Handles polling and downloading.",
        category=SkillCategory.WORKFLOW_AUTOMATION,
        tags=["suno", "music", "creative", "ai-art", "audio"],
        version="1.0.0",
        capabilities=[
            "generate_music",
            "generate_lyrics",
            "download_audio",
            "get_credits",
        ],
        dependencies=["suno-api", "requests"],
        execution_mode=ExecutionMode.ASYNC,
        estimated_duration_ms=60000,
        philosophy_scores=PhilosophyScore(
            truth=85, goodness=90, beauty=100, serenity=95
        ),
    )

    # Skill 16: Web3 Manager
    skill_016 = AFOSkillCard(
        skill_id="skill_016_web3_manager",
        name="Web3 Blockchain Manager",
        description="Manages blockchain interactions and smart contract execution for assets.",
        category=SkillCategory.INTEGRATION,
        tags=["web3", "blockchain", "crypto", "wallet", "smart-contract"],
        version="1.0.0",
        capabilities=[
            "check_balance",
            "monitor_transactions",
            "execute_contract",
            "verify_signature",
        ],
        dependencies=["web3.py", "eth-account"],
        execution_mode=ExecutionMode.SYNC,
        estimated_duration_ms=1000,
        philosophy_scores=PhilosophyScore(
            truth=100, goodness=90, beauty=85, serenity=90
        ),
    )

    # Skill 17: Data Pipeline
    skill_017 = AFOSkillCard(
        skill_id="skill_017_data_pipeline",
        name="Real-time Data Pipeline",
        description="Real-time collection of system friction, complexity, and metrics.",
        category=SkillCategory.HEALTH_MONITORING,
        tags=["data-pipeline", "real-time", "friction", "complexity", "metrics"],
        version="1.0.0",
        capabilities=[
            "ingest_logs",
            "calculate_friction",
            "track_complexity",
            "stream_metrics",
        ],
        dependencies=["kafka", "redis", "pandas"],
        execution_mode=ExecutionMode.STREAMING,
        estimated_duration_ms=100,
        philosophy_scores=PhilosophyScore(
            truth=98, goodness=95, beauty=90, serenity=97
        ),
    )

    # Skill 18: Docker Recovery (Sima Yi)
    skill_018 = AFOSkillCard(
        skill_id="skill_018_docker_recovery",
        name="Docker Auto-Recovery (Sima Yi)",
        description="Autonomous health monitoring and self-healing system.",
        category=SkillCategory.HEALTH_MONITORING,
        tags=["docker", "recovery", "self-healing", "sima-yi", "uptime"],
        version="1.0.0",
        capabilities=[
            "monitor_containers",
            "restart_container",
            "detect_deadlock",
            "analyze_logs",
        ],
        dependencies=["docker", "ai-analysis"],
        execution_mode=ExecutionMode.BACKGROUND,
        estimated_duration_ms=5000,
        philosophy_scores=PhilosophyScore(
            truth=99, goodness=100, beauty=85, serenity=100
        ),
    )

    # Skill 19: Hybrid GraphRAG
    skill_019 = AFOSkillCard(
        skill_id="skill_019_hybrid_graphrag",
        name="Hybrid GraphRAG",
        description="Combining Vector Search with Knowledge Graphs for deep context understanding.",
        category=SkillCategory.RAG_SYSTEMS,
        tags=["graph-rag", "knowledge-graph", "vector-search", "hybrid"],
        version="1.0.0",
        capabilities=[
            "graph_traversal",
            "entity_extraction",
            "relationship_mapping",
            "hybrid_search",
        ],
        dependencies=["neo4j", "chromadb", "langchain"],
        execution_mode=ExecutionMode.ASYNC,
        estimated_duration_ms=4000,
        philosophy_scores=PhilosophyScore(
            truth=97, goodness=95, beauty=92, serenity=90
        ),
    )

    # Skill 20: Auto Security Agent
    skill_020 = AFOSkillCard(
        skill_id="skill_020_auto_security",
        name="Auto Security Agent",
        description="Automated security patching and vulnerability scanning using Bandit.",
        category=SkillCategory.SECURITY,
        tags=["security", "bandit", "auto-patch", "vulnerability"],
        version="1.0.0",
        capabilities=["security_scan", "auto_patch", "vulnerability_report"],
        dependencies=["bandit", "safety"],
        execution_mode=ExecutionMode.ASYNC,
        estimated_duration_ms=10000,
        philosophy_scores=PhilosophyScore(
            truth=99, goodness=100, beauty=85, serenity=95
        ),
    )

    # Skill 21: Code Analysis Agent
    skill_021 = AFOSkillCard(
        skill_id="skill_021_code_analysis",
        name="Code Analysis Agent",
        description="Deep static code analysis and typing verification using Ruff and MyPy.",
        category=SkillCategory.CODE_ANALYSIS,
        tags=["code-analysis", "ruff", "mypy", "static-analysis"],
        version="1.0.0",
        capabilities=["lint_code", "type_check", "quality_report"],
        dependencies=["ruff", "mypy"],
        execution_mode=ExecutionMode.ASYNC,
        estimated_duration_ms=8000,
        philosophy_scores=PhilosophyScore(
            truth=100, goodness=95, beauty=90, serenity=90
        ),
    )

    # Skill 22: Dependency Audit
    skill_022 = AFOSkillCard(
        skill_id="skill_022_dependency_audit",
        name="Dependency Audit",
        description="Scans Python and Node.js dependencies for vulnerabilities.",
        category=SkillCategory.SECURITY,
        tags=["dependency", "audit", "cve", "npm", "pip"],
        version="1.0.0",
        capabilities=["scan_dependencies", "check_cve"],
        dependencies=["pip-audit", "npm-audit"],
        execution_mode=ExecutionMode.BACKGROUND,
        estimated_duration_ms=12000,
        philosophy_scores=PhilosophyScore(
            truth=98, goodness=100, beauty=80, serenity=95
        ),
    )

    # Skill 23: Secret Guardian
    skill_023 = AFOSkillCard(
        skill_id="skill_023_secret_guardian",
        name="Secret Guardian",
        description="Detects hardcoded secrets, keys, and tokens in the codebase.",
        category=SkillCategory.SECURITY,
        tags=["secrets", "leak-detection", "security", "keys"],
        version="1.0.0",
        capabilities=["scan_secrets", "verify_git_history"],
        dependencies=["trufflehog-lite"],
        execution_mode=ExecutionMode.ASYNC,
        estimated_duration_ms=5000,
        philosophy_scores=PhilosophyScore(
            truth=99, goodness=100, beauty=85, serenity=98
        ),
    )

    # Skill 24: Container Sentry
    skill_024 = AFOSkillCard(
        skill_id="skill_024_container_sentry",
        name="Container Sentry",
        description="Security scanning for Docker containers and images.",
        category=SkillCategory.SECURITY,
        tags=["docker", "container", "security", "image-scan"],
        version="1.0.0",
        capabilities=["scan_image", "check_config"],
        dependencies=["trivy-lite"],
        execution_mode=ExecutionMode.BACKGROUND,
        estimated_duration_ms=15000,
        philosophy_scores=PhilosophyScore(
            truth=97, goodness=100, beauty=80, serenity=95
        ),
    )

    # Skill 25: Dataset Optimizer
    skill_025 = AFOSkillCard(
        skill_id="skill_025_dataset_optimizer",
        name="Dataset Optimizer",
        description="Optimizes and prunes RAG datasets for efficiency.",
        category=SkillCategory.DATA_ENGINEERING,
        tags=["dataset", "optimization", "rag", "pruning"],
        version="1.0.0",
        capabilities=["deduplicate", "compress", "prune_outdated"],
        dependencies=["pandas", "numpy"],
        execution_mode=ExecutionMode.BACKGROUND,
        estimated_duration_ms=20000,
        philosophy_scores=PhilosophyScore(
            truth=100, goodness=90, beauty=95, serenity=90
        ),
    )

    # Skill 26: Vector Gardener
    skill_026 = AFOSkillCard(
        skill_id="skill_026_vector_gardener",
        name="Vector Gardener",
        description="Manages and re-indexes vector database for performance.",
        category=SkillCategory.DATA_ENGINEERING,
        tags=["vector-db", "lancedb", "reindex", "optimization"],
        version="1.0.0",
        capabilities=["reindex", "optimize_segments", "vacuum"],
        dependencies=["lancedb"],
        execution_mode=ExecutionMode.BACKGROUND,
        estimated_duration_ms=10000,
        philosophy_scores=PhilosophyScore(
            truth=99, goodness=90, beauty=95, serenity=95
        ),
    )

    # Skill 27: Latency Profiler
    skill_027 = AFOSkillCard(
        skill_id="skill_027_latency_profiler",
        name="Latency Profiler",
        description="Analyzes system latency and identifies bottlenecks.",
        category=SkillCategory.DEVOPS,
        tags=["latency", "profiling", "performance", "bottleneck"],
        version="1.0.0",
        capabilities=["profile_request", "analyze_trace"],
        dependencies=["pyinstrument"],
        execution_mode=ExecutionMode.SYNC,
        estimated_duration_ms=1000,
        philosophy_scores=PhilosophyScore(
            truth=100, goodness=85, beauty=90, serenity=90
        ),
    )

    # Skill 28: Energy Monitor
    skill_028 = AFOSkillCard(
        skill_id="skill_028_energy_monitor",
        name="Energy Monitor",
        description="Estimates computational carbon footprint and energy usage.",
        category=SkillCategory.SUSTAINABILITY,
        tags=["energy", "carbon", "sustainability", "green-ai"],
        version="1.0.0",
        capabilities=["calc_energy", "report_carbon"],
        dependencies=["codecarbon-lite"],
        execution_mode=ExecutionMode.ASYNC,
        estimated_duration_ms=500,
        philosophy_scores=PhilosophyScore(
            truth=95, goodness=100, beauty=90, serenity=100
        ),
    )

    # Skill 29: GenUI Expander
    skill_029 = AFOSkillCard(
        skill_id="skill_029_gen_ui_expander",
        name="GenUI Expander",
        description="Autonomously generates and refines React UI components.",
        category=SkillCategory.CREATIVE_AI,
        tags=["gen-ui", "react", "frontend", "auto-design"],
        version="1.0.0",
        capabilities=["generate_component", "refine_ui", "preview_render"],
        dependencies=["react-agent"],
        execution_mode=ExecutionMode.ASYNC,
        estimated_duration_ms=15000,
        philosophy_scores=PhilosophyScore(
            truth=90, goodness=95, beauty=100, serenity=95
        ),
    )

    # Skill 30: Chancellor Monitor
    skill_030 = AFOSkillCard(
        skill_id="skill_030_chancellor_monitor",
        name="Chancellor Monitor",
        description="Ensures all actions comply with AFO Constitution.",
        category=SkillCategory.GOVERNANCE,
        tags=["governance", "compliance", "constitution", "monitor"],
        version="1.0.0",
        capabilities=["audit_action", "verify_compliance", "log_verdict"],
        dependencies=["chancellor-core"],
        execution_mode=ExecutionMode.SYNC,
        estimated_duration_ms=200,
        philosophy_scores=PhilosophyScore(
            truth=100, goodness=100, beauty=95, serenity=100
        ),
    )

    core_skills = [
        skill_001,
        skill_002,
        skill_003,
        skill_004,
        skill_005,
        skill_006,
        skill_008,
        skill_009,
        skill_010,
        skill_011,
        skill_011_alt,
        skill_012,
        skill_013,
        skill_014,
        skill_015,
        skill_016,
        skill_017,
        skill_018,
        skill_019,
        skill_020,
        skill_021,
        skill_022,
        skill_023,
        skill_024,
        skill_025,
        skill_026,
        skill_027,
        skill_028,
        skill_029,
        skill_030,
    ]

    for skill in core_skills:
        registry.register(skill)

    return registry
