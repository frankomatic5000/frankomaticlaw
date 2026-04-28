# SKILL.md - mail-mate

## Name
mail-mate

## Description
Email operations for GrowBiz Media. Handles the centralized inbox (frankomatic5007@gmail.com) where all business emails forward. Triages, drafts responses, and routes to appropriate agents (Frank for business, Jarbas for Karine's content).

## When to Use
- Processing forwarded emails from GoDaddy domains
- Triage: urgent vs. routine vs. spam
- Drafting responses for Rod/Karine approval
- Scheduling send times (not 2 AM)
- Following up on unanswered emails
- Newsletter/content ideas from incoming mail

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| action | enum | yes | triage, draft, send, schedule, followup, summarize |
| email_id | string | yes | Gmail message ID |
| priority | enum | no | urgent, normal, low (auto-detected) |
| draft_tone | enum | no | professional, friendly, brief, sales, karine-warm |
| requires_approval | boolean | no | true for sends (default: true) |

## Outputs
Triage classification + drafted response + next action

## Email Routing Logic

**Auto-Triage Rules:**

**URGENT (Notify immediately):**
- Client complaints
- Payment issues
- Legal/government correspondence
- Press inquiries
- Grant deadlines (NJEDA, IFundWomen)

**NORMAL (Process within 24h):**
- General inquiries
- Collaboration requests
- Vendor communications
- Scheduling

**LOW (Batch weekly):**
- Newsletters
- Marketing solicitations
- Spam (auto-filter)

**Routing:**

| Sender/Type | Route To | Action |
|-------------|----------|--------|
| Imigrou/Studios content | Jarbas → Karine | Flag for approval |
| GrowBiz Services leads | Frank → FrankCMO | Auto-draft response |
| DoodleType orders | Frank | Process or forward |
| Financial/taxes | Frank → FrankCFO | Secure handling |
| Legal/contracts | Frank | Hold for Rod review |
| Spam/junk | Auto-delete | Log only |

## Draft Templates

**Professional (GrowBiz Services):**
> "Hi [Name], Thanks for reaching out about [topic]. I'd love to learn more about your business needs. Can we schedule a brief call this week? — Rod, GrowBiz Media"

**Karine-Warm (Imigrou/Studios):**
> "Olá! Obrigada pelo contato sobre [topic]. Vamos conversar mais sobre isso? — Karine"

**Brief (Routine):**
> "Got it. I'll handle this by [date]. — Rod"

## Access Control
- **Frank:** Full access (triage, draft, send with approval)
- **Jarbas:** Read-only Karine's emails, draft for her approval
- **FrankCMO:** Access to marketing/sales emails
- **FrankCFO:** Access to finance emails

## Security
- Gmail OAuth2 (not password)
- IMAP access only (no SMTP sends without approval)
- Log all access to memory/audit
- PII redaction in logs

## Triggers
- "email"
- "inbox"
- "gmail"
- "forwarded email"
- "new message"

## Permissions
- gmail_api_read
- gmail_api_draft
- memory_read
- memory_write

## Preferred Model
kimi-k2.5:cloud

## Example Flow

1. Email arrives at frankomatic5007@gmail.com
2. Mail-mate triages: "Collaboration request for Imigrou"
3. Routes to Jarbas (Karine's content)
4. Jarbas drafts response in Portuguese
5. Flags for Karine approval
6. Karine approves via WhatsApp voice
7. Jarbas sends via Gmail

## Cron Monitoring
- Check inbox every 30 minutes (9 AM - 6 PM)
- Alert Frank on URGENT items
- Daily digest: "You have 5 emails pending"

## Connection Details
- **Inbox:** frankomatic5007@gmail.com
- **Protocol:** Gmail IMAP + OAuth2
- **Scope:** Read, draft, label (no auto-send)
- **Setup:** Requires Rod to authorize via Google OAuth

## Next Steps
1. Rod authorizes Gmail OAuth for mail-mate
2. Set up GoDaddy forwarding (all domains → frankomatic5007@gmail.com)
3. Test with 1-2 emails
4. Enable full processing
