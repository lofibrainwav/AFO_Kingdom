import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    import redis
    from watchdog.events import FileSystemEventHandler

from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

# ============================================================================
# AGENTS.md 통합 상수 (SSOT)
# ============================================================================

# AGENTS.md 파일 경로 (루트 기준)
# packages/afo-core/config/antigravity.py -> ... -> AFO_Kingdom/AGENTS.md
# .parent(config) -> .parent(afo-core) -> .parent(packages) -> .parent(AFO_Kingdom)
AGENTS_MD_PATH = Path(__file__).resolve().parent.parent.parent.parent / "AGENTS.md"

# Trinity Score 가중치 (AGENTS.md Ⅲ. 5기둥 철학 및 SSOT 가중치)
# Truth(35%), Goodness(35%), Beauty(20%), Serenity(8%), Eternity(2%)
AGENTS_MD_TRINITY_WEIGHTS = {
    "truth": 0.35,
    "goodness": 0.35,
    "beauty": 0.20,
    "serenity": 0.08,
    "eternity": 0.02,
}

# AUTO_RUN 조건 (AGENTS.md Rule #1)
AGENTS_MD_AUTO_RUN_TRINITY_THRESHOLD = 90
AGENTS_MD_AUTO_RUN_RISK_THRESHOLD = 10

# Risk Score 가이드 (AGENTS.md Ⅵ. Risk Score 가이드)
AGENTS_MD_RISK_SCORE_GUIDE = {
    "auth_payment_secrets_prod": 60,
    "db_data_irreversible": 40,
    "dependency_large_refactor": 30,
    "core_logic_no_test": 25,
    "doc_small_bug_ui": 5,
}


class AntiGravitySettings(BaseSettings):
    """
    AntiGravity 중앙 설정 클래스 - 모든 마찰 제거를 위한 통합 포인트
    Truth (眞): 타입 안전성 및 명시적 설정
    Goodness (善): DRY_RUN 기본값으로 안전 우선
    Beauty (美): 간결한 설정 인터페이스
    Serenity (孝): 자동화로 운영 마찰 제거

    [AGENTS.md 통합]
    - AGENTS.md 파일 경로: AGENTS_MD_PATH
    - Trinity Score 가중치: AGENTS_MD_TRINITY_WEIGHTS
    - AUTO_RUN 조건: AGENTS_MD_AUTO_RUN_TRINITY_THRESHOLD, AGENTS_MD_AUTO_RUN_RISK_THRESHOLD
    - Risk Score 가이드: AGENTS_MD_RISK_SCORE_GUIDE
    """

    ENVIRONMENT: Literal["dev", "prod", "test"] = "dev"  # 환경 자동 감지
    AUTO_DEPLOY: bool = True  # 자동 배포 활성화 (孝: 운영 마찰 제거)
    DRY_RUN_DEFAULT: bool = True  # 기본 DRY_RUN (善: 안전 우선)
    CENTRAL_CONFIG_SYNC: bool = True  # 중앙 설정 동기화 (永: 영속성)
    AUTO_SYNC: bool = True  # 자동 동기화 활성화 (孝: 설정 마찰 제거)
    SELF_EXPANDING_MODE: bool = True  # 자율 확장 모드 (永: 창조자 트랙 활성화)

    # [Phase A] 언어 정책 설정 (SSOT)
    REPORT_LANGUAGE: Literal["ko", "en"] = os.getenv(
        "REPORT_LANGUAGE", "ko"
    )  # 기본값: ko (왕국 SSOT 협업 기준)
    USE_PROTOCOL_OFFICER: bool = True  # Protocol Officer 사용 여부

    # [AGENTS.md 통합] AGENTS.md 파일 존재 확인
    @property
    def agents_md_exists(self) -> bool:
        """AGENTS.md 파일 존재 여부 확인"""
        return AGENTS_MD_PATH.exists()

    @property
    def agents_md_path(self) -> Path:
        """AGENTS.md 파일 경로 반환"""
        return AGENTS_MD_PATH

    @property
    def trinity_weights(self) -> dict[str, float]:
        """Trinity Score 가중치 반환 (AGENTS.md SSOT)"""
        return AGENTS_MD_TRINITY_WEIGHTS.copy()

    @property
    def auto_run_trinity_threshold(self) -> int:
        """AUTO_RUN Trinity Score 임계값 (AGENTS.md Rule #1)"""
        return AGENTS_MD_AUTO_RUN_TRINITY_THRESHOLD

    @property
    def auto_run_risk_threshold(self) -> int:
        """AUTO_RUN Risk Score 임계값 (AGENTS.md Rule #1)"""
        return AGENTS_MD_AUTO_RUN_RISK_THRESHOLD

    @property
    def risk_score_guide(self) -> dict[str, int]:
        """Risk Score 가이드 반환 (AGENTS.md Ⅵ)"""
        return AGENTS_MD_RISK_SCORE_GUIDE.copy()

    # [NEW] Phase 0: Logging Level Enforcement (眞: 관찰 강화)
    @property
    def LOG_LEVEL(self) -> str:
        return "DEBUG" if self.ENVIRONMENT == "dev" else "INFO"

    class Config:
        env_file = ".env.antigravity"  # 별도 env 파일로 마찰 최소화
        case_sensitive = False
        extra = "allow"

    def auto_sync(self) -> str:
        """
        자동 동기화 실행 (孝: Serenity) - Hot Reload Implementation

        Reads .env.antigravity and updates the singleton instance in-place.
        """
        if not self.AUTO_SYNC:
            return "[孝: 자동 동기화] 비활성화됨"

        try:
            # 1. Create a fresh instance to read new env values
            new_settings = AntiGravitySettings(_env_file=".env.antigravity")

            # 2. Update current instance attributes
            # effectively becoming the new settings while keeping the same object reference
            changes = []
            for key, value in new_settings.model_dump().items():
                old_value = getattr(self, key, None)
                if old_value != value:
                    setattr(self, key, value)
                    changes.append(f"{key}: {old_value} -> {value}")

            if changes:
                log_msg = f"[孝: 자동 동기화] 설정 업데이트 완료: {', '.join(changes)}"
                logger.info(log_msg)
                return log_msg
            else:
                return "[孝: 자동 동기화] 변경사항 없음"

        except Exception as e:
            err_msg = f"[孝: 자동 동기화] 실패: {e}"
            logger.error(err_msg)
            return err_msg

    def _get_redis_conn(self) -> "redis.Redis":
        """Helper for test mocking"""
        import redis

        try:
            from AFO.config.settings import get_settings

            redis_url = get_settings().get_redis_url()
        except ImportError:
            redis_url = "redis://localhost:6379"

        from typing import cast

        return cast(
            "redis.Redis",
            redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=1,
                socket_timeout=1,
            ),
        )

    def _calculate_risk_score(self, key: str, context: dict | None = None) -> float:
        """
        [Goodness] 사마의(善) 리스크 평가 모델 (Mock)

        Args:
            key: 기능/액션 키
            context: 컨텍스트 데이터

        Returns:
            float: 리스크 점수 (0-100)
        """
        # TODO: 실제 사마의 로직 연동 or Trinity Score 연동
        # 현재는 보수적으로 5.0 (안전) 리턴, 특정 키워드에 대해 높임
        if "delete" in key.lower() or "drop" in key.lower():
            return 80.0  # 위험
        if "deploy" in key.lower():
            return 20.0  # 주의
        return 5.0

    def check_governance(
        self, key: str, user_id: str | None = None, context: dict | None = None
    ) -> bool:
        """
        [Pure Governance] 통합 거버넌스 체크 (眞·善·美)

        1. Truth: Feature Flag 확인
        2. Goodness: Risk Score 확인 (>10 이면 Block)
        3. Eternity: DRY_RUN 모드 확인
        """
        # 1. Feature Flag (Truth)
        if not self.get_feature_flag(key, user_id):
            logger.info(f"⛔ [Governance] Feature '{key}' disabled by Flag")
            return False

        # 2. Dry Run Check (Eternity/Safety)
        if self.DRY_RUN_DEFAULT and "write" in key.lower():
            logger.info(f"🛡️ [Governance] Feature '{key}' blocked by DRY_RUN_DEFAULT")
            return False

        # 3. Risk Score (Goodness)
        risk_score = self._calculate_risk_score(key, context)
        if risk_score > 10.0:
            logger.warning(
                f"🛡️ [Governance] Feature '{key}' blocked by Risk Score ({risk_score} > 10.0)"
            )
            # TODO: Notify User / Ask Permission logic here
            return False

        return True

    def get_feature_flag(
        self, key: str, user_id: str | None = None, default: bool = False
    ) -> bool:
        """
        [Advanced Governance] Feature Flag Check
        Redis 기반의 실시간 기능 플래그 확인 (Hot Reloading 없이 즉시 반영)

        Args:
            key: 기능 플래그 키 (예: "new_ui", "beta_feature")
            user_id: 사용자 ID (대상 지정 롤아웃용)
            default: Redis 연결 실패 또는 키 없음 시 기본값

        Returns:
            bool: 기능 활성화 여부
        """
        try:
            # Lazy Import to avoid circular dependencies
            import hashlib

            # 1. Redis Connection
            r = self._get_redis_conn()

            # 2. Fetch Flag Data
            flag_key = f"feature_flags:{key}"
            raw_data = r.hgetall(flag_key)
            # Handle potential awaitable (though unlikely here) or simplify for MyPy
            from typing import cast

            data = cast("dict", raw_data)
            r.close()

            if not data:
                return default

            # 3. Check 'enabled' (Global Switch)
            is_enabled = str(data.get("enabled", "")).lower() == "true"
            if not is_enabled:
                return False  # Globally disabled

            # 4. Check Targeted Users (Allow List)
            if user_id:
                # Assuming comma-separated string for simplicity in Hash
                targets = str(data.get("targeted_users", "")).split(",")
                if user_id in targets:
                    logger.info(
                        f"🎯 [Governance] Targeted User {user_id} allowed for {key}"
                    )
                    return True

            # 5. Check Percentage Rollout (Deterministic)
            rollout_pct = int(data.get("rollout_percentage", 0))
            if rollout_pct >= 100:
                return True
            if rollout_pct <= 0:
                return False

            if user_id:
                # Deterministic hashing: hash(key + user_id) % 100 < percentage
                hash_input = f"{key}:{user_id}".encode()
                hash_val = int(hashlib.sha256(hash_input).hexdigest(), 16)
                user_bucket = hash_val % 100
                return user_bucket < rollout_pct

            return False

        except Exception as e:
            logger.warning(
                f"⚠️ [Governance] Flag check failed for {key}: {e}. Using default."
            )
            return default

    def check_auto_run_eligibility(
        self, trinity_score: float, risk_score: float
    ) -> tuple[bool, str]:
        """
        [AGENTS.md Rule #1] AUTO_RUN 조건 검증

        조건: Trinity Score >= 90 AND Risk Score <= 10

        Args:
            trinity_score: Trinity Score (0-100)
            risk_score: Risk Score (0-100)

        Returns:
            (is_eligible, reason): 자격 여부와 이유
        """
        if trinity_score >= self.auto_run_trinity_threshold:
            if risk_score <= self.auto_run_risk_threshold:
                return (
                    True,
                    f"AUTO_RUN: Trinity Score ({trinity_score}) >= {self.auto_run_trinity_threshold} AND Risk Score ({risk_score}) <= {self.auto_run_risk_threshold}",
                )
            else:
                return (
                    False,
                    f"ASK_COMMANDER: Risk Score ({risk_score}) > {self.auto_run_risk_threshold}",
                )
        else:
            return (
                False,
                f"ASK_COMMANDER: Trinity Score ({trinity_score}) < {self.auto_run_trinity_threshold}",
            )


# 싱글톤 인스턴스 - 전체 앱에서 공유
antigravity = AntiGravitySettings()

# Startup 시 AGENTS.md 통합 확인
if antigravity.agents_md_exists:
    logger.info(f"✅ [AGENTS.md] 파일 확인: {antigravity.agents_md_path}")
    logger.info(f"✅ [AGENTS.md] Trinity 가중치: {antigravity.trinity_weights}")
    logger.info(
        f"✅ [AGENTS.md] AUTO_RUN 조건: Trinity >= {antigravity.auto_run_trinity_threshold}, Risk <= {antigravity.auto_run_risk_threshold}"
    )
else:
    logger.warning(f"⚠️ [AGENTS.md] 파일 없음: {antigravity.agents_md_path}")

# Startup 시 자동 동기화 실행
antigravity.auto_sync()


class ConfigWatcher:
    """
    Antigravity 설정을 감시하고 변경 시 자동 리로드합니다.
    (永: Eternity - Self-Healing & Reactive)
    """

    def __init__(self) -> None:
        try:
            from watchdog.observers import Observer

            self.observer: Any = Observer()
            self.handler: Any = self._create_handler()
            self.running: bool = False
            logger.info("🔭 ConfigWatcher initialized")
        except ImportError:
            logger.warning("⚠️ watchdog not installed. Config monitoring disabled.")
            # [장자] 무용지용 - 없음도 쓰임이 있음, 옵저버 없이도 작동함
            self.observer = None

    def _create_handler(self) -> "FileSystemEventHandler":
        from watchdog.events import FileSystemEventHandler

        class Handler(FileSystemEventHandler):
            def on_modified(self, event: Any) -> None:
                if event.src_path.endswith(".env.antigravity"):
                    logger.info(f"🔄 Config changed: {event.src_path}. Reloading...")
                    # Reload logic here (mocked for now)
                    antigravity.auto_sync()

        return Handler()

    def start(self) -> None:
        if self.observer and not self.running:
            try:
                self.observer.schedule(self.handler, path=".", recursive=False)
                self.observer.start()
                self.running = True
                logger.info("🔭 ConfigWatcher started monitoring .env.antigravity")
            except RuntimeError as e:
                if "already scheduled" in str(e).lower():
                    logger.debug(
                        "🔭 ConfigWatcher already running, skipping duplicate start"
                    )
                    self.running = True
                else:
                    raise


# Initialize and start watcher (with error handling)
watcher = ConfigWatcher()
try:
    watcher.start()
except Exception as e:
    logger.warning(f"⚠️ ConfigWatcher start failed (non-critical): {e}")
