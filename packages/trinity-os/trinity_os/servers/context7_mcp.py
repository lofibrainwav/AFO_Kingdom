import json
from datetime import datetime

class Context7MCP:
    """
    Context7 Tool (Knowledge Injector)
    Provides pinned context and documentation retrieval for the AFO Kingdom.
    """

    # Mock Knowledge Base (In production, this would be a Vector DB or Doc Store)
    KNOWLEDGE_BASE = {
        "AFO_ARCHITECTURE": """
        AFO Kingdom Architecture:
        - Brain: Chancellor (LangGraph)
        - Soul: Trinity (5 Pillars: Truth, Goodness, Beauty, Serenity, Eternity)
        - Heart: Auth (Security)
        - Liver: Users (Management)
        - Stomach: Intake (Data Parsing)
        - Mask: Personas (Interface)
        - Spleen: Family Hub (Happiness Tracking)
        """,
        "TRINITY_PHILOSOPHY": """
        Trinity 5 Pillars:
        1. Truth (眞): 35% - Technical Certainty
        2. Goodness (善): 35% - Ethics & Safety
        3. Beauty (美): 20% - UX & Aesthetics
        4. Serenity (孝): 8% - Peace of Mind (Chancellor's Duty)
        5. Eternity (永): 2% - Sustainability (Legacy)
        """,
        "MCP_PROTOCOL": """
        MCP (Master Control Program) utilizes JSON-RPC 2.0 over stdio.
        Unified Server: afo_ultimate_mcp_server.py
        Tools: shell_execute, read_file, write_file, kingdom_health, calculate_trinity_score, verify_fact, cupy_weighted_sum, sequential_thinking, retrieve_context
        """
    }

    @staticmethod
    def retrieve_context(query: str, domain: str = "general") -> dict:
        """
        Retrieve context based on query keywords.
        """
        results = []
        query_upper = query.upper()

        if "ARCH" in query_upper or "STRUCT" in query_upper:
            results.append(Context7MCP.KNOWLEDGE_BASE["AFO_ARCHITECTURE"])
        if "TRINITY" in query_upper or "PHILOSOPHY" in query_upper or "SCORE" in query_upper:
            results.append(Context7MCP.KNOWLEDGE_BASE["TRINITY_PHILOSOPHY"])
        if "MCP" in query_upper or "TOOL" in query_upper:
            results.append(Context7MCP.KNOWLEDGE_BASE["MCP_PROTOCOL"])

        if not results:
             return {
                 "found": False,
                 "message": f"No specific context found for '{query}'.",
                 "timestamp": datetime.now().isoformat()
             }

        combined_context = "\n---\n".join(results)
        
        # Calculate Trinity Metadata (Truth Impact)
        truth_score = 10 if results else 0

        return {
            "found": True,
            "context": combined_context.strip(),
            "domain": domain,
            "metadata": {
                "truth_impact": truth_score,
                "source": "Context7 Internal DB"
            }
        }
