## Risk Management & Mitigation

### AI-Specific Risk Matrix

| Risk                                              | Probability        | Impact                     | Severity    | Mitigation Strategy                                                                        |
| ------------------------------------------------- | ------------------ | -------------------------- | ----------- | ------------------------------------------------------------------------------------------ |
| **Hallucination** (AI invents facts)              | Medium (5%)        | High (damages trust)       | 🔴 Critical | 4-layer defense: confidence scoring, fact-checking, source citations, progressive autonomy |
| **Bias** (favors certain deal types)              | Low (2%)           | Medium (skews reporting)   | 🟡 Moderate | Accuracy tracking by segment, fairness metrics, diverse training data                      |
| **Model drift** (GPT-4 API changes)               | Medium (quarterly) | High (breaks prompts)      | 🔴 Critical | Model pinning, regression testing, prompt versioning, graceful degradation                 |
| **PII leakage** (sensitive data exposed)          | Low (1%)           | Critical (legal liability) | 🔴 Critical | Redaction, encryption, SOC2 compliance, audit logs                                         |
| **Automation complacency** (users stop reviewing) | High (30% @ 6mo)   | High (errors unnoticed)    | 🔴 Critical | Random spot checks, engagement tracking, gamification                                      |
| **Adversarial gaming** (reps manipulate system)   | Low (5%)           | Medium (data integrity)    | 🟡 Moderate | Anomaly detection, manager dashboards, usage patterns                                      |
| **API failures** (Salesforce down)                | Low (0.5%)         | Medium (blocks workflow)   | 🟡 Moderate | Retry logic, graceful degradation, queue for later                                         |

### Critical Risk #1: Hallucination

**Definition**: AI generates plausible-sounding but factually incorrect information.

**Example Scenario**:

```
Call transcript: "We should probably circle back on pricing next week"

AI Output (hallucination):
├── Salesforce note: "Customer committed to pricing discussion on Dec 15"
├── Email draft: "Per our call, I'll send pricing details by Friday"
└── Problem:
    ├── Customer said "probably" (soft commitment)
    ├── AI invented "Dec 15" (date not mentioned)
    └── Consequence: Customer confused, deal damaged, trust lost
```

**4-Layer Mitigation Strategy**:

#### Layer 1: Confidence Scoring

```python
def get_confidence_score(llm_output, transcript):
    """
    Ask GPT-4 to score its own confidence
    """
    confidence_prompt = f"""
    You generated this output based on a call transcript.
    Rate your confidence (0-1) that this output is factually accurate.

    Output: {llm_output}
    Transcript: {transcript}

    Consider:
    - Is every claim directly supported by the transcript?
    - Did you make any assumptions?
    - Are there ambiguous statements?

    Response format: {{"confidence": 0.0-1.0, "reasoning": "..."}}
    """

    response = llm.invoke(confidence_prompt)
    return response["confidence"]

# Usage
if confidence < 0.95:
    require_human_review = True
    dont_auto_send = True
    flag_for_approval()
```

#### Layer 2: Fact-Checking Against Source

```python
def verify_claim(claim: str, transcript: str) -> dict:
    """
    Ground every claim in source transcript
    """
    # Extract keywords from claim
    keywords = extract_keywords(claim)

    # Search transcript for supporting evidence
    evidence = search_transcript(keywords, transcript, fuzzy=True)

    if not evidence:
        return {
            "verified": False,
            "risk": "HIGH",
            "reason": "No supporting evidence found in transcript"
        }

    # Measure evidence strength
    strength = calculate_evidence_strength(evidence, claim)

    if strength < 0.7:
        return {
            "verified": False,
            "risk": "MEDIUM",
            "reason": "Evidence too weak or ambiguous",
            "evidence": evidence.text
        }

    return {
        "verified": True,
        "timestamp": evidence.timestamp,
        "evidence": evidence.text
    }

# Example
claim = "Customer requested API documentation"
result = verify_claim(claim, transcript)
# Result: {"verified": True, "timestamp": "18:34", "evidence": "Can you send those API docs?"}
```

#### Layer 3: Mandatory Source Citations

```
Every AI output MUST include timestamp citations:

✅ GOOD:
"Customer requested API documentation (18:34)"
→ Verifiable, user can check transcript

❌ BAD:
"Customer requested API documentation"
→ No way to verify, could be hallucinated

Implementation:
- Prompt engineering: "ALWAYS cite timestamp for every claim"
- Post-processing: Validate every sentence has (MM:SS) citation
- UI: Make citations clickable (jumps to transcript timestamp)
```

#### Layer 4: Progressive Autonomy

```
Phase 1 (Months 1-3): PREVIEW MODE
├── AI writes outputs but doesn't send
├── Rep reviews every output + clicks "Approve" or edits
├── Goal: Build trust, collect error data
├── Success metric: 95% approval rate
└── Outcome: Baseline accuracy established

Phase 2 (Months 3-6): OPT-OUT MODE
├── AI auto-sends if:
│   ├── Confidence score >95% AND
│   ├── All claims fact-checked AND
│   └── No PII detected
├── Rep has 2-min window to cancel before sending
├── Goal: Validate autonomous operation
├── Success metric: 98% auto-approval, <2% errors
└── Outcome: Trust in autonomy established

Phase 3 (Months 6+): FULL AUTONOMY
├── AI writes directly to all systems
├── Random 10% of outputs require review (prevent complacency)
├── Rep can rollback any action within 24 hours
├── Goal: Scale to 100 reps
├── Success metric: <1% error rate, 80%+ engagement
└── Outcome: Production-ready autonomous system
```

**Hallucination Detection Dashboard** (for engineering team):

```
Weekly metrics:
├── Total outputs: 30,000 calls
├── Human edits: 450 (1.5%)
├── Hallucination breakdown:
│   ├── Invented dates/times: 180 (40% of errors)
│   ├── Wrong person attribution: 135 (30%)
│   ├── Overstated commitment: 90 (20%)
│   ├── Miscategorized blocker: 45 (10%)
└── Action: Update prompt with 10 new few-shot examples targeting date extraction
```

### Critical Risk #2: Automation Complacency

**The Danger**:

```
Week 1:  User carefully reviews every AI output (novelty effect)
Week 4:  User skims outputs (building trust)
Week 8:  User clicks "Approve All" without reading (automation complacency)
Week 12: AI errors propagate unnoticed → Customer complaints → Trust destroyed
```

**Why This Is Catastrophic**:

- AI isn't 100% accurate
- 5% error rate × 15 calls/day = **3-4 errors/day going unnoticed**
- One major error (wrong price quoted, wrong date promised) = lost deal

**Mitigation: Engagement Tracking + Forced Review**

#### 1. Random Spot Checks (10% of outputs)

```python
import random

def should_require_review(ai_output):
    """
    10% of outputs require mandatory review (cannot skip)
    """
    if random.random() < 0.10:
        return True, "random_spot_check"

    # Also require review if:
    if ai_output.confidence < 0.95:
        return True, "low_confidence"

    if ai_output.contains_pii:
        return True, "pii_detected"

    if ai_output.deal_value > 100000:  # $100k+ deals
        return True, "high_value_deal"

    return False, "auto_approved"

# UI implementation
if require_review:
    ui.show_modal(
        title="Review Required",
        body=ai_output.summary,
        can_skip=False,  # Must review, cannot dismiss
        track_time_spent=True
    )

    # Gamification
    if user_found_error:
        award_points(10)
        slack_notify_manager(f"{user} caught an AI error! Great attention to detail.")
```

#### 2. Engagement Dashboard (Manager View)

```
Sarah Johnson (Sales Rep):
├── Calls this week: 75
├── AI outputs generated: 75
├── AI outputs approved: 73 (97%)
├── AI outputs edited: 2 (3%)
├── Time spent reviewing: 15 min total (12 sec/call avg)
├── Last edit: 2 weeks ago ⚠️ WARNING
├── Error catch rate: 0% (last 50 calls) ⚠️ ALERT
└── Flag: Possible automation complacency

Manager action:
└── Schedule 1:1 conversation
    Script: "I notice you haven't edited any AI outputs in 2 weeks.
            Is the AI 100% accurate, or are we not reviewing thoroughly?
            Let's spot-check 5 random calls together."
```

#### 3. Accuracy Feedback Loop

```
Weekly Slack message to each rep:

"Sarah, your AI accuracy this week: 94% (4 errors caught)

Top errors you caught:
1. ✅ Missed technical blocker in Acme call (you caught it!)
2. ✅ AI said '95% confident' but you corrected sentiment
3. ✅ AI truncated Globex notes, you expanded context
4. ✅ Wrong next step date (AI said Friday, customer said next week)

Impact of your feedback:
├── Error #1: We've updated the prompt to detect this pattern
├── Error #4: Added date verification layer
└── Your edits improved the AI for all 100 reps!

Keep up the great work. The AI learns from you!"

Gamification:
├── Leaderboard: "Top AI trainers this week"
├── Badges: "Caught 10 errors", "100% review rate"
└── Team competition: Sales team A vs B accuracy
```

### Critical Risk #3: Model Drift

**What Is It?**
OpenAI updates GPT-4 → our prompts break → accuracy drops silently

**Real-World Example** (from industry):

```
2023-06-13: GPT-4 model update
├── Before: gpt-4-0613 good at structured extraction
├── After: gpt-4-1106-preview worse at JSON formatting
└── Result: Customers' prompts broke overnight
    ├── Accuracy: 85% → 72% (13% drop!)
    └── No warning, no migration guide
```

**Our Mitigation**:

#### 1. Model Pinning (Not "gpt-4", Use Specific Version)

```python
# ❌ BAD: Auto-updates to latest version
openai.ChatCompletion.create(
    model="gpt-4",  # This tracks the latest version
    messages=[...]
)

# ✅ GOOD: Pin to specific version
openai.ChatCompletion.create(
    model="gpt-4-0613",  # Frozen, won't change until we manually migrate
    messages=[...]
)

# Configuration management
MODEL_VERSIONS = {
    "orchestrator": "gpt-4-0613",
    "extractor": "gpt-4-0613",
    "summarizer": "gpt-3.5-turbo-0613"
}

# When we want to test new model:
if config.CANARY_MODE:
    model = "gpt-4-1106-preview"  # Test with 1% of traffic
else:
    model = MODEL_VERSIONS["orchestrator"]
```

#### 2. Regression Testing (Weekly, Automated)

```python
# Maintain 100-call "golden test set" (human-verified correct outputs)
def run_regression_test():
    """
    Test current AI against golden dataset
    Alert if accuracy drops >5%
    """
    test_calls = load_golden_dataset()  # 100 calls with verified outputs
    results = []

    for call in test_calls:
        ai_output = run_ai_pipeline(call.transcript)
        expected_output = call.gold_standard

        # Compare outputs
        accuracy = compare_outputs(ai_output, expected_output)
        results.append(accuracy)

    avg_accuracy = np.mean(results)
    baseline_accuracy = 0.95  # Established baseline

    if avg_accuracy < baseline_accuracy - 0.05:  # 5% drop
        alert_engineering_team(
            title="🚨 Model Drift Detected",
            message=f"Accuracy dropped from {baseline_accuracy} to {avg_accuracy}",
            severity="HIGH",
            action="Investigate prompt changes or model updates"
        )

    # Log to dashboard
    log_metric("regression_test_accuracy", avg_accuracy)

# Run weekly via Cloud Scheduler
schedule("0 9 * * 1", run_regression_test)  # Every Monday 9am
```

#### 3. Prompt Versioning (Git for Prompts)

```
prompts/
├── v1.0_baseline.txt (90% accuracy, deployed May 2024)
├── v1.1_few_shot.txt (92% accuracy, deployed Jun 2024)
├── v2.0_gpt4_turbo.txt (95% accuracy, deployed Aug 2024)
├── v2.1_soft_commitment.txt (97% accuracy, deployed Sep 2024)
└── changelog.md

# changelog.md
## v2.0 → v2.1 (Sep 15, 2024)
- **Change**: Added "soft commitment" detection rule
- **Reason**: 18% of calls had soft commitments misclassified as hard commitments
- **Examples added**: 10 new few-shot examples with "probably", "maybe", "assuming"
- **Impact**: +2% accuracy (95% → 97%)
- **Model**: gpt-4-0613 (unchanged)
- **Rollback plan**: Revert to v2.0 if regression detected
- **A/B test results**: v2.1 outperformed v2.0 by 2.3% (p<0.001, n=1000 calls)

# Code implementation
PROMPT_VERSION = "v2.1_soft_commitment"

def load_prompt(version):
    with open(f"prompts/{version}.txt") as f:
        return f.read()

prompt = load_prompt(PROMPT_VERSION)
```

#### 4. Graceful Degradation

```python
def orchestrate_call(call_id):
    """
    Try GPT-4 → fallback to GPT-3.5 → fallback to rules-based
    Never block the workflow
    """
    try:
        # Primary: GPT-4 Turbo
        result = gpt4_orchestrate(call_id, timeout=30)
        return result

    except (APIError, TimeoutError) as e:
        logger.warn(f"GPT-4 failed ({e}), falling back to GPT-3.5")

        try:
            # Fallback 1: GPT-3.5 Turbo (lower accuracy but faster)
            result = gpt35_orchestrate(call_id, timeout=15)
            result.metadata["degraded"] = True
            result.metadata["reason"] = "gpt4_failure"
            return result

        except (APIError, TimeoutError) as e2:
            logger.error(f"All LLMs failed ({e2}), using rule-based fallback")

            try:
                # Fallback 2: Rules-based extraction (70% accuracy but reliable)
                result = rules_based_extraction(call_id)
                result.metadata["degraded"] = True
                result.metadata["reason"] = "llm_failure"
                result.metadata["requires_review"] = True
                return result

            except Exception as e3:
                # Last resort: Flag for manual review
                logger.critical(f"All extraction methods failed ({e3})")
                alert_human(f"Manual review needed for call #{call_id}")
                return None

# Monitoring
if result.metadata.get("degraded"):
    increment_counter("degraded_mode_activations")
    alert_on_call_engineer("AI pipeline degraded mode activated")
```
