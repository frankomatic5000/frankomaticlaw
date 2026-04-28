# Gmail Forwarding Script for Bob (Sales & Growth)

## Setup Instructions

### Step 1: Create Google Apps Script
1. Go to https://script.google.com
2. Create new project named "GrowBiz Mail Gateway"
3. Paste the code below
4. Save and authorize with frankomatic5007@gmail.com

### Step 2: Set Up Triggers
1. Click clock icon (Triggers)
2. Add trigger: `checkInbox` function
3. Time-driven: Every 15 minutes
4. Save

### Step 3: Configure Discord Webhook
1. In Discord, create webhook for Bob's channel
2. Copy webhook URL
3. Replace `DISCORD_WEBHOOK_URL` in script

## Google Apps Script Code

```javascript
const CONFIG = {
  // Discord webhook for Bob notifications
  DISCORD_WEBHOOK: 'YOUR_DISCORD_WEBHOOK_URL',
  
  // Label to track processed emails
  PROCESSED_LABEL: 'Bob-Processed',
  
  // Forwarding destinations
  FORWARD_URGENT: 'rod@growbiz.media',
  FORWARD_SALES: 'frankomatic5007@gmail.com',
  
  // Auto-triage keywords
  URGENT_KEYWORDS: ['complaint', 'urgent', 'asap', 'payment', 'invoice', 'legal', 'lawsuit'],
  SALES_KEYWORDS: ['proposal', 'quote', 'pricing', 'demo', 'partnership', 'collaboration', 'sponsor'],
  SPAM_KEYWORDS: ['unsubscribe', 'promotional', 'newsletter', 'marketing']
};

function checkInbox() {
  // Get or create processed label
  let label = GmailApp.getUserLabelByName(CONFIG.PROCESSED_LABEL);
  if (!label) {
    label = GmailApp.createLabel(CONFIG.PROCESSED_LABEL);
  }
  
  // Search for unprocessed emails (last 30 minutes)
  const threads = GmailApp.search('is:unread -label:' + CONFIG.PROCESSED_LABEL, 0, 50);
  
  threads.forEach(thread => {
    const messages = thread.getMessages();
    messages.forEach(message => {
      if (message.isUnread()) {
        processEmail(message, label);
      }
    });
  });
}

function processEmail(message, label) {
  const from = message.getFrom();
  const subject = message.getSubject();
  const body = message.getPlainBody().substring(0, 1000); // First 1000 chars
  const date = message.getDate();
  
  // Determine priority
  const priority = classifyEmail(subject + ' ' + body);
  
  // Extract data
  const emailData = {
    id: message.getId(),
    from: from,
    subject: subject,
    date: date.toISOString(),
    priority: priority,
    snippet: body.substring(0, 200)
  };
  
  // Route based on priority
  switch(priority) {
    case 'URGENT':
      notifyDiscord(emailData, '🚨 URGENT');
      notifyDiscord(emailData, '💼 SALES LEAD');
      break;
    case 'SALES':
      notifyDiscord(emailData, '💼 SALES LEAD');
      break;
    case 'LOW':
      // Just mark as processed, no notification
      break;
  }
  
  // Mark as processed
  label.addToThread(message.getThread());
}

function classifyEmail(text) {
  const lowerText = text.toLowerCase();
  
  // Check urgent keywords
  for (const keyword of CONFIG.URGENT_KEYWORDS) {
    if (lowerText.includes(keyword)) return 'URGENT';
  }
  
  // Check sales keywords
  for (const keyword of CONFIG.SALES_KEYWORDS) {
    if (lowerText.includes(keyword)) return 'SALES';
  }
  
  // Check spam keywords
  for (const keyword of CONFIG.SPAM_KEYWORDS) {
    if (lowerText.includes(keyword)) return 'LOW';
  }
  
  return 'NORMAL';
}

function notifyDiscord(emailData, title) {
  const payload = {
    embeds: [{
      title: title,
      description: `**From:** ${emailData.from}\n**Subject:** ${emailData.subject}\n**Priority:** ${emailData.priority}\n**Snippet:** ${emailData.snippet}`,
      color: title.includes('URGENT') ? 15158332 : 3066993,
      timestamp: emailData.date
    }]
  };
  
  UrlFetchApp.fetch(CONFIG.DISCORD_WEBHOOK, {
    method: 'POST',
    contentType: 'application/json',
    payload: JSON.stringify(payload)
  });
}

// Daily digest function
function sendDailyDigest() {
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  
  const threads = GmailApp.search(`after:${yesterday.getFullYear()}/${yesterday.getMonth()+1}/${yesterday.getDate()} label:${CONFIG.PROCESSED_LABEL}`);
  
  let salesCount = 0;
  let urgentCount = 0;
  
  threads.forEach(thread => {
    thread.getMessages().forEach(message => {
      const subject = message.getSubject();
      if (classifyEmail(subject) === 'SALES') salesCount++;
      if (classifyEmail(subject) === 'URGENT') urgentCount++;
    });
  });
  
  const payload = {
    embeds: [{
      title: '📊 Daily Email Digest',
      description: `**Sales Leads:** ${salesCount}\n**Urgent Items:** ${urgentCount}\n**Total Processed:** ${threads.length}`,
      color: 3447003,
      timestamp: new Date().toISOString()
    }]
  };
  
  UrlFetchApp.fetch(CONFIG.DISCORD_WEBHOOK, {
    method: 'POST',
    contentType: 'application/json',
    payload: JSON.stringify(payload)
  });
}
```

## Output Format

Bob receives Discord messages like:

**💼 SALES LEAD**
- From: client@example.com
- Subject: Partnership proposal for GrowBiz Studios
- Priority: SALES
- Snippet: "Hi, I'd love to discuss a collaboration..."

## Manual Trigger

To manually check inbox:
```javascript
// In Google Apps Script editor
function manualCheck() {
  checkInbox();
}
```

## Integration with OpenClaw

When Bob receives Discord notification, he can:
1. Reply in Discord to acknowledge
2. Draft response via `mail-mate` skill
3. Send for Rod/Karine approval
4. Log to CRM

## Security Notes
- Script runs under frankomatic5007@gmail.com permissions
- Only reads emails (no sending)
- PII handled via Discord webhook (encrypted)
- No credentials stored in code

## Next Steps
1. Set up Discord webhook URL
2. Authorize script with Gmail
3. Test with 1-2 emails
4. Enable triggers
5. Train Bob on response templates
