---
name: multi-cloud-backup
description: High-availability backup system with 99.9% uptime across Hetzner and AWS with automatic failover.
license: MIT
compatibility:
  - claude-code
  - codex
  - cursor
metadata:
  version: "1.0.0"
  category: integration
  author: AFO Kingdom
  philosophy_scores:
    truth: 95
    goodness: 96
    beauty: 92
    serenity: 98
---

# Multi-Cloud Backup (Hetzner + AWS)

Enterprise-grade backup and failover system for the AFO Kingdom.

## Architecture

- Primary: Hetzner Cloud (cost-effective)
- Secondary: AWS (global reach)
- Automatic failover on health check failure
- ICCLS gap healing for data consistency

## Capabilities

- `health_check`: Verify backup system status
- `failover`: Switch between cloud providers
- `gap_healing`: Synchronize data gaps
- `uptime_monitoring`: Track availability metrics
