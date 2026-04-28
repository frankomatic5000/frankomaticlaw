---
name: arp-router
description: Agentic Router Protocol v1.0 — routes tasks to specialist agents, manages handoffs, bounce counts, and model selection
metadata:
  {
    "openclaw":
      {
        "emoji": "🧭",
        "requires": { "tools": ["sessions_spawn", "sessions_send", "write", "read"] },
        "primaryEnv": null
      }
  }
---

# arp-router

The Agentic Router Protocol (ARP) enforcement layer for GrowBiz Media. Frank uses this skill to route tasks to the correct specialist agent following ARP v1.0.

## When to Use

- Every task that needs specialist handling (code, marketing, finance, family)
- When building handoff envelopes between agents
- When tracking task lifecycle and bounce counts
- When selecting the right model for a spawned agent

## When NOT to Use

- Simple tasks Frank can handle directly (orchestration, quick answers)
- Tasks requiring human approval first (use approval workflow)
- Tasks that have already bounced twice (escalate to Rod)

## Core Concepts

### Domain Ownership Matrix

| Domain | Owner | Examples |
|--------|-------|----------|
| Engineering | rodzilla | Code, specs, deploys, debugging |
| Marketing | frankcmo | Social, SEO, content, analytics |
| Finance | frankcfo | QuickBooks, grants, forecasting |
| Family | severino | Calendar, travel, kids, birthdays |
| Orchestration | frank | Routing, approvals, budget |

### Handoff Envelope Format

Every spawn includes:

```
---HANDOFF---
FROM: frank
TO: [agent-id]
TASK-ID: TASK-[XXXX]
TIMESTAMP: [ISO 8601]
DOMAIN: [code|social|finance|family|email|general]
ACTION: [single verb phrase]
BRAND: [imigrou|studios|magazine|clipiq|vaptlux|services|doodletype|zecaos|family|none]
PRIORITY: [low|medium|high|critical]
CONTEXT: [3-5 sentences max]
INPUTS: [key: value]
APPROVAL: [none|rod|karine|both]
RETURN-TO: frank
BOUNCE-COUNT: [0-2]
---END---
```

### Model Selection Matrix

| Agent | Default Model | Escalation Trigger |
|-------|---------------|-------------------|
| rodzilla | ollama/kimi-k2.5:cloud | openrouter/deepseek/deepseek-r1 for architecture, security |
| frankcmo | ollama/kimi-k2.5:cloud | ollama/qwen3.5:cloud for content synthesis |
| frankcfo | ollama/kimi-k2.5:cloud | openrouter/deepseek/deepseek-chat for narrative |
| severino | ollama/kimi-k2.5:cloud | ollama/qwen3.5:cloud for complex travel |

## Usage

### Route to Specialist

```
Use arp-router to route this task to the correct specialist.

Task: [description]
Domain hint: [code|social|finance|family]
Priority: [low|medium|high|critical]
Brand context: [which brand]
```

The skill will:
1. Classify the domain
2. Select the owning agent
3. Build the handoff envelope
4. Spawn with correct model
5. Track in task registry

### Check Task Status

```
Check status of task TASK-[XXXX] in the task registry.
```

### Model Escalation

```
Spawn rodzilla with deepseek-r1 for this architecture decision.
```

## Implementation Notes

### Task Registry

Tasks are tracked in `~/.openclaw/workspace/tasks/TASK-[XXXX].md`:
- Status: open|in-progress|complete|blocked|escalated
- Bounce count: 0-2
- Specialist assignments
- Return envelope from specialist

### Bounce Count Rules

- 0: Normal routing
- 1: Second attempt, add note: "Second try—be definitive"
- 2: HARD STOP, escalate to Rod

### Loop Prevention

Specialists NEVER spawn other specialists directly. They return STATUS:escalate to Frank, who decides next routing.

### Budget Integration

Each spawn includes budget tracking:
- Model cost lookup (from config)
- Estimated tokens
- Cumulative spend tracking

## Example Workflow

**User:** "Build a Next.js site for Imigrou"

**Frank (arp-router):**
1. Classify: DOMAIN=code, BRAND=imigrou
2. Select: TO=rodzilla
3. Build envelope with context
4. Spawn: `sessions_spawn({ agentId: "rodzilla", model: "ollama/kimi-k2.5:cloud", ... })`
5. Write task file: `tasks/TASK-0001.md`
6. Wait for return

**RodZilla returns:**
- STATUS: complete
- OUTPUT: [code, specs, deploy instructions]
- TOKENS: [usage]

**Frank:** Synthesize for user, close task.

## ARP v1.0 Compliance

This skill enforces:
- ✅ Domain ownership (one task, one owner)
- ✅ Handoff envelope format
- ✅ Bounce counter (0→1→2→HARD STOP)
- ✅ One-direction rule (specialists don't route back)
- ✅ Model injection (workaround for OpenClaw bug #43680)
- ✅ Budget tracking per spawn

## Files

- Task registry: `~/.openclaw/workspace/tasks/`
- Active tasks: `tasks/TASK-[XXXX].md`
- Archive: `tasks/archive/`
