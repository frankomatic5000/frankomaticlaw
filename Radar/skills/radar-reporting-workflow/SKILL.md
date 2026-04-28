# SKILL.md - radar-reporting-workflow

## Name
radar-reporting-workflow

## Description
Automated end-to-end reporting workflow: Radar analyzes Instagram → generates reports → spawns FrankCMO for marketing strategy → posts complete action plan to Teams.

## Workflow Steps

### Bi-Weekly (Every 14 Days)

**Step 1: Radar Analysis**
- Analyze @imigrou changes since last report
- Track follower growth/decline
- Calculate engagement trends
- Identify top performing content
- Compare to previous period

**Step 2: Radar Report Generation**
- Create executive summary (Portuguese)
- Highlight key changes
- Generate action items
- Save report locally

**Step 3: Spawn FrankCMO**
- Send Radar report to FrankCMO
- Request marketing action plan
- Specify immediate priorities
- Set growth targets

**Step 4: FrankCMO Analysis**
- Review Radar findings
- Create marketing strategy
- Define Karine's tasks
- Define team tasks
- Set 7/30/90 day roadmap

**Step 5: Radar Teams Post**
- Compile executive summary
- List action items by person
- Post to Teams webhook
- Include links to full reports

### Monthly (1st of Month)

**Step 1: Radar Deep Research (Manus)**
- Full Instagram analysis
- SEO strategy research
- Competitor deep dive
- Trend identification

**Step 2: Radar Report Generation**
- Instagram analysis report
- SEO strategy report
- Save both locally

**Step 3: Spawn FrankCMO**
- Send both Radar reports
- Request comprehensive marketing plan
- Include content calendar
- Define KPIs

**Step 4: FrankCMO Strategy**
- 30-day content calendar
- Marketing action plan
- Team responsibilities
- Growth roadmap

**Step 5: Radar Teams Post**
- Complete summary
- All action items
- Links to 3 full reports
- Confirmation of delivery

## Triggers

- Cron: Bi-weekly (14 days)
- Cron: Monthly (1st of month)
- Manual: "Run bi-weekly report for @[handle]"
- Manual: "Run monthly deep report for @[handle]"

## Output Files

**Bi-Weekly:**
- `report_[handle]_biweekly_PT.md`
- `frankcmo_action_plan_[handle]_PT.md`

**Monthly:**
- `report_[handle]_PT.md`
- `report_[handle]_SEO_PT.md`
- `frankcmo_marketing_plan_[handle]_PT.md`

## Teams Delivery

**Bi-Weekly Post Includes:**
- Executive summary
- Key changes since last report
- Top 5 action items
- Person-specific tasks

**Monthly Post Includes:**
- Complete executive summary
- Full action plan
- 30-day content calendar preview
- All report links
- KPIs to track

## Future Expansion

### Channels to Add

1. **@pernascruzadastalks** — Talk show format
2. **@growbizmagazine** — Digital publication
3. **@pessoasglobais** — Community stories
4. **@growbiztalks** — Business interviews

### Adding New Channel

1. Duplicate workflow with new handle
2. Adjust metrics for channel type
3. Add to cron schedule
4. Update documentation

## Agent Coordination

| Agent | Role |
|-------|------|
| Radar | Analysis, research, Teams posting |
| FrankCMO | Marketing strategy, action plans |

## Handoff Protocol

**Radar → FrankCMO:**
```
AGENT MESSAGE
Protocol: ARP-2.0
Type: TASK_BRIEF
From: radar
To: frankcmo
Project: [handle]
Reports: [file paths]
Deliverable: Marketing action plan
```

**FrankCMO → Radar:**
- Saves marketing plan
- Returns confirmation
- Radar posts to Teams

## Error Handling

- **Manus timeout:** Retry with simplified query
- **FrankCMO fail:** Radar posts analysis only
- **Teams fail:** Save locally, retry later
- **File save fail:** Log error, continue

---

*Complete automated reporting with marketing intelligence.*
