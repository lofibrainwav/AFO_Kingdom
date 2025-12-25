---
name: mcp-tool-bridge
description: Universal bridge to connect and utilize any external MCP (Model Context Protocol) server tools. The gateway to infinite extensibility.
license: MIT
compatibility:
  - claude-code
  - codex
  - cursor
metadata:
  version: "1.0.0"
  category: integration
  author: AFO Kingdom
  mcp_version: "2024-11-05"
  philosophy_scores:
    truth: 95
    goodness: 99
    beauty: 96
    serenity: 94
---

# MCP Tool Bridge

The universal connector for the AFO Kingdom, enabling integration with any MCP-compatible server.

## What is MCP?

Model Context Protocol (MCP) is an open standard for AI model communication with external tools, resources, and services.

## Supported Operations

| Operation | Description |
|-----------|-------------|
| `list_mcp_resources` | List all available resources from MCP servers |
| `list_mcp_tools` | List all available tools from MCP servers |
| `call_mcp_tool` | Execute a specific tool with parameters |
| `read_mcp_resource` | Read content from an MCP resource |

## Registered MCP Servers

The AFO Kingdom includes these MCP servers:

| Server | Description | Tools |
|--------|-------------|-------|
| afo-ultimate-mcp | Universal connector | 12 tools |
| afo-skills-registry-mcp | Skills as MCP tools | 20 skills |
| trinity-score-mcp | Trinity Score calculator | 1 tool |
| afo-obsidian-mcp | Obsidian integration | 6 tools |
| context7 | Library documentation | 2 tools |
| sequential-thinking | Step-by-step reasoning | 1 tool |
| memory | Knowledge graph | 3 tools |
| filesystem | File operations | 10 tools |

## Usage

```python
# List available tools from a specific server
tools = await mcp_bridge.list_tools("afo-ultimate-mcp")

# Call a tool
result = await mcp_bridge.call_tool(
    server="trinity-score-mcp",
    tool="calculate",
    args={"truth_base": 95, "goodness_base": 90}
)
```

## Configuration

MCP servers are configured in:
- `~/.claude/mcp.json` - Claude Code CLI
- `~/.codex/config.toml` - Codex CLI
- `.mcp.json` - Project-level
- `.cursor/mcp.json` - Cursor IDE

## Philosophy Alignment

- **眞 (Truth)**: Standardized protocol ensures accurate communication
- **善 (Goodness)**: Infinite extensibility for any use case
- **美 (Beauty)**: Universal interface, clean abstractions
- **孝 (Serenity)**: Seamless integration, minimal friction
