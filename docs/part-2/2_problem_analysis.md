# Problem Statement & Quantification

---

"I have to get on calls with my sales prospects with 3CX, log in my notes in Salesforce, then send an email to the client with an overview, update my Jira ticket. I'm coordinating with my Solutions Engineer on slack in real time. Finally, my boss wants weekly Notion pages with prospect specific updates. I get on 15 calls a day! It's too much writing, too much admin. I feel like I don't have enough time to sell"

## **The Core Problem**

### **Daily Workflow Breakdown (Per Rep)**

```
Selling activity:
├── 15 sales calls × 30 min = 7.5 hours (value creation)

Admin & overhead:
├── Post-call notes (Salesforce): 8 min × 15 = 2.0 hours
├── Follow-up emails: 6 min × 15 = 1.5 hours
├── Jira ticket updates: 4 min × 15 = 1.0 hour
├── Pre-call preparation: 5 min × 15 = 1.25 hours
├── Slack coordination (SE, managers): ~45 min/day
└── Weekly Notion summary: ~45 min/day
────────────────────────────────────────────────────────────
Total explicit admin: **6.5 hours/day**
Context switching tax (90+ app transitions): **1–1.5 hours/day**
Total workflow demand: **~14 hours/day**
```

**Key insight:**
Half the rep’s effective day is consumed by non-selling work → systemic friction and predictable revenue leakage.

---

## **Financial Impact (100-Rep Enterprise Sales Org)**

### **Hard Costs (Guaranteed Waste)**

| Component                    | Formula                                    | Annual Impact    |
| ---------------------------- | ------------------------------------------ | ---------------- |
| **Admin labor waste**        | 100 reps × 6.5 hrs/day × 250 days × $80/hr | **$13,000,000**  |
| **Burnout-driven attrition** | ~20% excess attrition × $100k backfill     | **$2,000,000**   |
| **Tool sprawl (6 systems)**  | $468k–$792k/year                           | **$0.5–0.8M**    |
| **Total Hard Cost**          |                                            | **$14–15M/year** |

### **Opportunity Cost (Revenue Uplift Potential)**

```
Admin time recovered: 6.5 hrs/day → ~5 additional calls/day (conservative)

Org-wide volume:
├── 5 calls × 100 reps × 250 days = 125,000 incremental calls/year

Revenue impact range (close rate × ACV):
├── Conservative: 25,000 sales qualified calls x 0.5% close × $30k ACV = ~$3.75M org
├── Baseline: 30,000 sales qualified calls x 1.5% close × $40k ACV = ~$18M org
└── Optimistic: 35,000 sales qualified calls x 2.5% close × $50k ACV = ~$44M org
```

**Opportunity range:** **$4–44M/year**

---

### **Total Annual Impact (100 Reps)**

```
HARD COSTS:          $14–15M
OPPORTUNITY:         $4–44M
──────────────────────────────
TOTAL IMPACT:        $18–59M/year
```

---

## Parable's CEO Questions

| Category                                                     | Problem / Opportunity             | Key Details                                                                                                                                                 |
| ------------------------------------------------------------ | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Where's the bureaucracy?**                                 | Redundant data entry              | Same call summary re-typed into Salesforce, email, Jira, Slack, and Notion for 6 different stakeholders                                                     |
| **Where's the friction?**                                    | Context switching overload        | 90+ context switches/day across 6 tools; 6.5 hours of daily admin; reps report "no time to sell"                                                            |
| **Where's the waste?**                                       | Financial drain                   | ~$13M/year (100-rep team) + $5–15M in realistic revenue left on the table                                                                                   |
| **Where can we automate?**                                   | High-value, repetitive tasks      | Call transcription, CRM note generation, follow-up emails, Jira ticket creation, manager reporting — all derived from the same underlying call intelligence |
| **How can we use AI to make the team 100x more productive?** | End-to-end workflow orchestration | Deploy an agent layer that sits atop existing systems and orchestrates workflows, returning multiple hours/day to each rep                                  |

One input (the call) → one AI system → multiple outputs formatted per destination. The 100x productivity gain comes from collapsing the write-once-copy-six pattern into write-zero-distribute-everywhere.

---

## Why Existing Solutions Fail

| Solution Type             | Examples            | Why It Fails                                                                                                                             |
| ------------------------- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Call intelligence**     | Gong, Chorus        | Transcribes calls but does **not** update Salesforce, draft follow-up emails, or push info to Jira/Notion → still ~26 min admin per call |
| **CRM automation**        | Salesforce Einstein | Automates _inside Salesforce only_ → ignores Slack, email, Jira, Notion, 3CX                                                             |
| **Integration platforms** | Zapier, Workato     | Rule-based, brittle, cannot infer nuanced sales context or multi-step workflows                                                          |
| **Unified workspace**     | Custom portals      | Consolidates UI but doesn’t eliminate **data entry**, context switching, or weekly reporting                                             |

### **The Gap**

> **No existing tool provides autonomous, context-aware workflow orchestration across all 6 systems.**
