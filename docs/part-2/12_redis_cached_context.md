## Redis Context Data Example

### Key Structure

```
ctx:{account_id}
```

Example: `ctx:acme_corp_12345`

---

### Cached Payload (JSON)

```json
{
  "account_id": "acme_corp_12345",
  "cached_at": "2024-12-10T14:32:15Z",
  "ttl_seconds": 300,

  "salesforce": {
    "account_name": "Acme Corp",
    "industry": "Manufacturing",
    "employee_count": 2500,
    "website": "acme.com",
    "owner": {
      "name": "Sarah Chen",
      "email": "sarah.chen@parable.com"
    },
    "opportunity": {
      "id": "opp_789xyz",
      "name": "Acme Corp - Enterprise License",
      "stage": "Demo",
      "amount": 150000,
      "close_date": "2025-01-31",
      "probability": 40,
      "next_step": "Technical deep-dive scheduled",
      "days_in_stage": 12
    },
    "contacts": [
      {
        "name": "Jane Martinez",
        "title": "CTO",
        "email": "jane.martinez@acme.com",
        "role": "Economic Buyer"
      },
      {
        "name": "Bob Wilson",
        "title": "VP Engineering",
        "email": "bob.wilson@acme.com",
        "role": "Technical Evaluator"
      }
    ],
    "last_activity": {
      "type": "Call",
      "date": "2024-12-07",
      "subject": "Discovery call - API requirements"
    }
  },

  "jira": {
    "project_key": "ACME",
    "open_tickets": [
      {
        "key": "ACME-456",
        "summary": "API latency concerns - need benchmarks",
        "status": "In Progress",
        "assignee": "John Park (SE)",
        "priority": "High",
        "created": "2024-12-05",
        "labels": ["blocker", "technical"]
      },
      {
        "key": "ACME-423",
        "summary": "SSO integration questions",
        "status": "Done",
        "assignee": "Mike Torres (SE)",
        "priority": "Medium",
        "resolved": "2024-12-08"
      }
    ],
    "blocker_count": 1
  },

  "slack": {
    "channel_id": "C_acme_deal",
    "recent_threads": [
      {
        "timestamp": "2024-12-09T16:45:00Z",
        "author": "John Park",
        "preview": "Finished the API benchmark doc, ready for Sarah to send",
        "thread_reply_count": 3
      },
      {
        "timestamp": "2024-12-08T11:20:00Z",
        "author": "Sarah Chen",
        "preview": "Jane mentioned they're comparing us to Gong - need competitive positioning",
        "thread_reply_count": 7
      }
    ],
    "se_mentions": [
      {
        "se_name": "John Park",
        "last_active": "2024-12-10T14:15:00Z",
        "status": "active"
      }
    ]
  },

  "notion": {
    "account_page_id": "notion_abc123",
    "manager_flags": [
      {
        "flag": "strategic_account",
        "set_by": "David Kim (Sales Director)",
        "note": "Logo win important for manufacturing vertical"
      }
    ],
    "weekly_summary": {
      "week_of": "2024-12-09",
      "status": "On Track",
      "highlights": [
        "Technical concerns being addressed by SE team",
        "Budget confirmed, procurement timeline unclear"
      ],
      "risks": ["Competitor (Gong) also in evaluation"]
    }
  },

  "derived": {
    "deal_health": "yellow",
    "days_since_last_contact": 3,
    "has_active_blocker": true,
    "primary_blocker": "ACME-456: API latency concerns",
    "se_assigned": "John Park",
    "se_available_now": true,
    "competitive_threat": "Gong"
  }
}
```

---

### Field Sources

| Section      | Source API             | Key Fields                                 |
| ------------ | ---------------------- | ------------------------------------------ |
| `salesforce` | Salesforce REST API    | Account, Opportunity, Contacts, Activities |
| `jira`       | Jira Cloud API         | Issues filtered by account label           |
| `slack`      | Slack Web API          | Channel history, user presence             |
| `notion`     | Notion API             | Database query for account page            |
| `derived`    | Computed at cache time | Aggregated signals for quick access        |

---

### How It's Used in Workflow

**Phase 1 (Pre-call brief):**

```python
context = await redis.get(f"ctx:{account_id}")

brief = f"""📞 {context['salesforce']['account_name']} ({context['salesforce']['opportunity']['stage']})
💰 ${context['salesforce']['opportunity']['amount']:,} ARR
⚠️ Blocker: {context['derived']['primary_blocker']}
✅ SE {context['derived']['se_assigned']} {'available' if context['derived']['se_available_now'] else 'busy'}"""
```

**Phase 3 (Post-call extraction validation):**

```python
# Anomaly detection uses cached baseline
extracted_arr = 500000
historical_arr = context['salesforce']['opportunity']['amount']  # 150000

if extracted_arr > historical_arr * 2:
    anomaly_flag = True  # $500K is 3.3x the $150K baseline
```

---

```python
async def fetch_and_cache_context(account_id: str) -> dict:
    # 1. Parallel API calls
    sf_data, jira_data, slack_data, notion_data = await asyncio.gather(
        salesforce.get_account(account_id),
        jira.get_open_tickets(account_id),
        slack.get_recent_threads(account_id),
        notion.get_manager_flags(account_id)
    )

    # 2. Compute derived fields ← THIS IS WHERE IT HAPPENS
    derived = {
        "has_active_blocker": any(t["status"] != "Done" and "blocker" in t.get("labels", [])
                                  for t in jira_data["open_tickets"]),
        "primary_blocker": next(
            (f"{t['key']}: {t['summary']}" for t in jira_data["open_tickets"]
             if "blocker" in t.get("labels", [])),
            None
        ),
        "se_available_now": any(m["status"] == "active" for m in slack_data["se_mentions"]),
        "se_assigned": next((m["se_name"] for m in slack_data["se_mentions"]), None),
        "days_since_last_contact": (datetime.now() - parse(sf_data["last_activity"]["date"])).days,
        "deal_health": compute_deal_health(sf_data, jira_data),
        "competitive_threat": extract_competitor(slack_data["recent_threads"])
    }

    # 3. Assemble complete context
    context = {
        "account_id": account_id,
        "cached_at": datetime.utcnow().isoformat(),
        "salesforce": sf_data,
        "jira": jira_data,
        "slack": slack_data,
        "notion": notion_data,
        "derived": derived  # ← Pre-computed for fast access
    }

    # 4. Cache it
    await redis.set(f"ctx:{account_id}", json.dumps(context), ex=300)

    return context

```
