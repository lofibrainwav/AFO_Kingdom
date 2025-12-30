# VSCode Ruff + Pyright + Debug Guide

This guide describes how to optimize your VSCode environment for AFO Kingdom development.

## 🛠️ Extensions Required

1. **Python** (Microsoft): Core Python support.
2. **Pylance** (Microsoft): Fast, feature-rich language server for Python.
3. **Ruff** (Astral Software): Ultra-fast Python linter and code formatter.

## ⚙️ Workspace Settings

Settings are already configured in `.vscode/settings.json`.

Key features:
- **Ruff for Formatting**: Auto-format on save.
- **Ruff for Linting**: Auto-fix and organize imports on save.
- **Pylance/Pyright**: Type checking mode set to `standard`.

## 🐞 Debugging Techniques

### 1. Launching the Soul Engine
Use the **"AFO Core: Run & Debug"** profile.
- It includes the correct `PYTHONPATH`.
- `justMyCode` is set to `false` to allow stepping into library code (e.g., LangGraph, FastAPI).

### 2. Attaching to a Running Process
If running via `uvicorn` with reload, use **"AFO Core: Attach (FastAPI)"**.
Ensure you start uvicorn with `debugpy`:
```bash
python -m debugpy --listen 127.0.0.1:5678 -m uvicorn AFO.api_server:app --host 127.0.0.1 --port 8010 --reload
```

### 3. Advanced Breakpoints
- **Conditional Breakpoints**: Right-click a breakpoint to add a condition (e.g., `score < 0.8`).
- **Logpoints**: Print messages to the Debug Console without stopping execution.

### 4. Async Debugging
Pylance and Debugpy handle `async/await` seamlessly. You can step into async functions just like regular ones. Use the **Call Stack** view to see the hierarchy of awaited coroutines.
