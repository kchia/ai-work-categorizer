## Agentic Solution: Work Categorizer

1. Queries 90-day app usage patterns from BigQuery (cached nightly)
2. Analyzes patterns using LLM few-shot learning with industry benchmarks
3. Categorizes users with natural language explanations ("Heavy GitHub + Jira + Figma = Frontend Engineer signature")
4. Suggests role-specific productivity optimizations (e.g., GitHub workflow automation for engineers,
   Salesforce shortcuts for sales)
5. Work categorization transforms generic IT policies into role-specific optimizations—cutting measurable waste (unused licenses, excessive
   auth) while improving what matters (onboarding speed, tool access).

## **Why Agentic Workflows > Traditional ML**

Parable's customers are CEOs who need explainable insights. An agentic workflow can say 'Employee X wastes time BECAUSE...' with citations to raw data. A clustering model says 'User in cluster 3' - that's not actionable. At petabyte scale with hundreds of clients, explainability and adaptability matter more than marginal accuracy gains.

**Traditional ML Approach:**

```
Train k-means clustering → "User is in cluster 3"
```

**Problems:**

- Not explainable to CEOs
- Requires retraining for new apps
- No natural language output
- Brittle edge cases

**Agentic Workflow Approach:**

```
LLM Agent with tools → "This user is an engineer BECAUSE they use GitHub, Jira, and Slack together 80% of the time. Confidence: 95%."
```

**Benefits:**

- Explainable with citations
- Adapts to new apps without retraining
- Natural language for CEOs
- Reasons through edge cases
- Few-shot learning (works with limited data)
