---
name: health-monitor
description: Monitors 11 critical AFO system organs (五臟六腑) and generates comprehensive health reports with auto-recovery capabilities.
license: MIT
compatibility:
  - claude-code
  - codex
  - cursor
metadata:
  version: "1.5.0"
  category: health-monitoring
  author: AFO Kingdom
  philosophy_scores:
    truth: 100
    goodness: 100
    beauty: 95
    serenity: 100
---

# 11-Organ Health Monitor (五臟六腑)

Comprehensive health monitoring system for the AFO Kingdom infrastructure, tracking 11 critical system components.

## System Organs

### 五臟 (5 Vital Organs)
| Organ | System | Health Check |
|-------|--------|--------------|
| Heart (心) | Redis | Connection, memory usage, latency |
| Liver (肝) | PostgreSQL | Connection pool, query performance |
| Spleen (脾) | API Server | Response time, error rate |
| Lungs (肺) | Qdrant/ChromaDB | Vector store health, index status |
| Kidneys (腎) | Docker | Container status, resource usage |

### 六腑 (6 Hollow Organs)
| Organ | System | Health Check |
|-------|--------|--------------|
| Gallbladder (膽) | n8n Workflows | Execution status, queue depth |
| Stomach (胃) | LLM Router | Provider availability, latency |
| Small Intestine (小腸) | RAG Pipeline | Retrieval accuracy, throughput |
| Large Intestine (大腸) | Log Aggregator | Storage usage, ingestion rate |
| Bladder (膀胱) | Cache Layer | Hit rate, eviction rate |
| Triple Burner (三焦) | Network | Connectivity, bandwidth |

## Usage

```bash
# Quick health check
python scripts/verify_kingdom_core.py

# Comprehensive report
python scripts/comprehensive_system_check.py
```

## Output Format

```json
{
  "timestamp": "2025-12-25T10:00:00Z",
  "overall_status": "healthy",
  "organs": {
    "heart_redis": {"status": "healthy", "latency_ms": 2},
    "liver_postgresql": {"status": "healthy", "pool_usage": "40%"},
    "spleen_api": {"status": "healthy", "response_ms": 45},
    "lungs_qdrant": {"status": "healthy", "vectors": 125000},
    "kidneys_docker": {"status": "healthy", "containers": 8}
  },
  "trinity_score": 0.98,
  "recommendations": []
}
```

## Auto-Recovery

When an organ is unhealthy, the monitor can trigger automatic recovery:

1. **Restart**: Restart unhealthy containers
2. **Failover**: Switch to backup systems
3. **Alert**: Notify administrators via Discord/Slack
4. **Heal**: Execute predefined healing scripts
