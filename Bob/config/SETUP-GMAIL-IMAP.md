# Bob's Gmail IMAP Setup (Option C)

## Architecture

```
Mac Mini (Local)
    ↓
Python IMAP script runs every 15 min via cron
    ↓
Connects to Gmail IMAP (frankomatic5007@gmail.com)
    ↓
Classifies emails (URGENT/SALES/CONTENT/FINANCIAL/LEGAL)
    ↓
Sends WhatsApp via OpenClaw CLI
    ↓
Rod (+19082581356) or Karine (+18622520852) gets notification
```

## Setup Steps

### 1. Generate Gmail App Password

1. Go to https://myaccount.google.com/apppasswords
2. Sign in with frankomatic5007@gmail.com
3. Select "Mail" → "Mac" (or "Other")
4. Copy the 16-character password

### 2. Store Password Securely

```bash
# Add to ~/.zshrc or ~/.bash_profile
export GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"

# Reload
source ~/.zshrc
```

### 3. Test the Script

```bash
# Run manually
python3 ~/.openclaw/workspace/Bob/scripts/gmail-imap-monitor.py
```

Expected output:
```
🔌 Connecting to imap.gmail.com...
📧 Found 3 unread emails
📨 [URGENT] [SALES] Partnership proposal...
✅ WhatsApp sent to +19082581356
✅ Processed 1 important emails
```

### 4. Set Up Cron (Every 15 Minutes)

```bash
# Edit crontab
crontab -e

# Add this line:
*/15 * * * * cd ~/.openclaw/workspace/Bob/scripts && /usr/bin/python3 gmail-imap-monitor.py >> /tmp/gmail-monitor.log 2>&1

# For daily digest at 9 AM:
0 9 * * * cd ~/.openclaw/workspace/Bob/scripts && /usr/bin/python3 gmail-imap-monitor.py --digest >> /tmp/gmail-monitor.log 2>&1
```

### 5. Verify Cron is Running

```bash
# Check crontab
crontab -l

# Check logs
tail -f /tmp/gmail-monitor.log
```

## WhatsApp Response Commands

When Rod/Karine receive alerts, they reply in WhatsApp:

| Reply | Action |
|-------|--------|
| **CHECK** | Bob reviews email and drafts response |
| **APPROVE** | Send Bob's draft |
| **EDIT** | Modify Bob's draft |
| **IGNORE** | No action needed |
| **URGENT** | Escalate to Frank (CEO) |
| **REPORT** | Send daily digest |

## Classification Rules

| Type | Keywords | Priority |
|------|----------|----------|
| **URGENT** | complaint, urgent, asap, cancel, reclamação, payment issue, legal, lawsuit | Immediate |
| **SALES** | proposal, quote, pricing, demo, partnership, orçamento, proposta | P1 |
| **CONTENT** | imigrou, content, karine, video, estudio, youtube, tiktok | Normal |
| **FINANCIAL** | invoice, payment, tax, fatura, billing, subscription | P1 |
| **LEGAL** | contract, legal, agreement, terms, gdpr, privacy | P1 |

## Troubleshooting

### "GMAIL_APP_PASSWORD not set"
```bash
export GMAIL_APP_PASSWORD="your-password"
echo $GMAIL_APP_PASSWORD  # Should show password
```

### "Connection refused"
- Check internet connection
- Verify Gmail IMAP is enabled: https://mail.google.com → Settings → Forwarding and POP/IMAP

### "Login failed"
- App Password is required (not regular password)
- 2FA must be enabled on Google account
- Generate new App Password if needed

### "WhatsApp not sent"
- Check OpenClaw WhatsApp is configured: `openclaw status`
- Verify phone numbers in allowlist
- Check OpenClaw gateway is running

## Files

| File | Purpose |
|------|---------|
| `Bob/scripts/gmail-imap-monitor.py` | Main IMAP monitor script |
| `Bob/data/email-state.json` | Tracks processed email IDs |
| `Bob/config/SETUP-GMAIL-IMAP.md` | This file |
| `/tmp/gmail-monitor.log` | Execution logs |

## Security Notes
- App Password stored in environment variable (not in code)
- No credentials in git
- State file is local only
- All WhatsApp via existing OpenClaw auth
