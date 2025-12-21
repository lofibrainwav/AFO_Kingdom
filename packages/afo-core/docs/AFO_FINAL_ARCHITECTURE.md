
# 🏰 AFO Kingdom Final Architecture Report
## The LangGraph Chancellor System (승상 체제)

### 1. 👑 The Brain: LangGraph (Chancellor)
**Role**: State Management, Routing, Serenity (孝)
- **State**: Maintains the `Trinity Score` and Conversation History.
- **Routing**: Dynamically delegates to Strategists based on context.
- **Persistence**: Checkpointing for fault tolerance (永).
- **Auto-Run**: Enforces autonomous execution when alignment is high.

### 2. ⚔️ The Hands: Strategists (Nodes)
**Implementation**: CrewAI / AutoGen / LangChain
- **Zhuge Liang (Truth/Spear)**: Architecture & Strategy.
- **Sima Yi (Goodness/Shield)**: Risk & Ethics.
- **Zhou Yu (Beauty/Bridge)**: Narrative & UX.

### 3. 🛠️ The Tools: LangChain & MCP
**Role**: The Glue & The Toolkit
- **LangChain**: Connects LLMs to data/tools.
- **MCP Servers**: Standardized access to:
    - `afo-ultimate-mcp` (Filesystem, Docker, Process)
    - `afo-skills-mcp` (RAG, Search, Knowledge)
    - `playwright` (UI Automation)

---
*"The brain and memory are fully synchronized."*
