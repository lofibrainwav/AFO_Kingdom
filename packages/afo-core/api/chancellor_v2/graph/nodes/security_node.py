"""Security Node - AFO Kingdom Chancellor Graph.
Enforces real-time threat detection and anomaly monitoring (TICKET-085).
"""

import logging
from typing import Any

from AFO.agents.security_agent import (
    SecurityEventType,
    ThreatLevel,
    record_security_event,
    security_agent,
)
from api.chancellor_v2.graph.state import GraphState

logger = logging.getLogger(__name__)


def security_node(state: GraphState) -> GraphState:
    """Security node: Scan input for threats and monitor for anomalies.

    Philosophical Alignment:
    - 眞 (Truth): Detect real injection attempts and anomalies
    - 善 (Goodness): Protect the kingdom from malicious input
    - 孝 (Serenity): Automatic blocking of high-threat sources
    """
    command = state.input.get("command", "")
    source = state.input.get("source", "user")

    # 1. Check if source is blocked
    if security_agent.is_blocked(source):
        logger.warning(f"🚨 SECURITY BLOCKED: Source {source} is in the blocklist")
        state.errors.append(f"Security Blocked: {source} is currently restricted")
        state.outputs["SECURITY"] = {
            "status": "blocked",
            "reason": "Entity is on the security blocklist",
        }
        return state

    # 2. Scan for Injection Attempts
    injection_event = security_agent.scan_for_injection(command, source)
    if injection_event:
        logger.critical(f"🚨 SECURITY ALERT: Injection attempt detected from {source}")
        state.errors.append("Security Violation: Malicious input pattern detected")

        # Automatically block if critical
        if injection_event.threat_level == ThreatLevel.CRITICAL:
            security_agent.block_entity(source, "Multiple critical injection attempts")

        state.outputs["SECURITY"] = {
            "status": "threat_detected",
            "threat_type": SecurityEventType.INJECTION_ATTEMPT.value,
            "threat_level": injection_event.threat_level.value,
            "description": injection_event.description,
        }
        return state

    # 3. Anomaly Detection (Simple rate check for current command)
    metrics = {
        "command_length": float(len(command)),
        "complexity_hint": float(command.count(" ") + 1),
    }
    anomaly_event = security_agent.detect_anomaly(source, "submit_command", metrics)

    if anomaly_event and anomaly_event.threat_level.value >= ThreatLevel.HIGH.value:
        logger.warning(f"⚠️ SECURITY WARNING: Anomalous behavior detected from {source}")
        state.outputs["SECURITY"] = {
            "status": "anomaly_detected",
            "threat_level": anomaly_event.threat_level.value,
            "description": anomaly_event.description,
        }
        # We don't necessarily block here but we log and report in state

    else:
        state.outputs["SECURITY"] = {"status": "clear", "threat_level": ThreatLevel.NONE.value}

    return state
