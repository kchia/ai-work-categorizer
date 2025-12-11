### Why Agentic LLM Over Supervised ML?

**Comparison**:

| Dimension | Supervised ML (e.g., XGBoost) | Agentic LLM (GPT-4 + Tools) |
Winner |
| ------------------ | ---------------------------------------------------- | -------------------------------------------- |
------ |
| **How it works** | Train classifier on labeled calls → predict category | LLM reasons → calls tools → validates → acts |

-      |
  | **Training data** | Requires 10k+ labeled examples upfront | Zero-shot, works immediately | ✅
  LLM |
  | **Accuracy** | 85% (brittle, breaks on edge cases) | 95% (handles nuance) | ✅
  LLM |
  | **Explainability** | ❌ Black box (why did it decide X?) | ✅ Shows reasoning + cites sources | ✅ LLM |
  | **Adaptability** | ❌ Requires retraining for new products | ✅ Update prompt (5 min) | ✅ LLM |
  | **Multi-system** | ❌ Can't query Jira/Slack/SF during inference | ✅ Calls APIs as part of reasoning | ✅ LLM |
  | **Cost** | $0.001/call (cheaper) | $0.15/call (150x more expensive) | ❌
  LLM |
  | **Latency** | 50ms (faster) | 2 sec (40x slower) | ❌
  LLM |

**Example Where Supervised ML Fails**:

```
Transcript: "I think we should probably circle back on pricing next week,
             assuming the technical team is aligned."

Supervised ML:
├── Detects keywords: "pricing", "next week"
├── Output: action_item = "Send pricing", confidence = 0.82
├── Problem: Missed conditionality ("probably", "assuming")
└── Result: Creates wrong action item

Agentic LLM:
├── Reasoning: "Customer said 'probably' and 'assuming' - soft commitment"
├── Tool call: query_jira(account="Acme", keyword="technical")
├── Result: Found Jira #456 "API latency" (blocking technical alignment)
├── Output: action_item = "Follow up on pricing AFTER technical alignment (Jira #456 resolved)"
└── Result: Correct, nuanced interpretation
```

**Decision**: **Agentic LLM is worth 150x cost premium** because:

1. Sales conversations are unstructured (infinite phrasing variations)
2. Nuance matters ("soft no" vs "hard no" changes deal stage)
3. Multi-system awareness (checks Jira before promising timeline)
4. 95% accuracy vs 85% → 10% fewer errors = $2.8M/year in prevented mistakes
