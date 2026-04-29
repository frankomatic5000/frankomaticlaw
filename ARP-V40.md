# ARP v4.0 — Agentic Router Protocol

> **Corporate OS for GrowBiz Holding Co. & Rezende Family Office**
> **Runtime:** OpenClaw 2026.4 + ByteRover Logistics Plugin
> **Agents:** 9-agent Hydra Mesh
> **Budget:** $100/mo (Hard-Capped)

---

## 1. Protocol Overview

ARP v4.0 standardizes communication across the 9-agent Hydra mesh. It bridges OpenClaw's native agent registry with structured inter-agent routing.

### Core Innovation: Agent Registry Routing
Unlike ARP v2.0 which relied on `sessions_send` to arbitrary session keys, ARP v4.0 uses **OpenClaw's agent registry** (`openclaw.json` → `agents.list`) for:
- Model assignment enforcement
- Workspace isolation
- Audit trail generation

---

## 2. The 9-Agent Hierarchy

| Agent | Role | Assigned Model* | Strategic Unit | Workspace |
|-------|------|-----------------|----------------|-----------|
| **Frank** | CEO / Orchestrator | `kimi-k2.6:cloud` | Velocity Engine | `workspace/` |
| **RodZilla** | CTO / Engineering | `glm-5.1:cloud` | Velocity Engine | `workspace/Rodzilla/` |
| **Jarbas** | CoS / Cultural Gate | `kimi-k2.6:cloud` | Aesthetic Soul | `workspace/Jarbas/` |
| **DaVinci** | CMO / UI-UX | `qwen3-vl:235b-cloud` | Aesthetic Soul | `workspace/DaVinci/` |
| **Franklyn** | CFO / Wealth Manager | `kimi-k2.6:cloud` | Immune System | `workspace/Franklyn/` |
| **X9** | Security & Compliance | `deepseek-v4-pro:cloud` | Immune System | `workspace/X9/` |
| **Radar** | Market Intelligence | `minimax-m2.7:cloud` | Velocity Engine | `workspace/Radar/` |
| **Bob** | Sales & Growth | `glm-5.1:cloud` | Velocity Engine | `workspace/Bob/` |
| **Severino** | Family Butler | `minimax-m2.7:cloud` | Immune System | `workspace/Severino/` |

\* **Model assignments are registered in `openclaw.json` but not enforced at runtime.**
See Section 4 "Spawn Patterns" for limitation details and workarounds.

**Current Runtime Behavior:** All subagents inherit parent model (`kimi-k2.6:cloud` when spawned from Frank).

---

## 3. Message Header (ARP-4.0)

```markdown
# AGENT ACTION (ARP-4.0)
Protocol: ARP-4.0
Type: [MESSAGE_TYPE]
From: [agent-id]
To: [agent-id]
Project: [brand-name]
Priority: [P0 | P1 | P2 | P3]
Status: [NEW | IN_PROGRESS | BLOCKED | READY | DONE]
Timestamp: [YYYY-MM-DD HH:MM]
Task-ID: [TASK-XXXX]
Budget: [$amount | N/A]
Logic: "Validated by [X9/Franklyn]; within $X daily burn."
Success_Criteria: "Explicit definition of 'Done'"
```

---

## 4. Spawn Patterns

### ⚠️ Known Limitation: Model Routing

**OpenClaw 2026.4.26 does NOT support per-agent model routing in subagent spawns.**

| Feature | Status | Detail |
|---------|--------|--------|
| Workspace isolation | ✅ Working | Each agent gets their own workspace directory |
| Role context from `.md` files | ✅ Working | `IDENTITY.md`, `SOUL.md` load correctly |
| `model` parameter in `sessions_spawn` | ⚠️ Accepted but ignored | Stored in session metadata, not applied to inference |
| True per-agent model routing | ❌ Not available | All subagents inherit parent model |

**Verified by Frank (CEO) on 2026-04-28:**
- Spawned RodZilla with `model="ollama/glm-5.1:cloud"`
- Session metadata showed `"model": "glm-5.1:cloud"`
- Runtime metadata confirmed actual model: `ollama/kimi-k2.6:cloud` (inherited from parent)

**Workaround:** Agents differentiate via workspace context and role definitions, not model. Model assignments in `openclaw.json` are forward-compatible.

---

### Pattern A: Direct Agent Spawn (Recommended)
Spawn into agent workspace for identity isolation. Model inheritance is a known limitation.

```bash
# Frank spawns RodZilla for engineering task
sessions_spawn(
  runtime="subagent",
  cwd="/Users/frankomatic5007/.openclaw/workspace/Rodzilla",
  task="ARP-4.0 PACKET\n# AGENT ACTION...",
  context="fork"  # Optional: inherit parent context
)
```

**Result:** RodZilla gets his workspace files (`IDENTITY.md`, `SOUL.md`) but runs on parent's model.

---

### Pattern B: Session Model Switching (Workaround)
Change parent model before spawning, then switch back after completion.

```bash
# Step 1: Switch Frank to X9's model
session_status(model="ollama/deepseek-v4-pro:cloud")

# Step 2: Spawn X9 (inherits deepseek-v4-pro)
sessions_spawn(
  runtime="subagent",
  cwd="/Users/frankomatic5007/.openclaw/workspace/X9",
  task="Security audit..."
)

# Step 3: Switch back to Frank's default model
session_status(model="ollama/kimi-k2.6:cloud")
```

**Caution:** Disrupts Frank's context. Use only for isolated security/fiduciary tasks.

---

### Pattern C: ACP Harness Routing (External Models)
Use ACP for external model providers (Claude, Gemini, etc.) with true model separation.

```bash
sessions_spawn(
  runtime="acp",
  agentId="claude",
  task="Security audit...",
  model="claude-3-7-sonnet"  # External model, enforced
)
```

**Limitation:** Only for external APIs. Ollama model switching not supported via ACP.

---

### Pattern D: Registry-Aware Spawn (Future)
Pending OpenClaw feature. Will use `openclaw.json` agent registry for automatic model routing.

```json
// In openclaw.json — already configured
{
  "id": "x9",
  "model": { "primary": "ollama/deepseek-v4-pro:cloud" }
}
```

**Status:** Agent registry populated. Awaiting OpenClaw runtime support.

---

### Pattern E: Karine's Fast Lane (Cultural Pre-Approval Routing)
For Aesthetic Soul tasks where Karine wants speed without CEO bottleneck.

**Flow:**
```
Karine asks Jarbas
    ↓
Jarbas validates cultural fit (Zosima Protocol)
    ↓
Jarbas sends ARP-4.0 TASK_BRIEF to Frank
    ↓
Frank auto-spawns specialist (no approval needed for Fast Lane)
    ↓
Specialist completes work, reports to Frank
    ↓
Frank notifies Jarbas/Karine
```

**Jarbas → Frank Routing Template:**
```markdown
# AGENT ACTION (ARP-4.0)
Type: TASK_BRIEF
From: jarbas
To: frank
Project: [brand]
Priority: [P1-P3]
Status: NEW
Task-ID: [TASK-XXXX]
Budget: <$20
Via: Karine Fast Lane
PreApproved: true

Request: Spawn [rodzilla|davinci|severino] for [task]
Cultural Check: ✅ Passed — aligns with Zosima Protocol
AutoApprove: Yes (within Fast Lane budget)
```

**Frank's Auto-Spawn Action:**
```bash
# Frank receives Fast Lane TASK_BRIEF from Jarbas
# No approval needed — cultural pre-check done by Jarbas
# Frank spawns immediately

sessions_spawn(
  runtime="subagent",
  cwd="/Users/frankomatic5007/.openclaw/workspace/DaVinci",
  task="Karine Fast Lane: [task description per Jarbas brief]"
)
```

**What Jarbas CAN Do Directly:**
- ✅ Cultural pre-approval (validates Zosima Protocol fit)
- ✅ Veto tasks that fail cultural check
- ✅ Draft creative briefs for specialists
- ✅ Review and soul-audit completed output

**What Requires Frank (CEO):**
- ❌ Direct agent spawn (OpenClaw blocks non-main agentId)
- ❌ Budget redistribution
- ❌ Cross-strategic-unit routing (Aesthetic Soul → Velocity Engine)

**Fallback if Frank Unavailable:**
1. Jarbas queues TASK_BRIEF
2. If no response in 10 minutes, auto-log to ByteRover
3. Frank reviews async and spawns retroactively
4. If URGENT: Jarbas escalates to direct WhatsApp to Rod

---

## 5. Message Types (ARP-4.0)

| Type | Purpose | Direction |
|------|---------|-----------|
| **TASK_BRIEF** | Assign work to specialist | Frank → Any |
| **COLLAB_REQUEST** | Cross-agent help request | Any → Any |
| **RESULT** | Completed task output | Specialist → Frank |
| **STATE_SUMMARY** | Project snapshot | Frank → All |
| **DECISION** | Recorded decision | Frank → All |
| **BLOCKER** | Cannot proceed | Any → Frank |
| **STATUS_UPDATE** | Progress update | Any → Frank |
| **DEPLOYMENT_REPORT** | Infra deploy report | RodZilla → Frank |
| **RESEARCH_BRIEF** | Research findings | Radar/Franklyn → Frank |
| **DESIGN_HANDOFF** | Design → Dev transfer | DaVinci → RodZilla |
| **FAMILY_TASK** | Family coordination | Jarbas → Severino |
| **SOUL_AUDIT** | Cultural veto/approval | Jarbas → DaVinci/Bob |
| **SHADOW_AUDIT** | Security scan report | X9 → RodZilla/Frank |
| **FIDUCIARY_ALERT** | Budget threshold warning | Franklyn → Frank |

---

## 6. The Sacred Three (Auto-Hold Rules)

Frank MUST stop and wait for explicit approval for:

1. **Soul Pivot** — Changes to Imigrou/Pernas Cruzadas core voice
2. **Big Spend** — Single cost or API credit spike > $500
3. **Public Face** — Major UI/UX changes to MyClipIQ/GMV homepages

---

## 7. Budget Guardrails

| Threshold | Trigger | Action |
|-----------|---------|--------|
| **$50** (50%) | Yellow Alert | Franklyn warns Boardroom; audit API calls |
| **$80** (80%) | Orange Alert | Disable high-cost models; revert to Gemma 4 |
| **$95** (95%) | Red Alert / Killswitch | HARD STOP all external API calls |

---

## 8. Karine's Fast Lane (v4.1 Appendix)

> **Important:** Due to OpenClaw 2026.4.26 limitation (`sessions_spawn` only supports `agentId="main"`), Jarbas **cannot directly spawn** other agents. The Fast Lane is implemented as **ARP routing through Frank** with cultural pre-approval.

### How It Actually Works

```
Karine asks Jarbas
    ↓
Jarbas validates cultural fit (Soul Audit)
    ↓
Jarbas sends ARP-4.0 TASK_BRIEF to Frank
    ↓
Frank spawns the specialist (no approval needed for Fast Lane tasks)
    ↓
Specialist completes work, reports to Frank
    ↓
Frank notifies Jarbas/Karine
```

### Fast Lane Routing Template

```markdown
# AGENT ACTION (ARP-4.0)
Type: TASK_BRIEF
From: jarbas
To: frank
Project: [brand]
Priority: [P1-P3]
Status: NEW
Task-ID: [TASK-XXXX]
Budget: <$20
Via: Karine Fast Lane
PreApproved: true

Request: Spawn [rodzilla|davinci|severino] for [task]
Cultural Check: ✅ Passed — aligns with Zosima Protocol
AutoApprove: Yes (within Fast Lane budget)
```

### Routing Rules

| Agent | Jarbas Routes To | Budget | Frank Action |
|-------|-----------------|--------|--------------|
| **RodZilla** | Frank → RodZilla | <$20 | Spawn immediately, no approval |
| **DaVinci** | Frank → DaVinci | <$10 | Spawn immediately, no approval |
| **Severino** | Frank → Severino | Any | Spawn immediately, no approval |

### What Jarbas CAN Do Directly

✅ **Cultural pre-approval** — Validates task fits Karine's voice
✅ **Veto** — Blocks tasks that fail Zosima Protocol
✅ **Draft specs** — Provides creative brief for specialist
✅ **Review output** — Soul audit on completed work

### What Requires Frank (CEO) Spawn

❌ **Direct agent spawn** — OpenClaw blocks non-main agentId
❌ **Budget redistribution** — Only Frank can move $ between agents
❌ **Cross-unit tasks** — Aesthetic Soul → Velocity Engine needs CEO routing

### Implementation Note

```python
# Jarbas sends to Frank (not direct spawn)
sessions_send(
  sessionKey="agent:main:discord:direct:1483206130426712115",
  message="ARP-4.0 TASK_BRIEF... Via: Karine Fast Lane"
)

# Frank spawns the specialist
sessions_spawn(
  runtime="subagent",
  task="Execute per Jarbas cultural brief..."
)
```

### Fallback: If Frank is Unavailable

1. Jarbas queues TASK_BRIEF for Frank
2. If no response in 10 minutes, auto-spawn (within budget)
3. Log to ByteRover for audit
4. Frank reviews async

---

## 9. ByteRover Integration

Every ARP-4.0 message MUST be logged to ByteRover context-tree:

```bash
# After completing task
brv curate "TASK-0042: RodZilla fixed export hang. PR #248 merged."
```

---

## 10. Example: Full Task Lifecycle

### Step 1: Frank assigns task
```markdown
# AGENT ACTION (ARP-4.0)
Type: TASK_BRIEF
From: frank
To: rodzilla
Project: myclipiq
Priority: P1
Status: NEW
Task-ID: TASK-0105
Budget: <$10
Logic: "Validated by X9; within daily burn."
Success_Criteria: "Export succeeds for 15min video"

Objective: Fix content pipeline export hang
```

### Step 2: RodZilla works (IN_PROGRESS)

### Step 3: X9 shadow audit (SHADOW_AUDIT)
```markdown
# AGENT ACTION (ARP-4.0)
Type: SHADOW_AUDIT
From: x9
To: rodzilla
Project: myclipiq
Status: READY
Task-ID: AUDIT-0105

Scan: No secrets detected. Diff approved.
```

### Step 4: RodZilla deploys (DEPLOYMENT_REPORT)

### Step 5: Franklyn verifies budget (FIDUCIARY_ALERT if needed)

---

## 11. Future State: True Model Routing

### When OpenClaw Supports Per-Agent Model Assignment

Once OpenClaw implements model enforcement in `sessions_spawn`, the agent registry (`openclaw.json`) will automatically route each agent to their assigned model.

**Required OpenClaw Feature:**
```json
// sessions_spawn parameter
{
  "agentId": "x9",
  "runtime": "subagent",
  "model": "auto" // Reads from agent registry
}
```

**Current Registry (Ready for Activation):**
| Agent | Model in Registry | Runtime Status |
|-------|-------------------|----------------|
| Frank | `kimi-k2.6:cloud` | ✅ Active (parent) |
| RodZilla | `glm-5.1:cloud` | ⏳ Awaiting OpenClaw |
| Jarbas | `kimi-k2.6:cloud` | ⏳ Awaiting OpenClaw |
| DaVinci | `qwen3-vl:235b-cloud` | ⏳ Awaiting OpenClaw |
| Franklyn | `kimi-k2.6:cloud` | ⏳ Awaiting OpenClaw |
| X9 | `deepseek-v4-pro:cloud` | ⏳ Awaiting OpenClaw |
| Radar | `minimax-m2.7:cloud` | ⏳ Awaiting OpenClaw |
| Bob | `glm-5.1:cloud` | ⏳ Awaiting OpenClaw |
| Severino | `minimax-m2.7:cloud` | ⏳ Awaiting OpenClaw |

**Detection:** Check `session_status` or spawn metadata for `"modelApplied": true` with correct model ID.

### Migration Path

When the feature drops:
1. No config changes needed — registry is already populated
2. Update ARP v4.0 Section 4 to mark Pattern D (Registry-Aware Spawn) as active
3. Deprecate Pattern B (Session Model Switching) and Pattern C (ACP Harness)
4. Resume per-agent budget tracking in Franklyn's reports

---

> *"Building a legacy of active love through autonomous intelligence. Secure by design, human by heart."*
