# PH-SE-07-01: Juggl & Dataview Integration Strategy

## 🎯 Objective
Transform the static Link Graph into a **Dynamic, High-Density Knowledge Network** using Juggl (Graph) and Dataview (Query).

## 🧩 Component Analysis
- **Juggl**: Adds "Force Layout", "Node Styling", and "Workspace" capabilities to the Graph.
- **Dataview**: Allows SQL-like querying of Markdown files (Metadata).
- **Integration**: Use DataviewJS to dynamically generate Juggl graphs based on current context (e.g., "Show me all nodes related to PH-SE-07").

## 🛠️ Implementation Specs (Kingdom Standard)
### 1. Juggl Settings (`.obsidian/plugins/juggl/data.json`)
- **Node Color**:
  - `#MCP` -> Blue (Truth)
  - `#Skills` -> Green (Growth)
  - `#Context7` -> Gold (Eternity)
- **Layout**: Force-Directed (Gravity: 0.8, Repulsion: 200)
- **Edges**: Show Label on Hover

### 2. Dataview Script (`scripts/dv_graph.js`)
- A modular script to be embedded in MOCs.
- `dv.view("scripts/dv_graph", { query: "#MCP" })` -> Renders a mini-graph of all MCPs.

## 📅 Execution Plan
1.  Provision `data.json` for Juggl.
2.  Create `dv_graph.js` template.
3.  Inject into `00_HOME.md`.
