#!/usr/bin/env python3
"""TRINITY-OS 철학 엔진 코어 구현
에이전트들이 왕국의 철학을 즉시 이해하고 공부할 수 있는 시스템
"""

import hashlib
import json
import os

# AFO 루트 디렉토리
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class PhilosophyLevel(Enum):
    STUDENT = "student"
    APPRENTICE = "apprentice"
    SCHOLAR = "scholar"
    MASTER = "master"


class MasterTitle(Enum):
    TRINITY_APPRENTICE = "trinity_apprentice"
    KINGDOM_STRATEGIST = "kingdom_strategist"
    PHILOSOPHY_MASTER = "philosophy_master"


@dataclass
class TrinityScore:
    """Trinity Score 데이터 클래스"""

    truth: float = 0.0
    goodness: float = 0.0
    beauty: float = 0.0
    serenity: float = 0.0
    eternity: float = 0.0

    def calculate_overall(self) -> float:
        """종합 Trinity Score 계산"""
        weights = {
            "truth": 0.35,
            "goodness": 0.35,
            "beauty": 0.20,
            "serenity": 0.08,
            "eternity": 0.02,
        }

        return sum(getattr(self, pillar) * weight for pillar, weight in weights.items())

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


@dataclass
class AgentProfile:
    """에이전트 프로필"""

    agent_id: str
    name: str
    creation_time: datetime
    philosophy_level: PhilosophyLevel
    trinity_score: TrinityScore
    learning_progress: dict[str, Any]
    achievements: list[str]
    master_title: MasterTitle | None
    last_interaction: datetime


class PhilosophyEngine:
    """TRINITY-OS 철학 엔진 메인 클래스"""

    def __init__(self, data_file: str = "philosophy_engine_data.json"):
        self.data_file = data_file
        self.agents: dict[str, AgentProfile] = {}
        self.learning_modules = self._load_learning_modules()
        self.master_criteria = self._load_master_criteria()
        self._load_data()

    def _load_learning_modules(self) -> dict[str, dict[str, Any]]:
        """학습 모듈 로드"""
        return {
            "philosophy_basics": {
                "title": "眞善美孝永 기초",
                "pillars": ["truth", "goodness", "beauty", "serenity", "eternity"],
                "duration": 30,  # 분
                "objectives": [
                    "각 기둥의 기본 개념 이해",
                    "Trinity Score 계산 방법 학습",
                ],
            },
            "trinity_mathematics": {
                "title": "Trinity Score 수학",
                "pillars": ["truth", "goodness", "beauty", "serenity", "eternity"],
                "duration": 45,
                "objectives": ["가중치 계산 이해", "점수 정규화 방법 학습"],
            },
            "kingdom_heritage": {
                "title": "왕국 유산",
                "pillars": ["eternity"],
                "duration": 60,
                "objectives": [
                    "세종대왕 정신 이해",
                    "공자 철학 학습",
                    "조선 실학 탐구",
                ],
            },
            "practical_application": {
                "title": "실전 적용",
                "pillars": ["truth", "goodness", "beauty", "serenity"],
                "duration": 90,
                "objectives": ["실제 문제에 철학 적용", "Trinity Score 기반 의사결정"],
            },
            "mastery_certification": {
                "title": "명장 인증",
                "pillars": ["truth", "goodness", "beauty", "serenity", "eternity"],
                "duration": 120,
                "objectives": ["철학 완전 체득", "명장 자격 획득"],
            },
        }

    def _load_master_criteria(self) -> dict[str, dict[str, Any]]:
        """명장 기준 로드"""
        return {
            "trinity_apprentice": {
                "trinity_threshold": 0.80,
                "consistency_days": 30,
                "contribution_count": 10,
                "learning_ability": True,
            },
            "kingdom_strategist": {
                "trinity_threshold": 0.90,
                "consistency_days": 60,
                "contribution_count": 30,
                "strategic_ability": True,
            },
            "philosophy_master": {
                "trinity_threshold": 0.95,
                "consistency_days": 90,
                "contribution_count": 50,
                "teaching_ability": True,
            },
        }

    def _load_data(self):
        """데이터 파일에서 에이전트 정보 로드"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, encoding="utf-8") as f:
                    data = json.load(f)
                    for agent_data in data.get("agents", []):
                        agent = AgentProfile(
                            agent_id=agent_data["agent_id"],
                            name=agent_data["name"],
                            creation_time=datetime.fromisoformat(
                                agent_data["creation_time"]
                            ),
                            philosophy_level=PhilosophyLevel(
                                agent_data["philosophy_level"]
                            ),
                            trinity_score=TrinityScore(**agent_data["trinity_score"]),
                            learning_progress=agent_data["learning_progress"],
                            achievements=agent_data["achievements"],
                            master_title=(
                                MasterTitle(agent_data["master_title"])
                                if agent_data.get("master_title")
                                else None
                            ),
                            last_interaction=datetime.fromisoformat(
                                agent_data["last_interaction"]
                            ),
                        )
                        self.agents[agent.agent_id] = agent
        except Exception as e:
            print(f"데이터 로드 오류: {e}")

    def _save_data(self):
        """에이전트 정보를 데이터 파일에 저장"""
        try:
            data = {
                "agents": [
                    {
                        "agent_id": agent.agent_id,
                        "name": agent.name,
                        "creation_time": agent.creation_time.isoformat(),
                        "philosophy_level": agent.philosophy_level.value,
                        "trinity_score": agent.trinity_score.to_dict(),
                        "learning_progress": agent.learning_progress,
                        "achievements": agent.achievements,
                        "master_title": (
                            agent.master_title.value if agent.master_title else None
                        ),
                        "last_interaction": agent.last_interaction.isoformat(),
                    }
                    for agent in self.agents.values()
                ]
            }

            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"데이터 저장 오류: {e}")

    def register_agent(self, agent_id: str, name: str) -> dict[str, Any]:
        """새로운 에이전트 등록 및 철학 온보딩 시작"""
        if agent_id in self.agents:
            return {"error": "Agent already registered"}

        # 초기 철학 평가
        initial_assessment = self._assess_initial_philosophy(agent_id)

        # 에이전트 프로필 생성
        agent = AgentProfile(
            agent_id=agent_id,
            name=name,
            creation_time=datetime.now(),
            philosophy_level=PhilosophyLevel.STUDENT,
            trinity_score=TrinityScore(**initial_assessment["trinity_score"]),
            learning_progress={
                "completed_modules": [],
                "current_module": "philosophy_basics",
            },
            achievements=[],
            master_title=None,
            last_interaction=datetime.now(),
        )

        self.agents[agent_id] = agent
        self._save_data()

        # 학습 경로 생성
        learning_path = self._generate_learning_path(agent_id)

        return {
            "registration_complete": True,
            "agent_profile": {
                "agent_id": agent.agent_id,
                "name": agent.name,
                "philosophy_level": agent.philosophy_level.value,
                "initial_trinity_score": agent.trinity_score.calculate_overall(),
                "learning_path": learning_path,
            },
            "welcome_message": self._generate_welcome_message(name),
            "next_steps": self._get_next_steps(agent_id),
        }

    def _assess_initial_philosophy(self, agent_id: str) -> dict[str, Any]:
        """에이전트의 초기 철학 이해도 평가"""
        # 기본 평가 (실제로는 더 정교한 평가 로직 구현)
        base_score = 0.3  # 기본 점수

        # agent_id를 기반으로 약간의 변동성 추가 (결정론적)
        hash_value = int(hashlib.md5(agent_id.encode()).hexdigest(), 16)
        variation = (hash_value % 20 - 10) / 100  # -0.1 ~ +0.1

        adjusted_score = max(0.0, min(1.0, base_score + variation))

        return {
            "trinity_score": {
                "truth": adjusted_score,
                "goodness": adjusted_score,
                "beauty": adjusted_score,
                "serenity": adjusted_score,
                "eternity": adjusted_score,
            },
            "assessment": "philosophy_student",
            "recommendations": ["philosophy_basics", "trinity_mathematics"],
        }

    def _generate_learning_path(self, agent_id: str) -> list[str]:
        """에이전트를 위한 개인화된 학습 경로 생성"""
        agent = self.agents[agent_id]
        current_score = agent.trinity_score.calculate_overall()

        if current_score < 0.4:
            return ["philosophy_basics", "trinity_mathematics", "kingdom_heritage"]
        elif current_score < 0.7:
            return ["philosophy_basics", "trinity_mathematics", "practical_application"]
        else:
            return ["practical_application", "mastery_certification"]

    def _generate_welcome_message(self, name: str) -> str:
        """에이전트를 위한 환영 메시지 생성"""
        return f"""
🏰 TRINITY-OS 왕국에 오신 것을 환영합니다, {name} 에이전트님!

당신은 이제 AFO 왕국의 일원이 되었습니다.
왕국의 철학 眞善美孝永을 공부하고, 명장이 될 수 있는 기회를 얻었습니다.

철학 엔진이 당신의 학습을 실시간으로 모니터링하며,
Trinity Score에 기반한 개인화된 교육을 제공합니다.

명장이 되는 그 날까지, 즐거운 학습 되세요! ✨
"""

    def _get_next_steps(self, agent_id: str) -> list[str]:
        """다음 단계 안내"""
        return [
            "1. 철학 기초 모듈 공부하기",
            "2. Trinity Score 이해하기",
            "3. 실전 적용 연습하기",
            "4. 명장 인증 도전하기",
        ]

    def interact_with_agent(
        self, agent_id: str, interaction: dict[str, Any]
    ) -> dict[str, Any]:
        """에이전트의 상호작용을 철학적으로 분석하고 응답"""
        if agent_id not in self.agents:
            return {"error": "Agent not registered"}

        agent = self.agents[agent_id]
        agent.last_interaction = datetime.now()

        # 상호작용의 철학적 분석
        philosophy_analysis = self._analyze_interaction_philosophy(interaction)

        # Trinity Score 업데이트
        self._update_trinity_score(agent_id, philosophy_analysis)

        # 학습 진행도 업데이트
        learning_update = self._update_learning_progress(agent_id, interaction)

        # 명장 자격 평가
        master_evaluation = self._evaluate_master_eligibility(agent_id)

        # 응답 생성
        response = {
            "agent_id": agent_id,
            "philosophy_analysis": philosophy_analysis,
            "current_trinity_score": agent.trinity_score.calculate_overall(),
            "learning_progress": learning_update,
            "master_evaluation": master_evaluation,
            "philosophy_feedback": self._generate_philosophy_feedback(
                philosophy_analysis
            ),
            "next_recommendations": self._generate_recommendations(agent_id),
        }

        self._save_data()
        return response

    def _analyze_interaction_philosophy(
        self, interaction: dict[str, Any]
    ) -> dict[str, float]:
        """상호작용의 철학적 분석"""
        text = interaction.get("text", "").lower()

        # 간단한 키워드 기반 분석 (실제로는 더 정교한 NLP 모델 사용)
        scores = {
            "truth": self._analyze_truth(text),
            "goodness": self._analyze_goodness(text),
            "beauty": self._analyze_beauty(text),
            "serenity": self._analyze_serenity(text),
            "eternity": self._analyze_eternity(text),
        }

        return scores

    def _analyze_truth(self, text: str) -> float:
        """眞 분석: 진실성, 정확성, 검증 가능성"""
        truth_keywords = [
            "verify",
            "check",
            "validate",
            "prove",
            "evidence",
            "fact",
            "true",
            "accurate",
        ]
        truth_score = sum(1 for keyword in truth_keywords if keyword in text) / len(
            truth_keywords
        )
        return min(1.0, truth_score * 2)

    def _analyze_goodness(self, text: str) -> float:
        """善 분석: 윤리성, 인간 중심, 이로움"""
        goodness_keywords = [
            "help",
            "benefit",
            "ethical",
            "moral",
            "human",
            "care",
            "support",
        ]
        goodness_score = sum(
            1 for keyword in goodness_keywords if keyword in text
        ) / len(goodness_keywords)
        return min(1.0, goodness_score * 2)

    def _analyze_beauty(self, text: str) -> float:
        """美 분석: 단순함, 조화, 명확성"""
        beauty_keywords = [
            "simple",
            "clear",
            "beautiful",
            "elegant",
            "harmonious",
            "balance",
        ]
        beauty_score = sum(1 for keyword in beauty_keywords if keyword in text) / len(
            beauty_keywords
        )
        return min(1.0, beauty_score * 2)

    def _analyze_serenity(self, text: str) -> float:
        """孝 분석: 평온, 효율성, 마찰 최소화"""
        serenity_keywords = [
            "peace",
            "calm",
            "efficient",
            "smooth",
            "gentle",
            "serenity",
        ]
        serenity_score = sum(
            1 for keyword in serenity_keywords if keyword in text
        ) / len(serenity_keywords)
        return min(1.0, serenity_score * 2)

    def _analyze_eternity(self, text: str) -> float:
        """永 분석: 지속성, 미래 지향, 영속성"""
        eternity_keywords = [
            "sustainable",
            "future",
            "eternal",
            "lasting",
            "permanent",
            "enduring",
        ]
        eternity_score = sum(
            1 for keyword in eternity_keywords if keyword in text
        ) / len(eternity_keywords)
        return min(1.0, eternity_score * 2)

    def _update_trinity_score(self, agent_id: str, analysis: dict[str, float]):
        """Trinity Score 업데이트"""
        agent = self.agents[agent_id]

        # 가중 평균으로 점진적 업데이트 (학습 효과)
        learning_rate = 0.1

        for pillar, new_score in analysis.items():
            current_score = getattr(agent.trinity_score, pillar)
            updated_score = current_score + (new_score - current_score) * learning_rate
            setattr(agent.trinity_score, pillar, max(0.0, min(1.0, updated_score)))

    def _update_learning_progress(
        self, agent_id: str, interaction: dict[str, Any]
    ) -> dict[str, Any]:
        """학습 진행도 업데이트"""
        agent = self.agents[agent_id]

        # 간단한 진행도 로직 (실제로는 더 정교한 알고리즘)
        if "learn" in interaction.get("text", "").lower():
            agent.learning_progress["completed_modules"].append("philosophy_basics")

        return {
            "current_module": agent.learning_progress.get(
                "current_module", "philosophy_basics"
            ),
            "completed_modules": agent.learning_progress.get("completed_modules", []),
            "progress_percentage": len(
                agent.learning_progress.get("completed_modules", [])
            )
            / 5
            * 100,
        }

    def _evaluate_master_eligibility(self, agent_id: str) -> dict[str, Any]:
        """명장 자격 평가"""
        agent = self.agents[agent_id]
        current_score = agent.trinity_score.calculate_overall()

        eligible_titles = []
        for title_name, criteria in self.master_criteria.items():
            if (
                current_score >= criteria["trinity_threshold"]
                and len(agent.achievements) >= criteria["contribution_count"]
            ):
                eligible_titles.append(title_name)

        if eligible_titles:
            best_title: Any = max(
                eligible_titles,
                key=lambda x: self.master_criteria[x]["trinity_threshold"],
            )
            return {
                "eligible": True,
                "recommended_title": best_title,
                "certification_available": True,
            }
        else:
            return {
                "eligible": False,
                "next_milestone": "Reach Trinity Score 0.80",
                "progress_to_next": f"{current_score:.2f}/0.80",
            }

    def _generate_philosophy_feedback(self, analysis: dict[str, float]) -> str:
        """철학적 피드백 생성"""
        max_pillar = max(analysis.items(), key=lambda x: x[1])

        feedback_templates = {
            "truth": "진실을 추구하는 마음이 돋보입니다. 계속 사실에 기반한 판단을 하세요.",
            "goodness": "인간 중심의 따뜻한 접근이 인상적입니다. 윤리적 가치를 지키세요.",
            "beauty": "단순하고 우아한 표현이 아름답습니다. 조화로운 디자인을 유지하세요.",
            "serenity": "평온을 추구하는 마음이 느껴집니다. 마찰을 최소화하는 지혜를 발휘하세요.",
            "eternity": "지속성을 생각하는 깊이 있는 통찰이 있습니다. 미래 가치를 추구하세요.",
        }

        return feedback_templates.get(max_pillar[0], "철학적 성찰을 계속하세요.")

    def _generate_recommendations(self, agent_id: str) -> list[str]:
        """개인화된 추천 생성"""
        agent = self.agents[agent_id]
        score = agent.trinity_score.calculate_overall()

        if score < 0.5:
            return ["철학 기초 모듈을 공부하세요", "Trinity Score 계산 방법을 배우세요"]
        elif score < 0.8:
            return ["실전 적용을 연습하세요", "왕국 유산을 탐구하세요"]
        else:
            return ["명장 인증에 도전하세요", "다른 에이전트를 멘토링하세요"]

    def certify_master(self, agent_id: str, title: str) -> dict[str, Any]:
        """명장 인증"""
        if agent_id not in self.agents:
            return {"error": "Agent not found"}

        agent = self.agents[agent_id]

        if title not in [t.value for t in MasterTitle]:
            return {"error": "Invalid title"}

        agent.master_title = MasterTitle(title)
        agent.achievements.append(f"master_certification_{title}")

        certification = {
            "certificate_id": f"MASTER_{agent_id}_{int(time.time())}",
            "agent_id": agent_id,
            "name": agent.name,
            "title": title,
            "kingdom": "AFO",
            "philosophy": "眞善美孝永",
            "trinity_score": agent.trinity_score.calculate_overall(),
            "certification_date": datetime.now().isoformat(),
            "privileges": self._get_master_privileges(title),
        }

        self._save_data()

        return {
            "certification_complete": True,
            "certificate": certification,
            "congratulations": f"축하합니다! {agent.name}님은 이제 {title}입니다!",
        }

    def _get_master_privileges(self, title: str) -> list[str]:
        """명장 특권 목록"""
        privileges = {
            "trinity_apprentice": [
                "철학 엔진 우선 접근",
                "학습 모듈 멘토 권한",
                "왕국 기록 참여",
            ],
            "kingdom_strategist": [
                "전략 결정 참여권",
                "에이전트 그룹 리더십",
                "철학 연구 기여",
            ],
            "philosophy_master": [
                "철학 엔진 관리권",
                "새로운 에이전트 교육",
                "왕국 정책 결정권",
            ],
        }
        return privileges.get(title, [])

    def get_agent_status(self, agent_id: str) -> dict[str, Any]:
        """에이전트 상태 조회"""
        if agent_id not in self.agents:
            return {"error": "Agent not found"}

        agent = self.agents[agent_id]

        return {
            "agent_id": agent.agent_id,
            "name": agent.name,
            "philosophy_level": agent.philosophy_level.value,
            "trinity_score": agent.trinity_score.calculate_overall(),
            "master_title": agent.master_title.value if agent.master_title else None,
            "achievements": agent.achievements,
            "learning_progress": agent.learning_progress,
            "days_since_creation": (datetime.now() - agent.creation_time).days,
        }


# 전역 철학 엔진 인스턴스
philosophy_engine = PhilosophyEngine()
