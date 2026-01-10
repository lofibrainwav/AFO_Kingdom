# ⚠️ Quarantine Zone - Credential Tools

> **DO NOT EXECUTE** any scripts in this directory.

## Purpose

This directory contains **archived credential extraction scripts** that were quarantined during Phase 15 Security Seal (2026-01-08).

These scripts were previously used for development/debugging purposes but pose security risks if left in active codebase.

## Contents

| File | Description | Risk |
|------|-------------|------|
| `decrypt_chrome_cookies.py` | Chrome cookie extractor | HIGH |
| `extract_chrome_cookies.py` | Chrome cookie extractor | HIGH |
| `extract_openai_auth_token.py` | OpenAI token extractor | CRITICAL |
| `extract_openai_force.py` | OpenAI force extractor | CRITICAL |
| `extract_claude_force.py` | Claude token extractor | CRITICAL |
| `grok_chrome_launch.py` | Grok Chrome launcher | MEDIUM |
| `grok_interactive.py` | Grok interactive script | MEDIUM |
| `grok_safari_connect.py` | Grok Safari connector | MEDIUM |

## Policy

1. **No Execution**: These scripts must never be executed in production
2. **Evidence Preservation**: Kept for audit trail purposes
3. **Future Plan**: Migrate to separate private repository if needed

## Quarantine Date

- **Date**: 2026-01-08
- **Commit**: `9c0ad643`
- **Phase**: 15 (Security Seal)
- **Author**: Chancellor (AFO Kingdom)

---

*眞善美孝永 - Protected by Trinity Philosophy*
