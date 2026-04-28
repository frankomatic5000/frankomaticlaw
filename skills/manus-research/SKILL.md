# SKILL.md - manus-research

## Name
manus-research

## Description
Deep research automation via Manus.ai API for FrankCMO. Handles long-running Instagram and social media research tasks that require 10-30 minutes of autonomous analysis. Spawns Manus agents, monitors progress, and returns actionable reports for marketing strategy implementation.

## Integration
**External Service:** Manus.ai (https://manus.im)  
**API Type:** OpenAI-compatible (OpenAI Responses API)  
**Base URL:** https://api.manus.im  
**Auth:** API_KEY header (to be configured)

## When to Use
- Competitive Instagram account analysis (deep dive)
- Hashtag research and trend identification
- Content strategy research (what's working in niche)
- Market research for new brand opportunities
- Multi-step automation workflows
- Reports requiring web browsing and data synthesis

## When NOT to Use
- Quick lookups (use web-search instead)
- Real-time chat (Manus is async)
- Simple tasks (overkill)
- Tasks requiring immediate response

## Configuration

### Required Setup
```json
{
  "manus_api_key": "YOUR_MANUS_API_KEY_HERE",
  "manus_base_url": "https://api.manus.im",
  "default_agent_profile": "manus-1.6",
  "webhook_url": "https://your-webhook.com/manus-results"
}
```

### How to Get API Key
1. Sign up at https://manus.im
2. Go to Settings → Integrations → API
3. Generate API key
4. Add to skill config (below)

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| task_type | enum | yes | competitor_analysis, hashtag_research, content_strategy, trend_analysis, custom |
| target_accounts | array | no | Instagram handles to analyze (for competitor analysis) |
| research_topic | string | yes | What to research |
| depth | enum | no | quick (10min), standard (20min), deep (30min) |
| deliverable | enum | no | report, spreadsheet, content_calendar, custom |
| callback_agent | enum | yes | frankcmo, socialclaw, frank |

## Outputs
Manus returns complete deliverables:
- Structured reports (markdown)
- Data tables
- Actionable recommendations
- Source citations
- Next steps

## Workflow

### 1. Task Spawn
```
FrankCMO identifies need → manus-research spawns task → 
Manus API accepts → Returns task_id → 
Skill monitors status (running/pending/completed)
```

### 2. Manus Execution (10-30 min)
```
Manus agent:
- Browses web
- Analyzes Instagram accounts
- Researches trends
- Synthesizes findings
- Generates report
```

### 3. Result Delivery
```
Manus completes → Webhook triggers → 
Skill processes → Routes to callback_agent → 
Agent implements findings
```

## Example Tasks

### Task: Competitor Analysis
```json
{
  "task_type": "competitor_analysis",
  "target_accounts": ["@contabrasil", "@brasileiraspelomundo"],
  "research_topic": "What content formats get highest engagement for Brazilian creators in US?",
  "depth": "deep",
  "deliverable": "report",
  "callback_agent": "frankcmo"
}
```

### Task: Hashtag Research
```json
{
  "task_type": "hashtag_research",
  "research_topic": "Best performing hashtags for Brazilian immigrant content in 2026",
  "depth": "standard",
  "deliverable": "spreadsheet",
  "callback_agent": "socialclaw"
}
```

### Task: Content Strategy
```json
{
  "task_type": "content_strategy",
  "research_topic": "What topics are trending for diaspora communities this month?",
  "depth": "quick",
  "deliverable": "content_calendar",
  "callback_agent": "frankcmo"
}
```

## Polling Strategy
- Check status every 2 minutes
- Timeout: 45 minutes (max)
- Retry failed tasks: 2x
- Store results in: memory/manus-research/

## Error Handling
- **Task fails:** Log error, notify Frank
- **Timeout:** Mark as failed, partial results if any
- **API errors:** Retry with backoff
- **Webhook fails:** Queue for manual pickup

## Access Control
- **FrankCMO:** Primary user (spawns tasks)
- **SocialClaw:** Can spawn for content research
- **Frank:** Can spawn any research task
- **Manus API key:** Stored in secure credentials

## Model Configuration
Manus profiles:
- `manus-1.6-lite`: Quick tasks (10 min, cheaper)
- `manus-1.6`: Standard (20 min, balanced) ← DEFAULT
- `manus-1.6-max`: Deep analysis (30 min, most thorough)

## Cost Tracking
- Track per-task cost
- Report to budget-watch skill
- Alert if monthly spend >$50

## Triggers
- "research instagram accounts"
- "analyze competitors"
- "deep dive on [topic]"
- "manus research"
- "trend analysis"

## Permissions
- web_search (for Manus context)
- memory_read/write
- file_write (store reports)
- manus_api_access

## Notes
- Manus tasks run asynchronously (don't block)
- Results typically ready in 10-30 minutes
- Reports are comprehensive, not bullet points
- Designed for strategic decisions, not tactical

## Future Enhancements
- Auto-spawn weekly competitor reports
- Schedule recurring trend analysis
- Integrate with SocialClaw for auto-scheduling
- Connect to Imigrou analytics for data-driven research

---

## Setup Checklist

- [ ] Create Manus account at https://manus.im
- [ ] Generate API key
- [ ] Add API key to skill config
- [ ] Configure webhook endpoint
- [ ] Test with simple task
- [ ] Document first successful task

**API Key Status:** ⏳ PENDING (waiting for Rod to create Manus profile)
