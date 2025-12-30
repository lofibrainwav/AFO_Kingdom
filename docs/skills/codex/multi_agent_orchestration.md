# AFO Agent Skills for Codex CLI
# 2026-ready agent skills based on research

## multi_agent_orchestration
Invoke this skill when orchestrating multiple agents (Claude, Codex, Ollama) for parallel collaboration.

### Overview
Use MCP servers for shared context:
- `context7` for library documentation
- `sequential-thinking` for step-by-step planning
- `memory` for knowledge sharing across sessions
- `filesystem` for shared code access

### Protocol Stack (2026 Best Practice)
1. **MCP** - Tool access and context provision
2. **A2A** - Agent-to-agent communication (Google protocol)
3. **ACP** - Agent Communication Protocol for intent/planning

### Agent Card Pattern
Each agent exposes capabilities via JSON Agent Card:
- Claude (자룡): Logic verification, refactoring
- Codex (방통): Implementation, execution, prototyping
- Ollama (영덕): Local security, archiving

### Invocation
When starting multi-agent work:
1. Verify all MCP servers are running
2. Check Soul Engine health
3. Confirm Context7 + Sequential Thinking ready
4. Begin parallel reasoning with 3책사 pattern
