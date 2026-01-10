# Trinity Score: 90.0 (Established by Chancellor)
# afo_soul_engine/afo_skills_registry.py
"""
AFO Skill Registry System (2025 Standard)

Based on:
- Pydantic v2.12+ (Fail-fast validation, Pipeline API)
- MCP (Model Context Protocol) Integration
- FastAPI 0.115+ Query Parameter Models
- OpenAPI 3.1 Standards

Philosophy: 眞善美孝 (Truth, Goodness, Beauty, Serenity)
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Annotated, Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

# ============================================================================
# Enums & Constants
# ============================================================================


class SkillCategory(str, Enum):
    """Skill categories aligned with AFO architecture"""

    STRATEGIC_COMMAND = "strategic_command"  # LangGraph orchestration
    RAG_SYSTEMS = "rag_systems"  # Ultimate RAG, Trinity Loop, etc.
    WORKFLOW_AUTOMATION = "workflow_automation"  # n8n, Speckit
    HEALTH_MONITORING = "health_monitoring"  # 11-organ health
    MEMORY_MANAGEMENT = "memory_management"  # Redis, PostgreSQL, ChromaDB
    BROWSER_AUTOMATION = "browser_automation"  # Playwright
    ANALYSIS_EVALUATION = "analysis_evaluation"  # Ragas, Lyapunov
    INTEGRATION = "integration"  # External APIs, MCP
    METACOGNITION = "metacognition"  # Self-reflection, Vibe Coding
    SECURITY = "security"  # Security scanning & patching
    CODE_ANALYSIS = "code_analysis"  # Static analysis & linting
    DATA_ENGINEERING = "data_engineering"  # Data pipeline & optimization
    DEVOPS = "devops"  # CI/CD, Infrastructure, Profiling
    SUSTAINABILITY = "sustainability"  # Energy monitoring & Green AI
    CREATIVE_AI = "creative_ai"  # GenUI, Creative generation
    GOVERNANCE = "governance"  # Compliance, Constitution, Trinity Protocol


class SkillStatus(str, Enum):
    """Skill lifecycle status"""

    ACTIVE = "active"
    DEPRECATED = "deprecated"
    EXPERIMENTAL = "experimental"
    MAINTENANCE = "maintenance"


class ExecutionMode(str, Enum):
    """Skill execution modes"""

    SYNC = "sync"
    ASYNC = "async"
    STREAMING = "streaming"
    BACKGROUND = "background"


# ============================================================================
# Skill Execution Models
# ============================================================================


# ============================================================================
# Philosophy Score Model (眞善美孝)
# ============================================================================


class PhilosophyScore(BaseModel):
    """
    眞善美孝 philosophy alignment scores

    - 眞 (Truth): Technical certainty, provability (0-100)
    - 善 (Goodness): Ethical priority, stability (0-100)
    - 美 (Beauty): Clear storytelling, UX (0-100)
    - 孝 (Serenity): Frictionless operation (0-100)
    """

    model_config = ConfigDict(frozen=True)

    truth: Annotated[int, Field(ge=0, le=100, description="眞 (Truth) - Technical certainty")]
    goodness: Annotated[int, Field(ge=0, le=100, description="善 (Goodness) - Ethical priority")]
    beauty: Annotated[int, Field(ge=0, le=100, description="美 (Beauty) - Clear storytelling")]
    serenity: Annotated[
        int, Field(ge=0, le=100, description="孝 (Serenity) - Frictionless operation")
    ]

    @property
    def average(self) -> float:
        """Overall philosophy alignment score"""
        return (self.truth + self.goodness + self.beauty + self.serenity) / 4.0

    @property
    def summary(self) -> str:
        """Human-readable summary"""
        return f"眞{self.truth}% 善{self.goodness}% 美{self.beauty}% 孝{self.serenity}% (Avg: {self.average:.1f}%)"


# ============================================================================
# MCP Configuration
# ============================================================================


class MCPConfig(BaseModel):
    """MCP (Model Context Protocol) configuration for skill"""

    mcp_server_url: HttpUrl | None = Field(
        default=None, description="MCP server endpoint (if external)"
    )
    mcp_version: str = Field(default="2025.1", description="MCP protocol version")
    capabilities: list[str] = Field(
        default_factory=list,
        description="MCP capabilities (e.g., 'tools', 'prompts', 'resources')",
    )
    authentication_required: bool = Field(
        default=False, description="Whether MCP server requires authentication"
    )


# ============================================================================
# Skill Input/Output Schemas
# ============================================================================


class SkillParameter(BaseModel):
    """Single skill parameter definition"""

    name: str = Field(..., description="Parameter name")
    type: str = Field(..., description="Parameter type (e.g., 'string', 'int', 'list[str]')")
    description: str = Field(..., description="Parameter description")
    required: bool = Field(default=True, description="Whether parameter is required")
    default: Any | None = Field(default=None, description="Default value if not required")
    validation_rules: dict[str, Any] | None = Field(
        default=None, description="Validation rules (e.g., {'min': 0, 'max': 100})"
    )


class SkillIOSchema(BaseModel):
    """Input/Output schema for skill"""

    parameters: list[SkillParameter] = Field(default_factory=list, description="List of parameters")
    example: dict[str, Any] | None = Field(default=None, description="Example input/output")


# ============================================================================
# Skill Card (Main Model)
# ============================================================================


class AFOSkillCard(BaseModel):
    """
    AFO Skill Card - Complete skill metadata

    Aligned with:
    - MCP AgentCard standard
    - OpenAPI 3.1 component schema
    - 2025 AI agent registry best practices
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "skill_id": "skill_001_youtube_spec_gen",
                "name": "YouTube to n8n Spec Generator",
                "description": "Converts YouTube tutorial transcripts to n8n workflow specs",
                "category": "workflow_automation",
                "version": "1.0.0",
                "capabilities": [
                    "youtube_transcript_extraction",
                    "llm_spec_generation",
                    "n8n_workflow_creation",
                ],
                "philosophy_scores": {
                    "truth": 95,
                    "goodness": 90,
                    "beauty": 92,
                    "serenity": 88,
                },
            }
        }
    )

    # Core Identity
    skill_id: str = Field(
        ...,
        description="Unique skill identifier (e.g., 'skill_001_youtube_spec_gen')",
        pattern=r"^skill_\d{3}_[a-z0-9_]+$",
    )
    name: str = Field(..., description="Human-readable skill name", min_length=3, max_length=100)
    description: str = Field(
        ..., description="Detailed skill description", min_length=10, max_length=1000
    )

    # Classification
    category: SkillCategory = Field(..., description="Skill category")
    tags: list[str] = Field(default_factory=list, description="Searchable tags", max_length=20)

    # Versioning & Status
    version: str = Field(
        ..., description="Semantic version (e.g., '1.0.0')", pattern=r"^\d+\.\d+\.\d+$"
    )
    status: SkillStatus = Field(default=SkillStatus.ACTIVE, description="Skill lifecycle status")

    # Capabilities & Dependencies
    capabilities: list[str] = Field(
        default_factory=list, description="List of skill capabilities", max_length=50
    )
    dependencies: list[str] = Field(
        default_factory=list,
        description="Required dependencies (skill_ids or package names)",
        max_length=30,
    )

    # Execution Configuration
    execution_mode: ExecutionMode = Field(
        default=ExecutionMode.ASYNC, description="How the skill executes"
    )
    endpoint: HttpUrl | None = Field(
        default=None, description="API endpoint for skill execution (if applicable)"
    )
    estimated_duration_ms: int | None = Field(
        default=None, ge=0, description="Estimated execution time in milliseconds"
    )
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Default configuration parameters"
    )

    # Input/Output Schemas
    input_schema: SkillIOSchema = Field(
        default_factory=SkillIOSchema, description="Input parameters schema"
    )
    output_schema: SkillIOSchema = Field(default_factory=SkillIOSchema, description="Output schema")

    # Philosophy Alignment
    philosophy_scores: PhilosophyScore = Field(
        ..., description="眞善美孝 philosophy alignment scores"
    )

    # MCP Integration
    mcp_config: MCPConfig | None = Field(
        default=None, description="MCP configuration (if MCP-compatible)"
    )

    # Metadata
    author: str = Field(default="AFO Kingdom", description="Skill author/maintainer")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Skill creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Last update timestamp"
    )
    documentation_url: HttpUrl | None = Field(
        default=None, description="Link to detailed documentation"
    )

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: list[str]) -> list[str]:
        """Ensure tags are lowercase and unique"""
        return list({tag.lower().strip() for tag in v})

    @field_validator("capabilities")
    @classmethod
    def validate_capabilities(cls, v: list[str]) -> list[str]:
        """Ensure capabilities are unique"""
        return list(set(v))


# ============================================================================
# Skill Execution Models
# ============================================================================


class SkillExecutionRequest(BaseModel):
    """
    Request model for executing a skill.
    """

    skill_id: str = Field(..., description="ID of the skill to execute")
    parameters: dict[str, Any] = Field(default_factory=dict, description="Execution parameters")
    dry_run: bool = Field(False, description="If True, simulate execution without side effects")
    # Deprecated fields (kept for compatibility if needed, but defaults provided)
    context: dict[str, Any] | None = Field(default=None, description="Additional execution context")
    async_execution: bool = Field(default=False, description="Whether to execute asynchronously")


class SkillExecutionResult(BaseModel):
    """
    Result model for skill execution.
    """

    skill_id: str
    status: str
    result: dict[str, Any]
    dry_run: bool
    error: str | None = None

    # Legacy fields support (optional)
    success: bool = Field(default=True, description="Legacy success flag")
    execution_time_ms: int = Field(default=0, description="Execution time")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# Filter Models (FastAPI 0.115 Query Parameter Models)
# ============================================================================


class SkillFilterParams(BaseModel):
    """
    Query parameters for filtering skills

    Uses FastAPI 0.115+ Pydantic Query Parameter Models
    """

    category: SkillCategory | None = Field(default=None, description="Filter by category")
    status: SkillStatus | None = Field(default=None, description="Filter by status")
    tags: list[str] | None = Field(default=None, description="Filter by tags (OR logic)")
    search: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
        description="Search in name/description",
    )
    min_philosophy_avg: int | None = Field(
        default=None, ge=0, le=100, description="Minimum average philosophy score"
    )
    execution_mode: ExecutionMode | None = Field(
        default=None, description="Filter by execution mode"
    )
    limit: int = Field(default=100, ge=1, le=500, description="Maximum results")
    offset: int = Field(default=0, ge=0, description="Pagination offset")


# ============================================================================
# Skill Registry (Singleton)
# ============================================================================


class SkillRegistry:
    """
    Central skill registry for AFO system

    Pattern: Singleton with in-memory storage + optional persistence
    """

    _instance = None
    _skills: ClassVar[dict[str, AFOSkillCard]] = {}

    def __new__(cls) -> Any:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register(self, skill: AFOSkillCard) -> bool:
        """Register a skill"""
        try:
            if skill.skill_id in self._skills:
                # Update existing skill
                self._skills[skill.skill_id] = skill
                return False  # Not a new registration
            else:
                self._skills[skill.skill_id] = skill
                return True  # New registration
        except Exception:
            return False

    def get(self, skill_id: str) -> AFOSkillCard | None:
        """Get skill by ID"""
        try:
            return self._skills.get(skill_id)
        except Exception:
            return None

    def list_all(self) -> list[AFOSkillCard]:
        """List all skills"""
        try:
            return list(self._skills.values())
        except Exception:
            return []

    def filter(self, params: SkillFilterParams) -> list[AFOSkillCard]:
        """Filter skills by parameters"""
        try:
            results = self.list_all()

            # Category filter
            if params.category:
                results = [s for s in results if s.category == params.category]

            # Status filter
            if params.status:
                results = [s for s in results if s.status == params.status]

            # Tags filter (OR logic)
            if params.tags:
                tag_set = {tag.lower() for tag in params.tags}
                results = [s for s in results if any(tag in tag_set for tag in s.tags)]

            # Search filter
            if params.search:
                search_lower = params.search.lower()
                results = [
                    s
                    for s in results
                    if search_lower in s.name.lower() or search_lower in s.description.lower()
                ]

            # Philosophy score filter
            if params.min_philosophy_avg:
                results = [
                    s for s in results if s.philosophy_scores.average >= params.min_philosophy_avg
                ]

            # Execution mode filter
            if params.execution_mode:
                results = [s for s in results if s.execution_mode == params.execution_mode]

            # Pagination
            start = params.offset
            end = params.offset + params.limit
            return results[start:end]
        except Exception as e:
            print(f"⚠️ Skill filtering failed: {e}")
            return []

    def get_categories(self) -> list[str]:
        """Get all unique categories"""
        try:
            return [cat.value for cat in SkillCategory]
        except Exception:
            return []

    def get_category_stats(self) -> dict[str, int]:
        """Get category statistics (category -> count)"""
        try:
            stats: dict[str, int] = {}
            for skill in self._skills.values():
                category = skill.category.value
                if category not in stats:
                    stats[category] = 0
                stats[category] += 1
            return stats
        except Exception:
            return {}

    def count(self) -> int:
        """Total skill count"""
        return len(self._skills)

    def clear(self) -> None:
        """Clear all skills (for testing)"""
        self._skills.clear()

    @property
    def skills(self) -> dict[str, AFOSkillCard]:
        """Expose registry storage for backwards compatibility"""
        return self._skills


# ============================================================================
# Pre-defined Skills (AFO Core Skills)
# ============================================================================


def _get_mcp_server_url() -> str | None:
    """Helper to get MCP server URL from environment"""
    # Phase 2-4: settings 사용
    # Phase 2-4: settings 사용
    try:
        from AFO.config.settings import get_settings

        settings = get_settings()
        return settings.MCP_SERVER_URL
    except Exception:
        import os

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
        # [노자] 무위이치 - 동적 설정은 무위자연의 원리로
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
            truth=95,  # Provable spec generation
            goodness=90,  # Reliable, stable
            beauty=92,  # Clean JSON output
            serenity=88,  # Minimal user intervention
        ),
        mcp_config=MCPConfig(
            mcp_server_url=_get_mcp_server_url(),  # type: ignore
            capabilities=["transcript_extraction"],
        ),
        documentation_url="https://github.com/lofibrainwav/AFO/blob/main/docs/skills/youtube-spec-gen.md",  # type: ignore
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
            truth=98,  # Lyapunov-proven
            goodness=95,  # Stable, no hallucinations
            beauty=90,  # Clean retrieval
            serenity=92,  # Auto-converges
        ),
        documentation_url="https://github.com/lofibrainwav/AFO/blob/main/afo_soul_engine/hybrid_crag_selfrag.py",  # type: ignore
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
            truth=100,  # Measurable health metrics
            goodness=100,  # Critical for stability
            beauty=95,  # Clear reporting
            serenity=100,  # Hands-free monitoring
        ),
        documentation_url="https://github.com/lofibrainwav/AFO/blob/main/afo_soul_engine/auto_health_monitor.py",  # type: ignore
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
            truth=99,  # Scientific metrics
            goodness=92,  # Prevents hallucinations
            beauty=88,  # Clear scores
            serenity=85,  # Requires API calls
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
            truth=96,  # Deterministic routing
            goodness=94,  # Stable state management
            beauty=93,  # Clean graph design
            serenity=95,  # Minimal resource usage
        ),
        documentation_url="https://github.com/lofibrainwav/AFO/blob/main/afo_soul_engine/strategy_engine.py",  # type: ignore
    )

    # Skill 6: ML Metacognition Upgrade (Phase 3)
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
            truth=95,  # Mathematical proof
            goodness=94,  # Gap reduction
            beauty=92,  # Clean iteration
            serenity=93,  # Stable convergence
        ),
    )

    # Skill 8: Soul Refine (Vibe Alignment)
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
            truth=94,  # Mathematical alignment
            goodness=95,  # User satisfaction
            beauty=97,  # Aesthetic refinement
            serenity=96,  # Harmonious output
        ),
    )

    # Skill 9: Advanced Cosine Similarity (4 Advanced Techniques)
    skill_009 = AFOSkillCard(
        skill_id="skill_009_advanced_cosine",
        name="Advanced Cosine Similarity (4 Techniques)",
        description="4 advanced cosine similarity techniques: Weighted (gap 30% ↓), Sparse (5x speed), Embedding (768D BERT), sqrt (stability 10% ↑)",
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
            truth=97,  # Advanced mathematical techniques
            goodness=96,  # Gap improvement 15%+
            beauty=93,  # 4 clean implementations
            serenity=95,  # Enhanced taste alignment
        ),
    )

    # Skill 10: Family Persona Manager (Yeongdeok, Sima Yi, etc.)
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
            truth=92,  # Consistent personas
            goodness=94,  # Respectful interactions
            beauty=96,  # Engaging dialogue
            serenity=95,  # smooth roleplay
        ),
    )

    # Skill 11: Verify Full Stack (Consolidated)
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
        philosophy_scores=PhilosophyScore(truth=99, goodness=98, beauty=90, serenity=95),
    )

    # Continue with Skill 11 definitions...

    # Skill 11: AFO DevTool Belt (Veteran's Weapons)
    skill_011 = AFOSkillCard(
        skill_id="skill_011_dev_tool_belt",
        name="AFO DevTool Belt",
        description="Essential development tools for agents: Linting (Ruff), Testing (Pytest), Git, and Docker management",
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
            truth=98,  # Enforces code correctness
            goodness=95,  # Maintains system hygiene
            beauty=90,  # Clean code
            serenity=97,  # Automated maintenance
        ),
    )

    # Skill 12: MCP Tool Bridge (Universal Map)
    skill_012 = AFOSkillCard(
        skill_id="skill_012_mcp_tool_bridge",
        name="MCP Tool Bridge",
        description="Universal bridge to connect and utilize any external MCP (Model Context Protocol) server tools",
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
            truth=95,  # Standardized protocol
            goodness=99,  # Infinite extensibility
            beauty=96,  # Universal interface
            serenity=94,  # Seamless integration
        ),
        mcp_config=MCPConfig(mcp_version="2024.11.1", capabilities=["tools", "resources"]),
    )

    # Skill 13: AFO Obsidian Librarian (The Kingdom's Library)
    skill_013 = AFOSkillCard(
        skill_id="skill_013_obsidian_librarian",
        name="AFO Obsidian Librarian",
        description="Manages the Kingdom's Knowledge in Obsidian. Reads/Writes notes, manages Daily Notes, and creates bi-directional links.",
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
            truth=96,  # Persistent knowledge
            goodness=98,  # Accessible wisdom
            beauty=95,  # Structured organization
            serenity=99,  # Water-like flow
        ),
    )

    # Skill 14: Strangler Fig Integrator (Frontend Unification)
    skill_014 = AFOSkillCard(
        skill_id="skill_014_strangler_integrator",
        name="Strangler Fig Integrator",
        description="Unifies isolated services (n8n, LangFlow) into the Gateway (Port 3000) using the Strangler Fig pattern.",
        category=SkillCategory.INTEGRATION,
        tags=["strangler", "integration", "frontend", "n8n", "langflow"],
        version="1.0.0",
        capabilities=["proxy_service", "check_integration_health", "iframe_bridge"],
        dependencies=["react", "iframe"],
        execution_mode=ExecutionMode.SYNC,
        estimated_duration_ms=200,
        philosophy_scores=PhilosophyScore(
            truth=95,  # Unified access
            goodness=99,  # User convenience
            beauty=94,  # Seamless UI
            serenity=98,  # One URL to rule them all
        ),
    )

    # Skill 15: Suno AI Music Composer
    skill_015 = AFOSkillCard(
        skill_id="skill_015_suno_composer",
        name="Suno AI Music Composer",
        description="Generates high-quality music and lyrics using Suno AI. Handles generation, polling, and downloading.",
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
            truth=85,  # Creative generation
            goodness=90,  # Joyful output
            beauty=100,  # Pure artistic expression
            serenity=95,  # Automated creativity
        ),
    )

    # Skill 16: Web3 Blockchain Manager
    skill_016 = AFOSkillCard(
        skill_id="skill_016_web3_manager",
        name="Web3 Blockchain Manager",
        description="Manages blockchain interactions, wallet monitoring, and smart contract execution for the Kingdom's assets.",
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
            truth=100,  # Cryptographic certainty
            goodness=90,  # Transparent ledger
            beauty=85,  # Elegant math
            serenity=90,  # Trustless verification
        ),
    )

    # Skill 17: Real-time Data Pipeline
    skill_017 = AFOSkillCard(
        skill_id="skill_017_data_pipeline",
        name="Real-time Data Pipeline",
        description="Real-time collection and processing of system friction, complexity, and observer metrics (Roadmap S3-P2).",
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
            truth=98,  # Real-time accuracy
            goodness=95,  # Early warning system
            beauty=90,  # Flowing data
            serenity=97,  # Constant vigilance
        ),
    )

    # Skill 18: Docker Auto-Recovery (Sima Yi)
    skill_018 = AFOSkillCard(
        skill_id="skill_018_docker_recovery",
        name="Docker Auto-Recovery (Sima Yi)",
        description="Autonomous container health monitoring and self-healing system. Ensures 99.9% uptime (Roadmap S3-P1).",
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
            truth=99,  # Reliable recovery
            goodness=100,  # System survival
            beauty=85,  # Resilient architecture
            serenity=100,  # Sleep well at night
        ),
    )

    # Skill 19: Hybrid GraphRAG
    skill_019 = AFOSkillCard(
        skill_id="skill_019_hybrid_graphrag",
        name="Hybrid GraphRAG",
        description="Advanced knowledge retrieval combining Vector Search with Knowledge Graphs for deep context understanding (Roadmap S4-P3).",
        category=SkillCategory.RAG_SYSTEMS,
        tags=[
            "graph-rag",
            "knowledge-graph",
            "vector-search",
            "hybrid",
            "deep-context",
        ],
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
            truth=97,  # Structured knowledge
            goodness=95,  # Deep understanding
            beauty=92,  # Connected insights
            serenity=90,  # Comprehensive answers
        ),
    )

    # Skill 20: Auto Security Agent (Bandit/Safety)
    skill_020 = AFOSkillCard(
        skill_id="skill_020_auto_security",
        name="Auto Security Agent",
        description="Automated security patching and vulnerability scanning using Bandit and Safety (Phase 1).",
        category=SkillCategory.SECURITY,
        tags=["security", "bandit", "auto-patch", "vulnerability"],
        version="1.0.0",
        capabilities=["security_scan", "auto_patch", "vulnerability_report"],
        dependencies=["bandit", "safety"],
        execution_mode=ExecutionMode.ASYNC,
        estimated_duration_ms=10000,
        philosophy_scores=PhilosophyScore(truth=99, goodness=100, beauty=85, serenity=95),
    )

    # Skill 21: Code Analysis Agent (Ruff/MyPy)
    skill_021 = AFOSkillCard(
        skill_id="skill_021_code_analysis",
        name="Code Analysis Agent",
        description="Deep static code analysis and typing verification using Ruff and MyPy (Phase 1).",
        category=SkillCategory.CODE_ANALYSIS,
        tags=["code-analysis", "ruff", "mypy", "static-analysis"],
        version="1.0.0",
        capabilities=["lint_code", "type_check", "quality_report"],
        dependencies=["ruff", "mypy"],
        execution_mode=ExecutionMode.ASYNC,
        estimated_duration_ms=8000,
        philosophy_scores=PhilosophyScore(truth=100, goodness=95, beauty=90, serenity=90),
    )

    # Skill 22: Dependency Audit
    skill_022 = AFOSkillCard(
        skill_id="skill_022_dependency_audit",
        name="Dependency Audit",
        description="Scans Python and Node.js dependencies for known vulnerabilities (Phase 1).",
        category=SkillCategory.SECURITY,
        tags=["dependency", "audit", "cve", "npm", "pip"],
        version="1.0.0",
        capabilities=["scan_dependencies", "check_cve"],
        dependencies=["pip-audit", "npm-audit"],
        execution_mode=ExecutionMode.BACKGROUND,
        estimated_duration_ms=12000,
        philosophy_scores=PhilosophyScore(truth=98, goodness=100, beauty=80, serenity=95),
    )

    # Skill 23: Secret Guardian
    skill_023 = AFOSkillCard(
        skill_id="skill_023_secret_guardian",
        name="Secret Guardian",
        description="Detects hardcoded secrets, keys, and tokens in the codebase (Phase 1).",
        category=SkillCategory.SECURITY,
        tags=["secrets", "leak-detection", "security", "keys"],
        version="1.0.0",
        capabilities=["scan_secrets", "verify_git_history"],
        dependencies=["trufflehog-lite"],
        execution_mode=ExecutionMode.ASYNC,
        estimated_duration_ms=5000,
        philosophy_scores=PhilosophyScore(truth=99, goodness=100, beauty=85, serenity=98),
    )

    # Skill 24: Container Sentry
    skill_024 = AFOSkillCard(
        skill_id="skill_024_container_sentry",
        name="Container Sentry",
        description="Security scanning for Docker containers and images (Phase 1).",
        category=SkillCategory.SECURITY,
        tags=["docker", "container", "security", "image-scan"],
        version="1.0.0",
        capabilities=["scan_image", "check_config"],
        dependencies=["trivy-lite"],
        execution_mode=ExecutionMode.BACKGROUND,
        estimated_duration_ms=15000,
        philosophy_scores=PhilosophyScore(truth=97, goodness=100, beauty=80, serenity=95),
    )

    # Skill 25: Dataset Optimizer
    skill_025 = AFOSkillCard(
        skill_id="skill_025_dataset_optimizer",
        name="Dataset Optimizer",
        description="Optimizes and prunes RAG datasets for efficiency (Phase 2).",
        category=SkillCategory.DATA_ENGINEERING,
        tags=["dataset", "optimization", "rag", "pruning"],
        version="1.0.0",
        capabilities=["deduplicate", "compress", "prune_outdated"],
        dependencies=["pandas", "numpy"],
        execution_mode=ExecutionMode.BACKGROUND,
        estimated_duration_ms=20000,
        philosophy_scores=PhilosophyScore(truth=100, goodness=90, beauty=95, serenity=90),
    )

    # Skill 26: Vector Gardener
    skill_026 = AFOSkillCard(
        skill_id="skill_026_vector_gardener",
        name="Vector Gardener",
        description="Manages and re-indexes vector database for optimal performance (Phase 2).",
        category=SkillCategory.DATA_ENGINEERING,
        tags=["vector-db", "lancedb", "reindex", "optimization"],
        version="1.0.0",
        capabilities=["reindex", "optimize_segments", "vacuum"],
        dependencies=["lancedb"],
        execution_mode=ExecutionMode.BACKGROUND,
        estimated_duration_ms=10000,
        philosophy_scores=PhilosophyScore(truth=99, goodness=90, beauty=95, serenity=95),
    )

    # Skill 27: Latency Profiler
    skill_027 = AFOSkillCard(
        skill_id="skill_027_latency_profiler",
        name="Latency Profiler",
        description="Analyzes system latency and identifies bottlenecks (Phase 3).",
        category=SkillCategory.DEVOPS,
        tags=["latency", "profiling", "performance", "bottleneck"],
        version="1.0.0",
        capabilities=["profile_request", "analyze_trace"],
        dependencies=["pyinstrument"],
        execution_mode=ExecutionMode.SYNC,
        estimated_duration_ms=1000,
        philosophy_scores=PhilosophyScore(truth=100, goodness=85, beauty=90, serenity=90),
    )

    # Skill 28: Energy Monitor
    skill_028 = AFOSkillCard(
        skill_id="skill_028_energy_monitor",
        name="Energy Monitor",
        description="Estimates computational carbon footprint and energy usage (Phase 4).",
        category=SkillCategory.SUSTAINABILITY,
        tags=["energy", "carbon", "sustainability", "green-ai"],
        version="1.0.0",
        capabilities=["calc_energy", "report_carbon"],
        dependencies=["codecarbon-lite"],
        execution_mode=ExecutionMode.ASYNC,
        estimated_duration_ms=500,
        philosophy_scores=PhilosophyScore(truth=95, goodness=100, beauty=90, serenity=100),
    )

    # Skill 29: GenUI Expander
    skill_029 = AFOSkillCard(
        skill_id="skill_029_gen_ui_expander",
        name="GenUI Expander",
        description="Autonomously generates and refines React UI components (Phase 5).",
        category=SkillCategory.CREATIVE_AI,
        tags=["gen-ui", "react", "frontend", "auto-design"],
        version="1.0.0",
        capabilities=["generate_component", "refine_ui", "preview_render"],
        dependencies=["react-agent"],
        execution_mode=ExecutionMode.ASYNC,
        estimated_duration_ms=15000,
        philosophy_scores=PhilosophyScore(truth=90, goodness=95, beauty=100, serenity=95),
    )

    # Skill 30: Chancellor Monitor
    skill_030 = AFOSkillCard(
        skill_id="skill_030_chancellor_monitor",
        name="Chancellor Monitor",
        description="Ensures all system actions comply with AFO Constitution and Trinity Protocol (Governance).",
        category=SkillCategory.GOVERNANCE,
        tags=["governance", "compliance", "constitution", "monitor"],
        version="1.0.0",
        capabilities=["audit_action", "verify_compliance", "log_verdict"],
        dependencies=["chancellor-core"],
        execution_mode=ExecutionMode.SYNC,
        estimated_duration_ms=200,
        philosophy_scores=PhilosophyScore(truth=100, goodness=100, beauty=95, serenity=100),
    )

    skills = [
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
        skill_012,
        skill_013,
        skill_014,
        skill_015,
        skill_016,
        skill_017,
        skill_018,
        skill_019,
        # Phase 1 Expansion (Security & Analysis)
        skill_020,
        skill_021,
        skill_022,
        skill_023,
        skill_024,
        # Phase 2 Expansion (Data)
        skill_025,
        skill_026,
        # Phase 3 Expansion (Hardware/Perf)
        skill_027,
        # Phase 4 Expansion (Sustainability)
        skill_028,
        # Phase 5 Expansion (Self-Evolution)
        skill_029,
        # Governance
        skill_030,
    ]

    for skill in skills:
        registry.register(skill)

    return registry


# [논어] 과유불급 - 지나침은 모자람과 같으니, 중복된 코드는 제거함
# (Removed duplicate skill_015 definition and second registration loop - unreachable code after return)


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "AFOSkillCard",
    # Registry
    "AFOSkillCard",
    "ExecutionMode",
    "MCPConfig",
    # Models
    "PhilosophyScore",
    # Enums
    "SkillCategory",
    "SkillExecutionRequest",
    "SkillExecutionRequest",
    "SkillExecutionResult",
    "SkillExecutionResult",
    "SkillFilterParams",
    "SkillFilterParams",
    "SkillIOSchema",
    "SkillParameter",
    "register_core_skills",
]

# ============================================================================
# Manual Skill Registration (for new skills)
# ============================================================================

# Manually register verify_full_stack skill
try:
    registry = SkillRegistry()
    registry.register(
        AFOSkillCard(
            skill_id="skill_020_verify_full_stack",
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
            philosophy_scores=PhilosophyScore(truth=99, goodness=98, beauty=90, serenity=95),
        )
    )
except Exception:
    pass  # Silent failure for optional skill


# ============================================================================
# Self-Test
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("AFO Skill Registry System - Self-Test")
    print("=" * 70)

    # Register core skills
    registry = register_core_skills()

    # Test 1: List all skills
    print(f"\n📋 Total skills registered: {registry.count()}")
    for skill in registry.list_all():
        print(f"  - {skill.skill_id}: {skill.name} ({skill.category.value})")
        print(f"    Philosophy: {skill.philosophy_scores.summary}")

    # Test 2: Filter by category
    print("\n🔍 Filter: RAG Systems")
    rag_skills = registry.filter(SkillFilterParams(category=SkillCategory.RAG_SYSTEMS))
    for skill in rag_skills:
        print(f"  - {skill.name}")

    # Test 3: Search
    print("\n🔍 Search: 'health'")
    health_skills = registry.filter(SkillFilterParams(search="health"))
    for skill in health_skills:
        print(f"  - {skill.name}")

    # Test 4: High philosophy score filter
    print("\n🔍 Filter: Philosophy avg >= 95%")
    high_phil_skills = registry.filter(SkillFilterParams(min_philosophy_avg=95))
    for skill in high_phil_skills:
        print(f"  - {skill.name} (Avg: {skill.philosophy_scores.average:.1f}%)")

    # Test 5: Export as JSON
    print("\n📄 Sample Skill Card (JSON):")
    sample_skill = registry.get("skill_001_youtube_spec_gen")
    if sample_skill:
        import json

        print(json.dumps(sample_skill.model_dump(), indent=2, default=str))

    print("\n✅ Self-test completed successfully!")

# Rebuild models to resolve deferred types (Pydantic V2 + __future__.annotations)
try:
    SkillExecutionRequest.model_rebuild()
    SkillExecutionResult.model_rebuild()
    AFOSkillCard.model_rebuild()
except Exception:
    pass
