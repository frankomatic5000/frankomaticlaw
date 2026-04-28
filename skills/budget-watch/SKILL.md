---
name: budget-watch
description: Per-agent budget tracking for GrowBiz Media — $100/month cap, alerts at $50, weekly reports
metadata:
  {
    "openclaw":
      {
        "emoji": "💰",
        "requires": { "tools": ["read", "write", "sessions_send", "cron"] },
        "primaryEnv": null
      }
  }
---

# budget-watch

Budget enforcement and tracking for the 6-agent GrowBiz Media system. Monitors per-agent spend, alerts at thresholds, and provides weekly reports.

## Budget Structure

| Agent | Monthly Cap | Alert At (80%) | Model Tier |
|-------|-------------|----------------|------------|
| frank | $4 | $3.20 | 1 (kimi) |
| jarbas | $4 | $3.20 | 1 (kimi) |
| rodzilla | $14 | $11.20 | 2 (deepseek) |
| frankcmo | $9 | $7.20 | 1+2 (kimi+qwen) |
| frankcfo | $8 | $6.40 | 1+2 (kimi+deepseek) |
| severino | $6 | $4.80 | 1+2 (kimi+qwen) |
| **TOTAL** | **$45** | **—** | **$55 buffer** |

System thresholds:
- **Alert**: $50 (warn Rod, continue carefully)
- **Hard Stop**: $100 (refuse new tasks, manual approval required)

## When to Use

- Before spawning any specialist (check remaining budget)
- When receiving Return Envelope (update spent amount)
- Weekly Monday 9am for executive briefing
- When Rod asks "what's our spend?"

## When NOT to Use

- Don't use to enforce hard stop at OpenClaw level (not possible)
- Don't use for real-time billing (OpenClaw doesn't expose this)
- Don't use for per-request cost prediction (too variable)

## State File

```json
{
  "month": "2026-03",
  "agents": {
    "frank": { "spent": 0.00, "cap": 4.00 },
    "jarbas": { "spent": 0.00, "cap": 4.00 },
    "rodzilla": { "spent": 0.00, "cap": 14.00 },
    "frankcmo": { "spent": 0.00, "cap": 9.00 },
    "frankcfo": { "spent": 0.00, "cap": 8.00 },
    "severino": { "spent": 0.00, "cap": 6.00 }
  },
  "totalSpent": 0.00,
  "totalCap": 100.00,
  "lastUpdated": "2026-03-20T13:30:00Z"
}
```

Location: `~/.openclaw/workspace/budget/budget-state.json`

## Usage

### Check Budget Before Spawn

```
Check budget for rodzilla before spawning. Can we proceed with deepseek-r1?
```

Returns:
- ✅ Proceed: "$11.20 remaining, OK to spawn"
- ⚠️ Warning: "$2.50 remaining, advise kimi instead"
- ❌ Hard stop: "$0 remaining, escalate to Rod"

### Update After Task

```
Update budget: rodzilla spent $2.50 on TASK-0001
```

Reads Return Envelope, updates state file.

### Weekly Report (Cron)

Runs every Monday 9am EST:

```
Weekly budget report for Rod:

March 17-23, 2026
================
Total Spent: $23.45 / $100.00 (23%)

Per-Agent:
- frank: $2.10 / $4.00 (53%)
- jarbas: $1.50 / $4.00 (38%)
- rodzilla: $8.20 / $14.00 (59%) ⚠️
- frankcmo: $5.65 / $9.00 (63%)
- frankcfo: $3.00 / $8.00 (38%)
- severino: $3.00 / $6.00 (50%)

Projected month-end: $94.20 (under cap)

⚠️ rodzilla at 80% threshold
```

### Manual Query

```
What's our budget status?
```

## Model Cost Reference

From openclaw.json (per 1K tokens):

| Model | Input | Output | Cache |
|-------|-------|--------|-------|
| kimi-k2.5:cloud | $0.00 | $0.00 | $0.00 |
| deepseek-chat-v3 | $0.07 | $0.28 | $0.014 |
| deepseek-r1 | $0.55 | $2.19 | $0.11 |

**kimi-k2.5:cloud is FREE** (local Ollama with cloud routing).

**Implication**: Most agents cost nothing. Only DeepSeek models cost money.

## Tracking Method

Since OpenClaw doesn't expose real-time cost:

1. **Estimated from Return Envelope TOKENS field**
   - Input tokens: ~500 per request
   - Output tokens: varies by task
   - Model: from spawn params

2. **Formula**:
   ```
   cost = (input_tokens / 1000 * input_rate) + (output_tokens / 1000 * output_rate)
   ```

3. **Actual cost may differ** — this is approximation.

## Enforcement Strategy

| Threshold | Action |
|-----------|--------|
| 80% of agent cap | Warn, suggest cheaper model |
| 100% of agent cap | Refuse spawn, escalate to Rod |
| $50 system-wide | Warn Rod, continue with caution |
| $100 system-wide | Hard stop all non-essential tasks |

**Important**: Enforcement is advisory. Actual OpenClaw calls aren't blocked — this skill tracks and warns.

## Cron Schedule

```json
{
  "cron": {
    "weekly-budget-report": {
      "schedule": "0 9 * * 1",
      "command": "budget-watch weekly-report"
    }
  }
}
```

## Files

- State: `~/.openclaw/workspace/budget/budget-state.json`
- History: `~/.openclaw/workspace/budget/history/YYYY-MM.json`
- Reports: `~/.openclaw/workspace/budget/reports/`

## Integration

Called by `arp-router` before every spawn:

```javascript
// In arp-router
const budget = await readBudgetState();
if (budget.agents[agentId].remaining < estimate) {
  // Warn or escalate
}
```
