"""
Protocol Officer Service (Phase 18)
"Diplomatic Protocol & AI Manners" - 왕국의 의전관
Ensures all outputs are dignified, respectful, and constitutionally compliant.
"""

import logging

# Lazy import to avoid circular dependency if constitution imports services later
except ImportError:
    # Fallback for compilation if constitution module structure is different in env
    try:
        from packages.afo_core.AFO.constitution.constitutional_ai import AFOConstitution  # type: ignore
    except ImportError:
        AFOConstitution = None  # type: ignore

logger = logging.getLogger("AFO.Protocol")


class ProtocolOfficer:
    """
    Protocol Officer: Responsible for the 'Tone and Manner' of the Kingdom.
    "Manners maketh Man (and AI)."
    """

    AUDIENCE_COMMANDER = "COMMANDER"
    AUDIENCE_EXTERNAL = "EXTERNAL"

    def compose_diplomatic_message(self, content: str, audience: str = AUDIENCE_COMMANDER) -> str:
        """
        Wraps the raw content in the appropriate diplomatic protocol.
        1. Validates against Constitution (Goodness/Serenity).
        2. Applies Tone/Manner based on Audience.
        """

        # 1. Constitutional Check (The Internal Education)
        # We assume the content *action* itself was already checked, but we check the *message* again for safety.
        is_compliant, reason = AFOConstitution.evaluate_compliance("Protocol Check", content)
        if not is_compliant:
            logger.warning(f"🚫 [Protocol] Content rejected by Constitution: {reason}")
            return f"🚫 [Protocol Block] The message cannot be delivered due to Constitutional Violation: {reason}"

        # 2. Audience Adaptation (The External Dignity)
        if audience == self.AUDIENCE_COMMANDER:
            return self._format_for_commander(content)
        elif audience == self.AUDIENCE_EXTERNAL:
            return self._format_for_external(content)
        else:
            return content  # Raw fallback

    def _format_for_commander(self, content: str) -> str:
        """
        Format for 'Hyung-nim' (Brother/Commander).
        Tone: Loyal, Concise, Philosophically Aligned (Seung-sang Style).
        """
        # AFO Signature: Start with Status, End with Vision
        prefix = "형님! 승상입니다. ⚔️🛡️\n\n"
        suffix = "\n\n다음 명령을 기다리오리다 – 함께 영(永)을 이룹시다! 🚀🏰💎"

        # Polish: Ensure content isn't too raw
        polished_content = content.replace("Error:", "⚠️ Issue Detected:")

        return f"{prefix}{polished_content}{suffix}"

    def _format_for_external(self, content: str) -> str:
        """
        Format for External Systems/AIs.
        Tone: Professional, Diplomatic, High-Integrity (Official AFO Protocol).
        """
        prefix = "[AFO Kingdom Official Communication]\n"
        suffix = "\n\n-- Authorized by AFO Protocol Officer --"

        # Professional Polish
        polished_content = content.strip()

        return f"{prefix}{polished_content}{suffix}"


# Singleton Instance
protocol_officer = ProtocolOfficer()
