---
name: ragas-evaluator
description: Evaluates RAG quality using 4 metrics - Faithfulness, Relevancy, Precision, Recall.
license: MIT
compatibility:
  - claude-code
  - codex
  - cursor
metadata:
  version: "1.2.0"
  category: analysis-evaluation
  author: AFO Kingdom
  philosophy_scores:
    truth: 99
    goodness: 92
    beauty: 88
    serenity: 85
---

# Ragas RAG Quality Evaluator

Scientific evaluation of RAG system quality using the Ragas framework.

## Metrics

| Metric | Description |
|--------|-------------|
| Faithfulness | Answer grounded in retrieved context |
| Answer Relevancy | Answer addresses the question |
| Context Precision | Retrieved docs are relevant |
| Context Recall | All needed info was retrieved |

## Usage

```python
from AFO.evaluation import RagasEvaluator

scores = await evaluator.evaluate(
    question="What is Trinity Score?",
    answer="Trinity Score is a 5-pillar philosophy metric...",
    contexts=["Trinity Score measures Truth, Goodness..."]
)
```
