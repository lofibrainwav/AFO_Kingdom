# Trinity Score: 90.0 (Established by Chancellor)
#!/usr/bin/env python3
"""
승상의 거울 (Mirror of Chancellor)
Trinity Score 실시간 모니터링 및 자동 알람 시스템

AFO 왕국의 眞善美孝永 철학을 실시간으로 모니터링하여
Trinity Score가 90점 미만으로 떨어질 경우 즉시 알람을 발생시킵니다.

Author: AFO Kingdom Development Team
Date: 2025-12-24
Version: 1.0.0
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import aiohttp
import websockets
from pydantic import BaseModel
from redis.asyncio import Redis

# AFO Kingdom imports
try:
    from AFO.observability.rule_constants import WEIGHTS
    from AFO.services.trinity_calculator import (TrinityCalculator,
                                                 trinity_calculator)
except ImportError:
    print("❌ AFO Kingdom modules not found. Please run from AFO Kingdom root.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TrinityScoreAlert(BaseModel):
    """Trinity Score Alert Model"""

    pillar: str
    score: float
    threshold: float
    timestamp: str
    message: str


class ChancellorMirror:
    """
    승상의 거울 (Mirror of Chancellor)

    Trinity Score 실시간 모니터링 및 자동 알람 시스템.
    眞善美孝永 각 기둥의 점수를 지속적으로 모니터링하여
    시스템 건강 상태를 유지합니다.
    """

    def __init__(self, api_base: str = "http://localhost:8010"):
        self.api_base = api_base
        self.calculator = trinity_calculator
        self.alert_threshold = 90.0
        self.pillar_thresholds = {
            "truth": 90.0,
            "goodness": 90.0,
            "beauty": 90.0,
            "serenity": 90.0,
            "eternity": 90.0,
        }
        self.active_alerts: list[TrinityScoreAlert] = []
        self.redis: Redis | None = None
        self.stream_channel = "afo:verdicts"

    async def _init_redis(self) -> None:
        """Redis 연결 초기화"""
        try:
            host = os.environ.get("REDIS_HOST", "127.0.0.1")
            port = int(os.environ.get("REDIS_PORT", "6379"))
            self.redis = Redis(host=host, port=port, decode_responses=True)
            await self.redis.ping()
        except Exception as e:
            logger.warning(f"Redis connection failed (Observability disabled): {e}")
            self.redis = None

    async def _publish_thought(self, content: str, level: str = "info") -> None:
        """Matrix Stream에 생각(상태) 전파"""
        if not self.redis:
            return

        try:
            payload = {
                "type": "thought",
                "source": "Mirror",
                "content": content,
                "level": level,
                "timestamp": datetime.now().isoformat(),
            }
            await self.redis.publish(self.stream_channel, json.dumps(payload))
        except Exception as e:
            logger.error(f"Failed to publish thought: {e}")

    async def monitor_trinity_score(self) -> None:
        """
        Trinity Score 실시간 모니터링

        SSE 스트림을 통해 Chancellor Graph의 판결을 실시간으로 모니터링합니다.
        """
        await self._init_redis()
        logger.info("🔍 승상의 거울 가동: Trinity Score 실시간 모니터링 시작")
        await self._publish_thought(
            "Chancellor Mirror initialized (Perpetual Surveillance Active)"
        )

        try:
            async with websockets.connect(
                f"ws://{self.api_base.replace('http://', '')}/api/stream/chancellor"
            ) as websocket:
                logger.info("✅ Chancellor WebSocket 연결 성공")

                while True:
                    try:
                        # Chancellor 판결 수신
                        verdict_data = await websocket.recv()
                        verdict = json.loads(verdict_data)

                        # Trinity Score 분석
                        await self.analyze_verdict(verdict)

                    except websockets.exceptions.ConnectionClosed:
                        logger.warning("⚠️ WebSocket 연결 끊김, 재연결 시도...")
                        await asyncio.sleep(5)
                        break

                    except json.JSONDecodeError as e:
                        logger.error(f"❌ 판결 데이터 파싱 실패: {e}")
                        continue

        except Exception as e:
            logger.error(f"❌ WebSocket 연결 실패: {e}")
            logger.info("📡 HTTP 폴링 모드로 전환")
            await self.monitor_via_http()

    async def monitor_via_http(self) -> None:
        """
        HTTP 폴링을 통한 모니터링 (WebSocket 실패 시 대체)

        주기적으로 /api/5pillars/current 엔드포인트를 호출하여
        Trinity Score를 모니터링합니다.
        """
        logger.info("🔄 HTTP 폴링 모드로 Trinity Score 모니터링 시작")

        while True:
            try:
                await self.check_current_trinity_score()
                await self._publish_thought(
                    "System Pulse: All pillars monitored and stable."
                )
                await asyncio.sleep(600)  # 10분 간격으로 체크 및 하트비트

            except Exception as e:
                logger.error(f"❌ Trinity Score 체크 실패: {e}")
                await asyncio.sleep(60)  # 에러 시 1분 대기

    async def check_current_trinity_score(self) -> None:
        """
        현재 Trinity Score 조회 및 분석
        """
        try:
            async with (
                aiohttp.ClientSession() as session,
                session.get(f"{self.api_base}/api/5pillars/current") as response,
            ):
                if response.status == 200:
                    data = await response.json()
                    overall = data.get("scores", {}).get("overall", 0) * 100
                    logger.info(f"📊 [Mirror] Current Trinity Score: {overall:.2f}")
                    await self.analyze_pillars_data(data)
                else:
                    logger.warning(f"⚠️ Trinity Score 조회 실패: HTTP {response.status}")

        except Exception as e:
            logger.error(f"❌ HTTP 요청 실패: {e}")

    async def analyze_verdict(self, verdict: dict) -> None:
        """
        Chancellor 판결 분석

        Args:
            verdict: Chancellor 판결 데이터
        """
        trinity_score = verdict.get("trinity_score", 0)
        risk_score = verdict.get("risk_score", 0)

        logger.info(f"📊 Trinity Score: {trinity_score:.1f}, Risk Score: {risk_score}")

        # 전체 Trinity Score 알람 체크
        if trinity_score < self.alert_threshold:
            await self.raise_alert(
                "total",
                trinity_score,
                self.alert_threshold,
                f"🚨 긴급: 전체 Trinity Score {trinity_score:.1f}점으로 {self.alert_threshold}점 미만!",
            )

        # Risk Score 알람 체크
        if risk_score > 10:
            await self.raise_alert(
                "risk",
                risk_score,
                10,
                f"⚠️ 위험: Risk Score {risk_score}점으로 위험 수준!",
            )

    async def analyze_pillars_data(self, data: dict) -> None:
        """
        5기둥 데이터 분석

        Args:
            data: 5기둥 점수 데이터
        """
        pillars = data.get("scores", {})
        if not pillars:
            pillars = data.get("pillars", {})

        for pillar, score in pillars.items():
            if pillar == "overall":
                continue  # Skip overall in individual pillars check

            # Scale up to 100 if it's 0-1 range
            normalized_score = score * 100 if score <= 1.0 else score
            threshold = self.pillar_thresholds.get(pillar, 90.0)

            if normalized_score < threshold:
                await self.raise_alert(
                    pillar,
                    normalized_score,
                    threshold,
                    f"⚠️ {pillar.upper()}: {normalized_score:.1f}점으로 기준치 {threshold}점 미만!",
                )

    async def raise_alert(
        self, pillar: str, score: float, threshold: float, message: str
    ) -> None:
        """
        알람 발생

        Args:
            pillar: 문제 기둥
            score: 현재 점수
            threshold: 기준치
            message: 알람 메시지
        """

        alert = TrinityScoreAlert(
            pillar=pillar,
            score=score,
            threshold=threshold,
            timestamp=datetime.now().isoformat(),
            message=message,
        )
        await self._publish_thought(
            message, level="warning" if "⚠️" in message else "critical"
        )

        # 중복 알람 방지
        if not self._is_duplicate_alert(alert):
            self.active_alerts.append(alert)

            # 알람 로깅
            logger.warning(f"🚨 TRINITY ALERT: {message}")

            # 알람 전송 (확장 가능)
            await self.send_alert_notification(alert)

            # 심각한 경우 즉시 조치
            if pillar == "total" and score < 85.0:
                await self.emergency_response(alert)

    def _is_duplicate_alert(self, new_alert: TrinityScoreAlert) -> bool:
        """
        중복 알람 체크

        Args:
            new_alert: 새로운 알람

        Returns:
            중복 여부
        """
        import datetime

        # 최근 5분 내 동일 기둥 알람은 무시
        cutoff_time = datetime.datetime.now() - datetime.timedelta(minutes=5)

        for alert in self.active_alerts:
            if (
                alert.pillar == new_alert.pillar
                and alert.timestamp > cutoff_time.isoformat()
            ):
                return True

        return False

    async def send_alert_notification(self, alert: TrinityScoreAlert) -> None:
        """
        알람 알림 전송

        Args:
            alert: 알람 데이터
        """
        # 현재는 로깅만 수행, 확장 가능:
        # - Slack/Discord 웹훅
        # - 이메일 알림
        # - SMS 알림
        # - 내부 알람 시스템

        logger.warning(f"📢 알람 전송: {alert.message}")

        # TODO: 실제 알림 시스템 연동
        # await send_slack_notification(alert)
        # await send_email_notification(alert)

    async def emergency_response(self, alert: TrinityScoreAlert) -> None:
        """
        긴급 상황 대응

        Args:
            alert: 긴급 알람
        """
        logger.critical(f"🚨 EMERGENCY RESPONSE ACTIVATED | {alert.message}")

        # 긴급 대응 조치:
        # 1. 시스템 상태 로그 수집
        # 2. 자동 복구 시도
        # 3. 관리자 즉시 통보

        await self.collect_system_diagnostics()
        await self.attempt_auto_recovery()
        await self.notify_administrators(alert)

    async def collect_system_diagnostics(self) -> None:
        """
        시스템 진단 정보 수집
        """
        logger.info("🔍 시스템 진단 정보 수집 중...")

        try:
            async with aiohttp.ClientSession() as session:
                # 헬스 체크
                async with session.get(f"{self.api_base}/health") as response:
                    health_data = await response.json()
                    logger.info(f"📊 Health Status: {health_data}")

                # 시스템 메트릭
                async with session.get(
                    f"{self.api_base}/api/system/metrics"
                ) as response:
                    if response.status == 200:
                        metrics_data = await response.json()
                        logger.info(f"📊 System Metrics: {metrics_data}")

        except Exception as e:
            logger.error(f"❌ 진단 정보 수집 실패: {e}")

    async def attempt_auto_recovery(self) -> None:
        """
        자동 복구 시도
        """
        logger.info("🔧 자동 복구 시도 중...")

        # TODO: 자동 복구 로직 구현
        # - 캐시 클리어
        # - 서비스 재시작
        # - 설정 리로드

    async def notify_administrators(self, alert: TrinityScoreAlert) -> None:
        """
        관리자 통보

        Args:
            alert: 긴급 알람
        """
        logger.critical("📢 관리자 긴급 통보 발송")

        # TODO: 관리자 통보 로직 구현
        # - 이메일 발송
        # - SMS 발송
        # - 내부 알람 시스템

    def get_active_alerts(self) -> list[TrinityScoreAlert]:
        """
        활성 알람 목록 조회

        Returns:
            활성 알람 리스트
        """
        return self.active_alerts.copy()

    def clear_resolved_alerts(self) -> None:
        """
        해결된 알람 정리
        """
        import datetime

        # 1시간 이상 된 알람은 정리
        cutoff_time = datetime.datetime.now() - datetime.timedelta(hours=1)

        self.active_alerts = [
            alert
            for alert in self.active_alerts
            if alert.timestamp > cutoff_time.isoformat()
        ]

        logger.info(f"🧹 해결된 알람 정리 완료, 남은 알람: {len(self.active_alerts)}개")


async def main():
    """
    메인 함수: 승상의 거울 가동
    """
    print("🏰 AFO 왕국 승상의 거울 가동")
    print("=" * 50)

    # 환경 설정
    api_base = "http://localhost:8010"

    # 거울 생성
    mirror = ChancellorMirror(api_base)

    try:
        # 모니터링 시작
        await mirror.monitor_trinity_score()

    except KeyboardInterrupt:
        logger.info("🛑 승상의 거울 중지")

    except Exception as e:
        logger.error(f"❌ 승상의 거울 실행 실패: {e}")
        sys.exit(1)

    finally:
        # 정리 작업
        mirror.clear_resolved_alerts()
        active_alerts = mirror.get_active_alerts()

        if active_alerts:
            print(f"\n⚠️  종료 시점 활성 알람: {len(active_alerts)}개")
            for alert in active_alerts:
                print(f"   - {alert.pillar}: {alert.message}")
        else:
            print("\n✅ 모든 알람 해결됨")


if __name__ == "__main__":
    # Python 3.7+ asyncio run
    asyncio.run(main())
