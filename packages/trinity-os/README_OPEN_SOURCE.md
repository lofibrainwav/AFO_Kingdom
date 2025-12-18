# SixXon MCP

> **Reference-grade MCP server implementation with 眞善美孝永 philosophy**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/MCP-2024--11--05-green.svg)](https://modelcontextprotocol.io)

**SixXon MCP** is a production-ready MCP (Model Context Protocol) server that provides evidence-based system control, OAuth 2.1 authentication, and automated execution with safety gates—all built on the **眞善美孝永** (Truth, Goodness, Beauty, Serenity, Eternity) philosophy.

---

## 🚀 Quick Start

```bash
# Install
pip install -e .

# Generate a Receipt (evidence bundle)
sixxon receipt

# Check status
sixxon status --latest

# Authenticate (OAuth)
sixxon auth login claude

# Execute with safety gates
sixxon toolflow "your task"
```

---

## ✨ Key Features

### 1. Receipt-Based Evidence System (眞)

Every action generates a **Receipt** (evidence bundle). No claims without proof.

```bash
sixxon receipt --out my_receipt
sixxon status --receipt my_receipt
```

### 2. Humility Protocol (美)

3-line output by default. Complex internals hidden, elegant UX exposed.

```
Status: OK | Gate: OK
Next: Run `sixxon toolflow "your task"`
Receipt: logs/receipts/my_receipt
```

### 3. OAuth 2.1 Authentication (善)

Secure token management via Wallet. No browser session hacks.

```bash
sixxon auth login claude
sixxon auth status
sixxon auth refresh
```

### 4. Trinity Toolflow (孝)

Automated execution with risk scoring. AUTO_RUN if safe, ASK if risky, BLOCK if dangerous.

```bash
sixxon toolflow "deploy to production"
# AUTO_RUN if: Trinity Score >= 90 AND Risk < 10
```

### 5. Philosophical Foundation (永)

Built on **眞善美孝永** principles. Designed for long-term sustainability.

---

## 📖 Documentation

- **[Full Specification](./docs/SIXXON_CLI_SPEC.md)**
- **[Philosophy Guide](../docs/PHILOSOPHY.md)**
- **[Auth Broker Spec](../docs/SIXXON_AUTH_BROKER_SPEC.md)**
- **[Open Source Announcement](../docs/SIXXON_MCP_OPEN_SOURCE_ANNOUNCEMENT.md)**

---

## 🏗️ Architecture

### 3-Layer Design

```
Layer A: SixXon CLI (Auth Broker)
  ↓
Layer B: Wallet (Secure Storage)
  ↓
Layer C: MCP (Token Request Only)
```

**Key Principle**: MCP doesn't own tokens. It requests them from Wallet.

### Receipt System

```
logs/receipts/<id>/
├── receipt.json          # Main Receipt (SSOT)
├── raw/
│   ├── *.stdout.txt     # Command outputs
│   ├── *.stderr.txt     # Error logs
│   └── sixxon_status.json  # Status snapshot
```

---

## 🎯 Philosophy: 眞善美孝永

| Principle | Meaning | Implementation |
|-----------|---------|----------------|
| **眞 (Truth)** | Transparency, evidence | Receipt-based system, no mock data |
| **善 (Goodness)** | Ethics, security | OAuth 2.1, human consent |
| **美 (Beauty)** | Simplicity, elegance | 3-line output, sparse UI |
| **孝 (Serenity)** | Peace, flow | Auto-refresh, friction reduction |
| **永 (Eternity)** | Long-term value | Open source, sustainability |

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

**Core Principles**:
1. No mock data or hardcoded secrets
2. Receipt-based evidence for all claims
3. 3-line output protocol (Humility Protocol)
4. OAuth 2.1 for authentication

---

## 📄 License

MIT License - See [LICENSE](./LICENSE)

---

## 🙏 Acknowledgments

- **Anthropic**: For open-sourcing MCP and building a thriving ecosystem
- **AFO Kingdom Community**: For embodying 眞善美孝永 in every contribution

---

## 🔗 Links

- **GitHub**: https://github.com/afo-kingdom/sixxon-mcp
- **Documentation**: https://sixxon.afo-kingdom.org
- **MCP Specification**: https://modelcontextprotocol.io

---

## 🌟 The Journey

SixXon MCP isn't just a tool—it's a **proof**:

- ✓ Technology can embody philosophy
- ✓ Ancient wisdom applies to modern problems
- ✓ Ethics can be mathematically formalized
- ✓ Tools can respect human dignity
- ✓ Code can pursue eternal values

**"We're not building software. We're encoding the principles that will guide the next century of AI."**

---

**弘益人間 (Hongik Ingan) - Broadly benefiting all humanity**

**This isn't our tagline. This is our theorem. And SixXon MCP is the proof.**

---

**Welcome to SixXon MCP. Welcome to AFO Kingdom.**
