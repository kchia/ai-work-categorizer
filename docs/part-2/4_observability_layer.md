# Reusable Observability Layer (Streamlined)

SSO event logs are the **core telemetry source** for reconstructing user behavior. They let you:

- Trace end-to-end user journeys
- Quantify friction in authentication and tool access
- Distinguish habitual vs anomalous patterns
- Measure tool sprawl based on app transitions
- Surface burnout precursors (overload, repeated failures, excessive context switching)

But the logs are only one part of the picture.
In the Round 1 architecture, we introduced a **normalized event stream**: unified schema, ETL versioning, identity linkage, and consistent observability hooks. That means Round 2—the agentic workflow orchestrator—doesn’t start from raw, noisy logs. It starts from a coherent behavioral telemetry layer.

**Round 1 built the identity-centric observability fabric.
Round 2 consumes that fabric to:**

1. Map friction across authentication flows
2. Model user and workload-level behavioral patterns
3. Quantify cross-tool journeys and sprawl
4. Link friction and overload to burnout and attrition signals

No new instrumentation is needed—the Round 1 payload already contains everything required.

---

# Three Properties That Make the Data Reusable

## 1. Identity-Level Linkage

Every event includes the user (`actor.id`), the alternate ID, and session identifiers.
→ Enables longitudinal modeling by user, team, region, device, and workload.

## 2. Context-Rich Request Fingerprints

The logs carry:

- Authentication step
- IP / geo / device metadata
- User agent
- Built-in risk/behavior signals (new device, velocity, new geo)
- Error & outcome fields
- Target application identifiers

Each event is effectively a **behavioral signature**, not just an auth record.

## 3. Transaction-Level Granularity

Transaction IDs + millisecond timestamps allow sequencing events into flows.
→ You can reconstruct where friction happens and how users navigate across systems.

The Round 1 architecture gives you identity-linked, richly annotated telemetry describing _what users attempted_, _from where_, _with what context_, and _what happened next_. That is the foundation for reliable behavioral modeling.

---

# Which Parts of the Sample Data Enable Behavior Modeling?

## Identity + Session

```json
"actor": { "id": "...", "alternateId": "..." },
"authenticationContext": { "rootSessionId": "...", "externalSessionId": "..." }
```

→ Lets you cluster activity by identity and reconstruct sessions.

---

## Behavioral + Risk Signals

From `debugContext.debugData.logOnlySecurityData`:

```json
"behaviors": {
  "New Geo-Location": "...",
  "New Device": "...",
  "New IP": "...",
  "Velocity": "...",
  "New City": "..."
}
```

These are explicit behavioral features: anomaly signals, adaptation patterns, and indicators of friction cost (e.g., frequent device resets).

---

## Friction Indicators

Key fields include:

- `authenticationStep` → Higher = more friction
- `outcome.result` / `outcome.reason` → Success, MFA fail, lockout
- `eventType` / `legacyEventType` → Where the user was in the flow
- `responseTime` (when present) → Latency
- `redirectUri`, `requestUri` → Looping or broken flows

These enable reconstruction of stuck journeys, repeated MFA challenges, and high-friction segments.

---

# How the Agentic Workflow Orchestrator Reuses This Observability

The orchestrator relies on two capabilities:

## A. Behavior Modeling

It answers questions like:

- What does “normal” behavior look like for this role or team?
- Which groups experience abnormal friction or risky patterns?
- Who is switching tools excessively (a burnout signal)?
- Where do recurrent authentication loops appear?

All of this is directly supported by the identity-linked telemetry.

## B. Friction Mapping

Friction comes from:

1. Repeated MFA or step-up challenges
2. Geo/IP/device-driven risk triggers
3. Redirect loops or session resets
4. High-frequency tool switching
5. Latency spikes or slow auth responses

The orchestrator uses these signals to:

- Map events to real workflows
- Quantify where users struggle
- Connect friction to downstream effects like attrition, misconfiguration, or low adoption
