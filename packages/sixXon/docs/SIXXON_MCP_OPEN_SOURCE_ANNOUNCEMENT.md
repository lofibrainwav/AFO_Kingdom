# SixXon MCP: Open Source Announcement

**Date**: 2025-12-13  
**Purpose**: Contributing to Anthropic's MCP Ecosystem  
**Philosophy**: 眞善美孝永 (Truth, Goodness, Beauty, Serenity, Eternity)

---

## 🎉 Announcing SixXon MCP

We are proud to announce the open-source release of **SixXon MCP**, a reference-grade MCP (Model Context Protocol) server implementation that embodies the AFO Kingdom's philosophy of **眞善美孝永**.

This release is our way of **giving back to Anthropic** for open-sourcing MCP and building a thriving ecosystem that benefits all developers.

---

## What is SixXon MCP?

**SixXon MCP** is a production-ready MCP server that provides:

1. **Receipt-Based Evidence System** (眞 - Truth)
   - Every action generates a Receipt (evidence bundle)
   - No claims without proof
   - Full audit trail for accountability

2. **Humility Protocol** (美 - Beauty)
   - 3-line output by default
   - Complex internals hidden, elegant UX exposed
   - Cognitive load reduction as a core principle

3. **Auth Broker + Wallet** (善 - Goodness)
   - Prefer standards (OAuth) when a provider supports it
   - Support subscription (web login) flows via **user-controlled session capture + manual open**
   - Secure storage via Wallet (Keychain/Vault optional; never hardcode secrets)

4. **Trinity Toolflow** (孝 - Serenity)
   - Automated execution with risk scoring
   - AUTO_RUN gate: `Trinity Score >= 90 AND Risk < 10`
   - Human-in-the-loop for high-risk operations

5. **Philosophical Foundation** (永 - Eternity)
   - Built on 眞善美孝永 principles
   - Designed for long-term sustainability
   - Open source for eternal knowledge sharing

---

## Staged Release (Public First)

SixXon is intentionally released in stages to reduce misuse and friction:

- **Stage 0 (Public):** Receipt + status + explanation (a “calculator”)
- **Stage 1 (Builder):** Subscription auth (capture → wallet → open) for CLI usability
- **Stage 2 (Contributor):** Thin MCP tools (read/verify oriented)
- **Stage 3 (Internal):** OS/Toolflow/multi-agent operations (limited)

See: `docs/SIXXON_PUBLIC_RELEASE_STAGES.md`

## Key Features

### 1. Receipt System (Evidence-Based)

```bash
# Generate a Receipt (evidence bundle)
sixxon receipt

# Check status based on Receipt
sixxon status --receipt <id>

# Get 3-line explanation
sixxon explain --latest
```

**Why it matters**: No claims without proof. Every system state is verifiable through Receipts.

### 2. Auth Broker (OAuth 2.1)

```bash
# One-time login (OAuth flow)
sixxon auth login claude

# Check auth status
sixxon auth status

# Auto-refresh tokens
sixxon auth refresh
```

**Why it matters**: Secure, standard authentication where possible. For web-only subscription plans, SixXon uses a user-controlled capture + manual open flow.

See:
- `docs/SIXXON_AUTH_SUBSCRIPTION_FLOW.md`

### 3. Trinity Toolflow

```bash
# Execute with risk scoring
sixxon toolflow "deploy to production"

# AUTO_RUN if safe (Score >= 90, Risk < 10)
# ASK_COMMANDER if risky
# BLOCK if dangerous
```

**Why it matters**: Automated execution with safety gates. Serenity preserved.

### 4. Philosophy Integration

Every command respects the **眞善美孝永** principles:

- **眞 (Truth)**: Receipt-based evidence, no mock data
- **善 (Goodness)**: OAuth security, human consent
- **美 (Beauty)**: 3-line output, elegant UX
- **孝 (Serenity)**: Auto-refresh, friction reduction
- **永 (Eternity)**: Open source, long-term sustainability

---

## Installation

```bash
# Clone the repository
git clone https://github.com/afo-kingdom/sixxon-mcp.git
cd sixxon-mcp

# Install
pip install -e .

# Verify
sixxon --help
```

---

## Quick Start

### 1. Generate a Receipt

```bash
sixxon receipt --out my_first_receipt
```

This creates a Receipt bundle at `logs/receipts/my_first_receipt/` with:
- System state snapshot
- Service health checks
- Docker container status
- Usage logs (if available)

### 2. Check Status

```bash
sixxon status --receipt my_first_receipt
```

Output (3-line format):
```
Status: OK | Gate: OK
Next: Run `sixxon toolflow "your task"`
Receipt: logs/receipts/my_first_receipt
```

### 3. Authenticate (OAuth)

```bash
# Login once (OAuth flow)
sixxon auth login claude

# Status check
sixxon auth status
```

### 4. Execute Toolflow

```bash
sixxon toolflow "deploy to production"
```

The system will:
1. Calculate Trinity Score and Risk
2. If safe (Score >= 90, Risk < 10): AUTO_RUN
3. If risky: ASK_COMMANDER
4. If dangerous: BLOCK

---

## Architecture

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
Receipt Bundle Structure:
logs/receipts/<id>/
├── receipt.json          # Main Receipt (SSOT)
├── raw/
│   ├── *.stdout.txt     # Command outputs
│   ├── *.stderr.txt     # Error logs
│   ├── *.meta.txt       # Metadata
│   └── sixxon_status.json  # Status snapshot
```

**SSOT Principle**: Receipt is the single source of truth. No claims without Receipt.

---

## Philosophy: 眞善美孝永

### Truth (眞)

- Receipt-based evidence for every action
- No mock data or hardcoded values
- Full audit trail

### Goodness (善)

- OAuth 2.1 security
- Human-in-the-loop for high-risk operations
- Explicit consent before irreversible actions

### Beauty (美)

- 3-line output protocol (Humility Protocol)
- Sparse, serene interfaces
- Cognitive load reduction

### Serenity (孝)

- Auto-refresh tokens
- Friction reduction
- Flow state protection

### Eternity (永)

- Open source for eternal knowledge
- Long-term sustainability
- Principles outlive implementations

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](../TRINITY-OS/CONTRIBUTING.md) for guidelines.

**Core Principles**:
1. No mock data or hardcoded secrets
2. Receipt-based evidence for all claims
3. 3-line output protocol (Humility Protocol)
4. OAuth 2.1 for authentication

---

## License

MIT License - See [LICENSE](../TRINITY-OS/LICENSE)

---

## Acknowledgments

- **Anthropic**: For open-sourcing MCP and building a thriving ecosystem
- **AFO Kingdom Community**: For embodying 眞善美孝永 in every contribution
- **All Contributors**: For making this possible

---

## Links

- **GitHub**: https://github.com/afo-kingdom/sixxon-mcp
- **Documentation**: https://sixxon.afo-kingdom.org
- **Philosophy**: [AFO Kingdom Philosophy](./PHILOSOPHY.md)
- **MCP Specification**: https://modelcontextprotocol.io

---

## The Journey

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
