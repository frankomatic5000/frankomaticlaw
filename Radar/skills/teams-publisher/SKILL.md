# SKILL.md - teams-publisher

## Name
teams-publisher

## Description
Publish Radar reports to Microsoft Teams with proper formatting. Handles character limits by posting executive summaries with links to full reports.

## Teams Limits

| Limit | Value |
|-------|-------|
| Message text | ~4,000 chars |
| Adaptive Card | ~28,000 chars |
| File attachment | 50 MB |

## Strategy

### For Long Reports (>4,000 chars):
1. Generate **executive summary** (top 10 points)
2. Post summary to Teams
3. Include file path to full report
4. Karine accesses full report via workspace

### For Short Reports (<4,000 chars):
1. Post full content to Teams
2. No external file needed

## Format

### Executive Summary Template:
```
📊 [Report Title] — Resumo Executivo

🎯 TOP 10 AÇÕES:
1. [Action 1]
2. [Action 2]
...
10. [Action 10]

📁 Relatório completo:
[file path]

💡 Próximos passos:
[Next steps]
```

## Triggers

- "Post to Teams"
- "Send summary to Teams"
- "Publish report"

## Preferred Model

kimi-k2.5:cloud

---

*Teams-friendly report publishing.*
