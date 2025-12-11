# Tool definitions for GPT-4 function calling

```json
tools = [ # READ TOOLS (safe, no side effects)
{
"name": "query_salesforce",
"description": "Get Salesforce account details, deal stage, last contact",
"parameters": {
"account_id": {"type": "string", "required": True},
"fields": {"type": "array", "items": {"type": "string"}}
}
},
{
"name": "query_jira",
"description": "Get open Jira tickets for an account",
"parameters": {
"account_id": {"type": "string"},
"status": {"type": "string", "enum": ["Open", "In Progress", "All"]}
}
},
{
"name": "get_slack_threads",
"description": "Get recent Slack conversations about an account",
"parameters": {
"account_name": {"type": "string"},
"days_back": {"type": "integer", "default": 30}
}
},
{
"name": "get_calendar_upcoming",
"description": "Get upcoming calls for a user",
"parameters": {
"user_id": {"type": "string"},
"hours_ahead": {"type": "integer", "default": 24}
}
},

    # WRITE TOOLS (require approval in Phase 1)
    {
        "name": "write_salesforce_note",
        "description": "Write a call note to Salesforce",
        "parameters": {
            "account_id": {"type": "string", "required": True},
            "note": {"type": "string", "required": True},
            "call_duration_seconds": {"type": "integer"},
            "next_steps": {"type": "array"},
            "confidence": {"type": "number"}  # AI's confidence in this note
        }
    },
    {
        "name": "draft_email",
        "description": "Draft a follow-up email in Gmail",
        "parameters": {
            "to": {"type": "string", "required": True},
            "subject": {"type": "string", "required": True},
            "body": {"type": "string", "required": True},
            "cc": {"type": "array"},
            "send_immediately": {"type": "boolean", "default": False}
        }
    },
    {
        "name": "update_jira_ticket",
        "description": "Add a comment to a Jira ticket",
        "parameters": {
            "ticket_id": {"type": "string", "required": True},
            "comment": {"type": "string", "required": True},
            "update_status": {"type": "string", "enum": ["Open", "In Progress", "Closed"]}
        }
    },
    {
        "name": "send_slack_message",
        "description": "Send a Slack message to a user or channel",
        "parameters": {
            "channel": {"type": "string"},
            "user_id": {"type": "string"},
            "message": {"type": "string", "required": True}
        }
    },
    {
        "name": "append_notion_page",
        "description": "Append content to a Notion page",
        "parameters": {
            "page_id": {"type": "string", "required": True},
            "content": {"type": "string", "required": True},
            "format": {"type": "string", "enum": ["markdown", "plain"]}
        }
    },

    # UTILITY TOOLS
    {
        "name": "transcribe_call",
        "description": "Transcribe call audio using Whisper",
        "parameters": {
            "call_recording_url": {"type": "string", "required": True},
            "language": {"type": "string", "default": "en"}
        }
    },
    {
        "name": "extract_structured_data",
        "description": "Extract CRM fields from transcript",
        "parameters": {
            "transcript": {"type": "string", "required": True},
            "schema": {"type": "object"}  # JSON schema for output
        }
    },
    {
        "name": "verify_claim",
        "description": "Verify a claim against the source transcript",
        "parameters": {
            "claim": {"type": "string", "required": True},
            "transcript": {"type": "string", "required": True}
        }
    }

]
```
