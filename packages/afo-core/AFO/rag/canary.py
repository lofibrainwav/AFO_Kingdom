from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Literal


RAGVersion = Literal["v1", "v2"]
RAGMode = Literal["forced_on", "forced_off", "shadow_only", "on", "off"]


@dataclass(frozen=True)
class RagDecision:
    mode: RAGMode
    version: RAGVersion
    reason: str
    bucket: int | None = None


def _bucket_0_99(key: str) -> int:
    h = hashlib.sha256(key.encode("utf-8")).digest()
    return int.from_bytes(h[:4], "big") % 100


def is_canary_user(user_key: str, percent: int, salt: str = "afo") -> tuple[bool, int]:
    if percent <= 0:
        return (False, 0)
    if percent >= 100:
        return (True, 0)
    bucket = _bucket_0_99(f"{salt}:{user_key}")
    return (bucket < percent, bucket)


def decide_rag_version(
    *,
    user_key: str,
    header_mode: str | None,
    config_flag: bool,
    canary_percent: int,
    salt: str = "afo",
) -> RagDecision:
    hm = (header_mode or "").strip().lower()

    # Header 최우선
    if hm == "forced_off":
        return RagDecision(mode="forced_off", version="v1", reason="header_forced_off")
    if hm == "forced_on":
        # forced_on beats everything except kill
        if not config_flag:
            return RagDecision(mode="off", version="v1", reason="kill_switch_beats_forced_on")
        return RagDecision(mode="forced_on", version="v2", reason="header_forced_on")
    if hm == "shadow_only":
        # shadow_only는 "v1 응답 + v2 shadow" 같은 2-path가 필요하니, 지금은 decision만 제공
        return RagDecision(mode="shadow_only", version="v1", reason="header_shadow_only")

    # Kill switch
    if not config_flag:
        return RagDecision(mode="off", version="v1", reason="kill_switch_off")

    # Canary (deterministic)
    ok, bucket = is_canary_user(user_key=user_key, percent=canary_percent, salt=salt)
    if ok:
        return RagDecision(mode="on", version="v2", reason="canary", bucket=bucket)

    return RagDecision(mode="on", version="v1", reason="stable", bucket=bucket)
