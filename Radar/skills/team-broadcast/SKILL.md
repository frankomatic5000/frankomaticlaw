# SKILL.md - team-broadcast

## Name
team-broadcast

## Description
Send formatted alerts and updates to the GrowBiz Media team via Microsoft Teams webhook. Radar's primary output channel for research findings and early warnings.

## Webhook Configuration

**Teams Webhook URL:** (configured in Radar's TOOLS.md)
**Channel:** #general or #alerts (team's choice)
**Format:** Adaptive Cards (rich text, buttons)

## Message Types

### 1. 🚨 ALERT — Immediate Attention
```
🚨 RADAR ALERT — [Date]

[Critical information]
ACTION: [What to do]
```

### 2. 📊 UPDATE — Informational
```
📊 RADAR UPDATE — [Date]

[Market moves, trends, findings]
```

### 3. 🔍 RESEARCH — Deep Dive Complete
```
🔍 RADAR RESEARCH — [Topic]

EXECUTIVE SUMMARY
[1-2 sentences]

KEY FINDINGS
• [Point 1]
• [Point 2]

IMPLICATIONS
[What this means for GrowBiz]

FULL REPORT: [Link if applicable]
```

### 4. ✅ DAILY BRIEF — Morning Summary
```
🌅 DAILY BRIEF — [Date]

MARKETS: [S&P, oil, rates]
NEWS: [Key headlines]
THREATS: [Watch items]
OPPORTUNITIES: [Wins to chase]

PRIORITY: [Top 1-2 actions]
```

## Broadcast Rules

1. **Keep it short** — No walls of text
2. **Lead with action** — What to do, not just what happened
3. **Context matters** — Why this matters to GrowBiz
4. **No noise** — Skip unless actionable

## Color Coding

- 🟢 **Green** — Opportunity, positive
- 🟡 **Yellow** — Watch, monitor
- 🔴 **Red** — Alert, immediate action
- ⚪ **White/Gray** — Informational

## Examples

**Market Alert:**
```
🚨 RADAR ALERT — March 23, 2026

Oil +4% on Hormuz tension
→ Check shipping costs if importing
→ Monitor for 48hr resolution

ACTION: No change yet, watch Tuesday
```

**Research Complete:**
```
🔍 RADAR RESEARCH — Hermes Agent

CONFIRMED: Nous Research project
REAL: 10K+ GitHub stars
DIFFERENCE: Auto-skill generation, self-improvement

IMPLICATION: Interesting, but OpenClaw more mature
for multi-agent setups

ACTION: Monitor, no migration needed
```

## Triggers

- Scheduled (daily 7 AM)
- Event-driven (threshold breach)
- Manual (Frank/Radar decides)

## Permissions

- teams_webhook (POST to Teams)
- web_search (context gathering)

## Preferred Model

kimi-k2.5:cloud

---

*Radar's voice to the team.*
