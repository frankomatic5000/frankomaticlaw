# Gmail Integration for Bob — Direct OpenClaw Routing

## Architecture

```
frankomatic5007@gmail.com
    ↓ (Google Apps Script monitors)
URGENT / SALES detected
    ↓
OpenClaw WhatsApp channel
    ↓
Jarbas → Routes to Karine/Rod based on type
```

## Why This Works Better
- **No Discord webhook** — Direct OpenClaw integration
- **Jarbas handles routing** — Cultural gate decides who gets pinged
- **WhatsApp native** — Karine/Rod get real notifications on their phones
- **Bob stays in loop** — Can draft responses via OpenClaw

## Google Apps Script (Updated)

Replace Discord webhook with OpenClaw webhook URL:

```javascript
const CONFIG = {
  // OpenClaw webhook endpoint (your local gateway or cloud relay)
  OPENCLAW_WEBHOOK: 'https://your-openclaw-webhook-url.com/webhook',
  
  // Or use WhatsApp Business API directly
  WHATSAPP_API_URL: 'https://graph.facebook.com/v18.0/YOUR_PHONE_NUMBER_ID/messages',
  WHATSAPP_ACCESS_TOKEN: 'YOUR_TOKEN',
  
  // Direct numbers for URGENT routing
  KARINE_WHATSAPP: '+19739371073',
  ROD_WHATSAPP: '+18622520852',
  
  PROCESSED_LABEL: 'Bob-Processed'
};

function checkInbox() {
  let label = GmailApp.getUserLabelByName(CONFIG.PROCESSED_LABEL);
  if (!label) {
    label = GmailApp.createLabel(CONFIG.PROCESSED_LABEL);
  }
  
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
  
  const emailData = {
    id: message.getId(),
    from: from,
    subject: subject,
    date: message.getDate().toISOString(),
    priority: priority,
    snippet: body.substring(0, 200),
    type: determineType(subject)
  };
  
  // Route based on priority and type
  if (priority === 'URGENT') {
    notifyWhatsApp(emailData, 'URGENT');
  } else if (priority === 'SALES') {
    notifyOpenClaw(emailData, 'SALES');
  }
  
  label.addToThread(message.getThread());
}

function determineType(subject) {
  const s = subject.toLowerCase();
  if (s.includes('imigrou') || s.includes('content') || s.includes('karine')) return 'CONTENT';
  if (s.includes('invoice') || s.includes('payment') || s.includes('tax')) return 'FINANCIAL';
  if (s.includes('legal') || s.includes('contract')) return 'LEGAL';
  if (s.includes('proposal') || s.includes('partnership') || s.includes('collaboration')) return 'SALES';
  return 'GENERAL';
}

function classifyEmail(text) {
  const lower = text.toLowerCase();
  const urgentWords = ['complaint', 'urgent', 'asap', 'payment', 'invoice', 'legal', 'lawsuit', 'cancel'];
  const salesWords = ['proposal', 'quote', 'pricing', 'demo', 'partnership', 'collaboration', 'sponsor'];
  
  for (const word of urgentWords) if (lower.includes(word)) return 'URGENT';
  for (const word of salesWords) if (lower.includes(word)) return 'SALES';
  return 'NORMAL';
}

// Send WhatsApp message via OpenClaw or WhatsApp Business API
function notifyWhatsApp(emailData, priority) {
  // Option 1: Use OpenClaw webhook (if exposed to internet)
  // Option 2: Use WhatsApp Business API directly
  
  const message = `🚨 URGENT EMAIL\n\n` +
    `From: ${emailData.from}\n` +
    `Subject: ${emailData.subject}\n` +
    `Type: ${emailData.type}\n` +
    `Snippet: ${emailData.snippet}\n\n` +
    `Reply "CHECK" to have Bob draft a response.`;
  
  // Send to both Rod and Karine for URGENT
  sendWhatsAppMessage(CONFIG.ROD_WHATSAPP, message);
  if (emailData.type === 'CONTENT') {
    sendWhatsAppMessage(CONFIG.KARINE_WHATSAPP, message);
  }
}

function sendWhatsAppMessage(to, message) {
  // Using WhatsApp Business API
  UrlFetchApp.fetch(CONFIG.WHATSAPP_API_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${CONFIG.WHATSAPP_ACCESS_TOKEN}`,
      'Content-Type': 'application/json'
    },
    payload: JSON.stringify({
      messaging_product: 'whatsapp',
      recipient_type: 'individual',
      to: to,
      type: 'text',
      text: { body: message }
    })
  });
}

// Notify OpenClaw for SALES leads
function notifyOpenClaw(emailData, priority) {
  const payload = {
    protocol: 'ARP-4.0',
    type: 'TASK_BRIEF',
    from: 'bob-mail-gateway',
    to: 'bob',
    priority: priority === 'SALES' ? 'P1' : 'P2',
    status: 'NEW',
    taskId: `EMAIL-${emailData.id}`,
    data: emailData
  };
  
  UrlFetchApp.fetch(CONFIG.OPENCLAW_WEBHOOK, {
    method: 'POST',
    contentType: 'application/json',
    payload: JSON.stringify(payload)
  });
}
```

## OpenClaw Routing

When OpenClaw receives the webhook:

```
SALES Lead Detected
    ↓
Bob gets notified in Discord
    ↓
Bob drafts response
    ↓
Flags for Rod/Karine approval
    ↓
Bob sends via Gmail
```

For URGENT:
```
URGENT Email Detected
    ↓
WhatsApp sent to Rod (and Karine if content-related)
    ↓
Rod replies "CHECK" or ignores
    ↓
If "CHECK": Bob drafts response
    ↓
Sends to Rod for approval
```

## WhatsApp Response Commands

Rod/Karine can reply with:
- **"CHECK"** — Have Bob review and draft response
- **"DONE"** — Mark as handled, no action needed
- **"URGENT"** — Escalate to Frank (CEO)

## Setup Requirements

### Option A: WhatsApp Business API (Recommended)
1. Create Meta Business account
2. Set up WhatsApp Business API
3. Get phone number ID and access token
4. Update script with credentials

### Option B: OpenClaw Webhook (If Exposed)
1. Expose OpenClaw gateway to internet (Tailscale, ngrok)
2. Configure webhook endpoint
3. Script posts to webhook directly

### Option C: WhatsApp Plugin (If Available)
Check if OpenClaw has WhatsApp Business plugin

## Advantages Over Discord Webhook
- ✅ Karine/Rod get phone notifications instantly
- ✅ No Discord dependency
- ✅ Jarbas can route culturally appropriate content
- ✅ Direct reply via WhatsApp (familiar interface)
- ✅ No additional app needed

## Next Steps
1. Choose Option A, B, or C
2. Get WhatsApp Business API credentials (Option A)
3. Update Google Apps Script
4. Test with 1-2 emails
5. Enable triggers
