# SKILL.md - manus-research

## Name
manus-research

## Description
Deep research via Manus AI API using custom async handler. Unlike standard OpenClaw model calls, Manus requires async polling (24-48 hour typical turnaround).

## API Configuration

**Endpoint:** `https://api.manus.im/v1`  
**Auth:** `API_KEY` header (not Bearer)  
**Method:** Async task creation + polling  
**SDK:** OpenAI Python SDK 1.100.2+

## Usage

### For Radar Agent:

Radar calls this skill which executes:
```bash
/Users/frankomatic007/.openclaw/workspace-radar/scripts/submit_manus_task.sh "research query"
```

The script:
1. Submits task to Manus API
2. Polls for completion (every 60 seconds)
3. Posts results to Teams webhook
4. Saves results locally

### Expected Runtime:

| Task Complexity | Time |
|----------------|------|
| Simple | 5-15 min |
| Medium | 30-60 min |
| Deep research | 2-24 hours |
| Complex multi-step | 24-48 hours |

## Workflow

1. **Spawn Radar** with research query
2. **Radar executes** `submit_manus_task.sh`
3. **Background process** runs and polls Manus
4. **Results posted** to Teams when complete
5. **Radar confirms** task submitted (not waiting)

## Triggers

- "Research [topic] using Manus"
- "Deep analysis of [subject]"
- "Manus investigation into [area]"

## Output

- **Immediate:** Task submitted confirmation
- **Async (hours later):** Full research report posted to Teams

## Files

- `scripts/manus_research.py` - Python handler
- `scripts/submit_manus_task.sh` - Submission wrapper
- `logs/` - Execution logs
- `manus_results_*.json` - Saved results

## Environment Variables

```bash
MANUS_API_KEY="sk-..."
TEAMS_WEBHOOK_URL="https://imigrou.webhook.office.com/..."
```

## Notes

- Task runs in background (daemon)
- Results delivered async to Teams
- Radar does not wait for completion
- Check Manus dashboard for live progress

## Preferred Model

Uses Manus API directly (not OpenClaw routing)

---

*True async deep research when you need comprehensive analysis.*
