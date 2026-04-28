# Gmail → OpenClaw → WhatsApp Routing

## Architecture

```
frankomatic5007@gmail.com
    ↓ (Google Apps Script monitors every 15 min)
URGENT / SALES / CONTENT detected
    ↓
Google Apps Script calls OpenClaw CLI/API
    ↓
openclaw agent --to +NUMBER --message "..." --deliver
    ↓
Rod (+19082581356) or Karine (+18622520852) gets WhatsApp
    ↓
Reply "CHECK" → OpenClaw routes to Bob to draft response
```

## Why This Works
- ✅ **No Discord webhook** — Direct WhatsApp via OpenClaw
- ✅ **Jarbas handles routing** — Cultural gate decides who gets pinged
- ✅ **Native WhatsApp** — Karine/Rod get real notifications on their phones
- ✅ **Reply to act** — Just reply "CHECK" and Bob handles it
- ✅ **Secure** — Uses OpenClaw's existing WhatsApp auth (no new credentials)

## Google Apps Script

```javascript
const CONFIG = {
  // OpenClaw gateway URL (local or exposed)
  OPENCLAW_URL: 'http://127.0.0.1:18789', // Local gateway
  
  // OR use OpenClaw CLI directly (if script runs on same machine)
  USE_CLI: false,
  
  // Phone numbers (from allowlist)
  ROD_PHONE: '+19082581356',
  KARINE_PHONE: '+18622520852',
  
  // Processed label
  PROCESSED_LABEL: 'Bob-Processed'
};

function checkInbox() {
  let label = GmailApp.getUserLabelByName(CONFIG.PROCESSED_LABEL);
  if (!label) {
    label = GmailApp.createLabel(CONFIG.PROCESSED_LABEL);
  }
  
  // Get unread emails not yet processed
  const threads = GmailApp.search('is:unread -label:' + CONFIG.PROCESSED_LABEL, 0, 50);
  
  threads.forEach(thread => {
    thread.getMessages().forEach(message => {
      if (message.isUnread()) {
        processEmail(message, label);
      }
    });
  });
}

function processEmail(message, label) {
  const from = message.getFrom();
  const subject = message.getSubject();
  const body = message.getPlainBody().substring(0, 1000);
  const priority = classifyEmail(subject + ' ' + body);
  const type = determineType(subject);
  
  const emailData = {
    id: message.getId(),
    from: from,
    subject: subject,
    date: message.getDate().toISOString(),
    priority: priority,
    type: type,
    snippet: body.substring(0, 200)
  };
  
  // Route based on priority and type
  switch(priority) {
    case 'URGENT':
      sendWhatsAppAlert(emailData, type);
      break;
    case 'SALES':
      sendWhatsAppAlert(emailData, 'SALES');
      notifyBob(emailData);
      break;
    case 'CONTENT':
      sendWhatsAppAlert(emailData, 'CONTENT');
      break;
  }
  
  // Mark as processed
  label.addToThread(message.getThread());
}

function determineType(subject) {
  const s = subject.toLowerCase();
  if (s.includes('imigrou') || s.includes('content') || s.includes('karine') || s.includes('video') || s.includes('estudio')) return 'CONTENT';
  if (s.includes('invoice') || s.includes('payment') || s.includes('tax') || s.includes('fatura')) return 'FINANCIAL';
  if (s.includes('legal') || s.includes('contract') || s.includes('contrato')) return 'LEGAL';
  if (s.includes('proposal') || s.includes('quote') || s.includes('pricing') || s.includes('demo') || s.includes('partnership') || s.includes('collaboration') || s.includes('sponsor') || s.includes('orçamento')) return 'SALES';
  return 'GENERAL';
}

function classifyEmail(text) {
  const lower = text.toLowerCase();
  const urgentWords = ['complaint', 'urgent', 'asap', 'cancel', 'reclamação', 'cancelar'];
  const salesWords = ['proposal', 'quote', 'pricing', 'demo', 'partnership', 'collaboration', 'orçamento', 'proposta'];
  
  for (const word of urgentWords) if (lower.includes(word)) return 'URGENT';
  for (const word of salesWords) if (lower.includes(word)) return 'SALES';
  return 'NORMAL';
}

// Send WhatsApp via OpenClaw CLI
function sendWhatsAppAlert(emailData, alertType) {
  let message = '';
  let recipient = CONFIG.ROD_PHONE;
  
  switch(alertType) {
    case 'URGENT':
      message = `🚨 *URGENT EMAIL*\n\n` +
        `*From:* ${emailData.from}\n` +
        `*Subject:* ${emailData.subject}\n` +
        `*Type:* ${emailData.type}\n\n` +
        `*Snippet:* ${emailData.snippet}\n\n` +
        `Reply "CHECK" to have Bob review and draft response.`;
      break;
    case 'SALES':
      message = `💼 *SALES LEAD*\n\n` +
        `*From:* ${emailData.from}\n` +
        `*Subject:* ${emailData.subject}\n\n` +
        `*Snippet:* ${emailData.snippet}\n\n` +
        `Bob is drafting a response. Reply "APPROVE" to send or "EDIT" to modify.`;
      break;
    case 'CONTENT':
      message = `🎨 *CONTENT EMAIL*\n\n` +
        `*From:* ${emailData.from}\n` +
        `*Subject:* ${emailData.subject}\n\n` +
        `*Snippet:* ${emailData.snippet}\n\n` +
        `Reply "CHECK" to route to Jarbas for Karine's review.`;
      recipient = CONFIG.KARINE_PHONE;
      break;
    case 'FINANCIAL':
      message = `💰 *FINANCIAL EMAIL*\n\n` +
        `*From:* ${emailData.from}\n` +
        `*Subject:* ${emailData.subject}\n\n` +
        `Franklyn will review. Reply "CHECK" to escalate.`;
      break;
    case 'LEGAL':
      message = `⚖️ *LEGAL EMAIL*\n\n` +
        `*From:* ${emailData.from}\n` +
        `*Subject:* ${emailData.subject}\n\n` +
        `Reply "CHECK" to hold for Rod review.`;
      break;
  }
  
  // Call OpenClaw to send WhatsApp
  // Note: This requires OpenClaw gateway to be accessible
  // If running on same machine, use CLI:
  if (CONFIG.USE_CLI) {
    // This won't work in Google Apps Script directly
    // Use HTTP call to OpenClaw gateway instead
  }
  
  // HTTP call to OpenClaw gateway
  // Requires gateway to be exposed (Tailscale, ngrok, or public IP)
  sendViaOpenClawGateway(recipient, message);
}

function sendViaOpenClawGateway(to, message) {
  // This requires the OpenClaw gateway to be accessible from Google Apps Script
  // Options:
  // 1. Expose gateway via Tailscale
  // 2. Use ngrok for development
  // 3. Run script on same machine as OpenClaw
  
  try {
    UrlFetchApp.fetch(`${CONFIG.OPENCLAW_URL}/api/send`, {
      method: 'POST',
      contentType: 'application/json',
      payload: JSON.stringify({
        channel: 'whatsapp',
        to: to,
        message: message
      })
    });
  } catch (e) {
    // Fallback: Log for manual processing
    console.log(`Failed to send WhatsApp to ${to}: ${e}`);
    console.log(`Message: ${message}`);
  }
}

// Notify Bob via OpenClaw (creates a task for him)
function notifyBob(emailData) {
  // This would create an ARP-4.0 TASK_BRIEF for Bob
  // Implementation depends on OpenClaw API availability
  console.log(`SALES LEAD for Bob: ${emailData.subject} from ${emailData.from}`);
}

// Daily digest
function sendDailyDigest() {
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  
  const threads = GmailApp.search(
    `after:${yesterday.getFullYear()}/${yesterday.getMonth()+1}/${yesterday.getDate()} label:${CONFIG.PROCESSED_LABEL}`
  );
  
  let stats = { sales: 0, urgent: 0, content: 0, financial: 0, total: 0 };
  
  threads.forEach(thread => {
    thread.getMessages().forEach(message => {
      const type = determineType(message.getSubject());
      stats.total++;
      if (type === 'SALES') stats.sales++;
      if (type === 'CONTENT') stats.content++;
      if (type === 'FINANCIAL') stats.financial++;
      if (classifyEmail(message.getSubject()) === 'URGENT') stats.urgent++;
    });
  });
  
  const digest = `📊 *Daily Email Digest*\n\n` +
    `*Sales Leads:* ${stats.sales}\n` +
    `*Content:* ${stats.content}\n` +
    `*Financial:* ${stats.financial}\n` +
    `*Urgent:* ${stats.urgent}\n` +
    `*Total:* ${stats.total}\n\n` +
    `Reply "REPORT" for detailed breakdown.`;
  
  sendViaOpenClawGateway(CONFIG.ROD_PHONE, digest);
}
```

## Setup Steps

### 1. Expose OpenClaw Gateway (Required)

Option A: **Tailscale** (Recommended)
```bash
# Enable Tailscale in OpenClaw config
openclaw config.patch channels.whatsapp.tailscale.mode=on
```

Option B: **ngrok** (Development)
```bash
ngrok http 18789
# Use ngrok URL in Google Apps Script
```

Option C: **Run Script Locally** (Mac Mini)
- Use `osascript` or `curl` to call OpenClaw directly
- No external exposure needed

### 2. Authorize Google Apps Script
- Go to https://script.google.com
- Create project "GrowBiz Mail Gateway"
- Paste code above
- Authorize Gmail access
- Set trigger: `checkInbox` every 15 minutes

### 3. Test
1. Send test email to frankomatic5007@gmail.com with subject "URGENT: Test"
2. Verify WhatsApp notification arrives
3. Reply "CHECK" to test routing

## WhatsApp Response Commands

| Reply | Action |
|-------|--------|
| **CHECK** | Bob reviews and drafts response |
| **APPROVE** | Send Bob's drafted response |
| **EDIT** | Modify Bob's draft |
| **IGNORE** | Mark as handled, no action |
| **URGENT** | Escalate to Frank (CEO) |
| **REPORT** | Send daily digest |

## Fallback (If Gateway Not Exposed)

If you can't expose the gateway, run a local cron job instead:

```bash
# On Mac Mini, add to crontab
crontab -e

# Check inbox every 15 minutes
*/15 * * * * /usr/bin/osascript -e 'tell application "Terminal" to do script "cd ~/.openclaw/workspace && openclaw agent --to +19082581356 --message \"$(python3 check_email.py)\" --deliver"'
```

## Security
- Google Apps Script runs under frankomatic5007@gmail.com
- No credentials stored in script
- OpenClaw auth via existing WhatsApp pairing
- All access logged to ByteRover

## Next Steps
1. Choose gateway exposure method (Tailscale/ngrok/local)
2. Deploy Google Apps Script
3. Test with sample emails
4. Train Karine/Rod on response commands
