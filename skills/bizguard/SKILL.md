# SKILL.md - BizGuard

## Name
bizguard

## Description
Financial operations for GrowBiz Media portfolio. Tracks revenue across GrowBiz Services (recurring), Studios (project), and future product income (ClipIQ, Vaptlux). Manages grant applications (NJEDA, IFundWomen), equipment tracking, and tax compliance. The skill that keeps Rod and Karine's empire financially sound.

## When to Use
- Dashboard summaries (QuickBooks)
- Creating invoices (requires approval)
- Logging expenses (requires approval, $500 cap for Jarbas)
- Tracking grant applications
- Applying for grants (Rod only)
- Tax reminders
- Financial reports
- Revenue forecasting
- Reconciling accounts (Rod only)
- Client revenue reports
- Equipment tracking

## Inputs
| Name | Type | Required | Options |
|------|------|----------|---------|
| action | enum | yes | dashboard, invoice, expense, grant_track, grant_apply, tax_remind, report, forecast, reconcile, client_revenue, equipment_track |
| brand | enum | no | growbiz-media, growbiz-services, growbiz-studios, imigrou, clipiq, vaptlux, doodletype, zecaos, all (default: all) |
| period | enum | no | today, this_week, this_month, this_quarter, this_year, custom (default: this_month) |
| custom_range | object | no | {start: date, end: date} |
| grant_id | string | no | - |
| client_id | string | no | - |
| amount | number | no | - |
| description | string | no | - |

## Outputs
Result with: action_completed, dashboard_summary, grant_status, tax_reminders, report_data, forecast, client_mrr, equipment_registry, approval_status

## Active Grants to Track
- NJEDA Small Business Improvement Grant (Studios equipment)
- IFundWomen (production capacity)

## Access Control
- **Frank:** All actions
- **Jarbas:** dashboard, invoice, expense, grant_track, tax_remind, report, client_revenue, equipment_track
- **Jarbas blocked:** grant_apply, reconcile, forecast
- **Jarbas approval cap:** $500

## Triggers
- "quickbooks"
- "invoice"
- "grant"
- "revenue"
- "MRR"
- "expense"
- "tax"
- "equipment"
- "client revenue"

## Permissions
- quickbooks_api_read
- quickbooks_api_write
- memory_read
- memory_write

## Preferred Model
qwen3.5:cloud
## Escalation Model
deepseek-chat (for grant_apply, report, reconcile)
## Reasoning Model
deepseek-reasoner (for forecast)
