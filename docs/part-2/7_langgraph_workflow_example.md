```python
from langgraph.graph import StateGraph, END

# Define workflow state
class WorkflowState(TypedDict):
    call_id: str
    transcript: str
    extracted_data: dict
    salesforce_note: str
    email_draft: str
    jira_updates: list
    human_approval: bool
    confidence_score: float

# Build workflow graph
workflow = StateGraph(WorkflowState)

# Add nodes
workflow.add_node("transcribe", transcribe_call)
workflow.add_node("extract", extract_structured_data)
workflow.add_node("verify", verify_facts)
workflow.add_node("write_salesforce", write_sf_note)
workflow.add_node("draft_email", draft_follow_up)
workflow.add_node("update_jira", update_jira_tickets)

# Define conditional edges
def should_get_approval(state):
    """Require human approval if confidence low"""
    if state["confidence_score"] < 0.95:
        return "human_review"
    return "auto_execute"

workflow.add_conditional_edges(
    "verify",
    should_get_approval,
    {
        "human_review": "wait_for_approval",
        "auto_execute": "write_salesforce"
    }
)

# Human-in-loop node
workflow.add_node("wait_for_approval", human_approval_gate)

# Parallel execution for writes
workflow.add_node("parallel_writes", lambda state: {
    "salesforce": write_salesforce.invoke(state),
    "email": draft_email.invoke(state),
    "jira": update_jira.invoke(state),
})

workflow.set_entry_point("transcribe")
workflow.add_edge("transcribe", "extract")
workflow.add_edge("extract", "verify")
workflow.add_edge("parallel_writes", END)

agent = workflow.compile()
```
