---
name: finance-core
description: Core financial operations for FrankCFO — MRR, grants, forecasting, equipment tracking
metadata:
  {
    "openclaw":
      {
        "emoji": "💵",
        "requires": { "tools": ["read", "write", "exec"], "skills": ["quickbooks"] },
        "primaryEnv": null
      }
  }
---

# finance-core

Financial operations hub for GrowBiz Media. MRR tracking, grants, forecasting, and equipment registry.

## When to Use

- Check MRR and churn
- Update financial forecast
- Track grant applications
- Log equipment purchases
- Run P&L analysis

## When NOT to Use

- QuickBooks operations (use quickbooks skill)
- Family budget (use Severino's family-ops)
- Expense reimbursement (use expense-tracker)

## MRR Tracking

**GrowBiz Services Tiers:**
- $297/month — Local SEO Basic
- $497/month — Local SEO Pro
- $997/month — Full Service

**Metrics:**
- Total MRR: Sum of active subscriptions
- Churn rate: Canceled / Total (monthly)
- LTV: Average revenue per customer × lifespan
- CAC: Customer acquisition cost

**Dashboard:**
```
MRR: $X,XXX
Active clients: XX
Churn (30d): X%
Runway: XX months
```

## Grant Lifecycle

**Active Grants:**
- NJEDA Small Business Improvement Grant
- IFundWomen General Grant

**Status Tracking:**
- Applied → Under Review → Decision → Funded/Declined
- Due dates
- Reporting requirements
- Fund utilization

**Narrative Generation:**
- Immigrant founder story
- Community impact
- Equipment investment justification
- Revenue projections

**Approval Required:** Rod on ALL grant submissions

## Financial Forecasting

**Honest Projections:**
- Conservative (70% confidence)
- Base (50% confidence)
- Optimistic (30% confidence)

**Scenarios:**
- Pre-revenue products (ClipIQ, Vaptlux)
- Services MRR growth
- Imigrou monetization timeline
- Studio equipment ROI

**Outputs:**
- Monthly burn rate
- Runway (cash ÷ burn)
- Decision points ("If X doesn't happen by Y, we Z")

## Equipment Registry

**Tracked Assets:**
- Sony FX3 (anchor asset)
- Lenses, lighting, audio
- Computers, drives
- Software licenses

**Per Asset:**
- Purchase date
- Cost
- Depreciation schedule
- Grant attribution
- Insurance coverage
- Current value

**Example:**
```
Sony FX3
- Purchased: 2025-11-15
- Cost: $3,898
- Grant: NJEDA (partial)
- Depreciation: 20% / year
- Current value: $3,118
- Insurance: $4,000 replacement
```

## Tax Calendar

**Automatic Reminders:**
- Quarterly estimated taxes (15th of Jan, Apr, Jun, Sep)
- Annual filing prep (Feb 1)
- 1099 issuance (Jan 31)
- Sales tax (monthly if applicable)

**Integration:** QuickBooks tax reports

## Reporting

**Weekly (Monday 9am):**
- MRR movement
- New/expired clients
- Grant status updates
- Upcoming tax deadlines

**Monthly:**
- Full P&L
- Cash flow statement
- Balance sheet
- Forecast vs actual

**Quarterly:**
- Strategic review
- Budget reallocation
- Scenario planning

## Tool Usage

```javascript
// Query QuickBooks
const qb = await skills.quickbooks.query('SELECT * FROM Invoice WHERE TxnDate >= 2026-01-01');

// Update forecast
await tools.write('~/.openclaw/workspace-frankcfo/forecast/2026-Q1.md', forecast);

// Log equipment
await tools.exec({ command: 'sqlite3 equipment.db "INSERT INTO assets ..."' });
```

## Files

- MRR: `~/.openclaw/workspace-frankcfo/mrr/`
- Grants: `~/.openclaw/workspace-frankcfo/grants/`
- Forecasts: `~/.openclaw/workspace-frankcfo/forecast/`
- Equipment: `~/.openclaw/workspace-frankcfo/equipment.db`

## Security

- Financial data encrypted at rest
- QuickBooks OAuth in agent auth-profiles
- No plaintext account numbers in logs
- FrankCFO only (no Jarbas access)

## ARP Integration

Called by Frank for finance tasks:
```javascript
await tools.sessions_spawn({
  agentId: 'frankcfo',
  task: 'Update Q1 forecast',
  model: 'ollama/kimi-k2.5:cloud' // or deepseek-chat for narrative
});
```

Returns structured financial data for Frank to present to Rod.
