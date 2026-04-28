#!/usr/bin/env python3
"""
Bob's Gmail IMAP Monitor
Runs locally on Mac Mini, checks frankomatic5007@gmail.com via IMAP,
sends WhatsApp alerts via OpenClaw CLI.
"""

import imaplib
import email
import email.header
import re
import subprocess
import sys
import json
import os
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime

# Configuration
CONFIG = {
    "imap_server": "imap.gmail.com",
    "imap_port": 993,
    "email_account": "frankomatic5007@gmail.com",
    # Password should be stored in keychain or env var
    # For Gmail, use App Password (not regular password)
    "app_password": os.environ.get("GMAIL_APP_PASSWORD", ""),
    
    # Phone numbers
    "rod_phone": "+19082581356",
    "karine_phone": "+18622520852",
    
    # State file
    "state_file": os.path.expanduser("~/.openclaw/workspace/Bob/data/email-state.json"),
    
    # Alert thresholds
    "check_interval_minutes": 15,
}

# Keywords for classification
URGENT_KEYWORDS = [
    "complaint", "urgent", "asap", "cancel", "reclamação", "cancelar",
    "payment issue", "invoice problem", "legal", "lawsuit", "chargeback"
]

SALES_KEYWORDS = [
    "proposal", "quote", "pricing", "demo", "partnership", "collaboration",
    "sponsor", "orçamento", "proposta", "budget", "investment"
]

CONTENT_KEYWORDS = [
    "imigrou", "content", "karine", "video", "estudio", "studio",
    "podcast", "youtube", "tiktok", "instagram", "social media"
]

FINANCIAL_KEYWORDS = [
    "invoice", "payment", "tax", "fatura", "imposto", "receipt",
    "billing", "subscription", "refund"
]

LEGAL_KEYWORDS = [
    "contract", "legal", "agreement", "terms", "policy", "gdpr",
    "privacy", "compliance", "contrato"
]

def classify_email(subject, body):
    """Classify email priority and type."""
    text = (subject + " " + body).lower()
    
    # Check priority first
    for keyword in URGENT_KEYWORDS:
        if keyword in text:
            return "URGENT", determine_type(text)
    
    # Check type
    email_type = determine_type(text)
    if email_type == "SALES":
        return "SALES", email_type
    elif email_type == "CONTENT":
        return "NORMAL", email_type  # Content is normal priority unless urgent
    
    return "NORMAL", email_type

def determine_type(text):
    """Determine email type."""
    for keyword in CONTENT_KEYWORDS:
        if keyword in text:
            return "CONTENT"
    
    for keyword in SALES_KEYWORDS:
        if keyword in text:
            return "SALES"
    
    for keyword in FINANCIAL_KEYWORDS:
        if keyword in text:
            return "FINANCIAL"
    
    for keyword in LEGAL_KEYWORDS:
        if keyword in text:
            return "LEGAL"
    
    return "GENERAL"

def decode_header(header):
    """Decode email header."""
    decoded, charset = email.header.decode_header(header)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(charset or 'utf-8')
    return decoded

def get_email_body(msg):
    """Extract plain text body from email."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        except:
            body = str(msg.get_payload())
    return body[:1000]  # First 1000 chars

def load_state():
    """Load processed email IDs."""
    if os.path.exists(CONFIG["state_file"]):
        with open(CONFIG["state_file"], 'r') as f:
            return json.load(f)
    return {"processed_ids": [], "last_check": None}

def save_state(state):
    """Save processed email IDs."""
    os.makedirs(os.path.dirname(CONFIG["state_file"]), exist_ok=True)
    with open(CONFIG["state_file"], 'w') as f:
        json.dump(state, f)

def send_whatsapp_alert(phone, message):
    """Send WhatsApp via OpenClaw CLI."""
    try:
        cmd = [
            "openclaw", "agent",
            "--to", phone,
            "--message", message,
            "--deliver",
            "--channel", "whatsapp"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ WhatsApp sent to {phone}")
            return True
        else:
            print(f"❌ Failed to send WhatsApp: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error sending WhatsApp: {e}")
        return False

def send_alert(priority, email_type, from_addr, subject, snippet):
    """Send appropriate alert based on email classification."""
    
    if priority == "URGENT":
        if email_type == "CONTENT":
            message = f"""🚨 *URGENT CONTENT EMAIL*

*From:* {from_addr}
*Subject:* {subject}

*Snippet:* {snippet}

Reply "CHECK" to route to Jarbas for Karine's review."""
            send_whatsapp_alert(CONFIG["karine_phone"], message)
        else:
            message = f"""🚨 *URGENT EMAIL*

*From:* {from_addr}
*Subject:* {subject}
*Type:* {email_type}

*Snippet:* {snippet}

Reply "CHECK" to have Bob draft response."""
            send_whatsapp_alert(CONFIG["rod_phone"], message)
    
    elif priority == "SALES":
        message = f"""💼 *SALES LEAD*

*From:* {from_addr}
*Subject:* {subject}

*Snippet:* {snippet}

Bob is drafting a response. Reply "APPROVE" to send or "EDIT" to modify."""
        send_whatsapp_alert(CONFIG["rod_phone"], message)
    
    elif email_type == "FINANCIAL":
        message = f"""💰 *FINANCIAL EMAIL*

*From:* {from_addr}
*Subject:* {subject}

*Snippet:* {snippet}

Franklyn will review. Reply "CHECK" to escalate."""
        send_whatsapp_alert(CONFIG["rod_phone"], message)
    
    elif email_type == "LEGAL":
        message = f"""⚖️ *LEGAL EMAIL*

*From:* {from_addr}
*Subject:* {subject}

*Snippet:* {snippet}

Reply "CHECK" to hold for Rod review."""
        send_whatsapp_alert(CONFIG["rod_phone"], message)

def check_inbox():
    """Main function to check Gmail inbox."""
    if not CONFIG["app_password"]:
        print("❌ GMAIL_APP_PASSWORD not set")
        print("Set it with: export GMAIL_APP_PASSWORD='your-app-password'")
        return
    
    state = load_state()
    processed_ids = set(state.get("processed_ids", []))
    
    try:
        # Connect to Gmail IMAP
        print(f"🔌 Connecting to {CONFIG['imap_server']}...")
        mail = imaplib.IMAP4_SSL(CONFIG["imap_server"], CONFIG["imap_port"])
        mail.login(CONFIG["email_account"], CONFIG["app_password"])
        mail.select("inbox")
        
        # Search for unread emails
        status, messages = mail.search(None, "UNSEEN")
        
        if status != "OK" or not messages[0]:
            print("📭 No new emails")
            mail.logout()
            return
        
        email_ids = messages[0].split()
        print(f"📧 Found {len(email_ids)} unread emails")
        
        new_emails = []
        
        for email_id in email_ids:
            email_id_str = email_id.decode()
            
            # Skip already processed
            if email_id_str in processed_ids:
                continue
            
            # Fetch email
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            if status != "OK":
                continue
            
            # Parse email
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            subject = decode_header(msg["Subject"]) if msg["Subject"] else "(No Subject)"
            from_addr = msg["From"] if msg["From"] else "Unknown"
            body = get_email_body(msg)
            
            # Classify
            priority, email_type = classify_email(subject, body)
            
            print(f"📨 [{priority}] [{email_type}] {subject[:60]}...")
            
            # Send alert for important emails
            if priority in ["URGENT", "SALES"] or email_type in ["FINANCIAL", "LEGAL"]:
                snippet = body[:200] if body else "(No preview)"
                send_alert(priority, email_type, from_addr, subject, snippet)
                new_emails.append({
                    "id": email_id_str,
                    "from": from_addr,
                    "subject": subject,
                    "priority": priority,
                    "type": email_type,
                    "time": datetime.now().isoformat()
                })
            
            # Mark as processed
            processed_ids.add(email_id_str)
        
        # Save state
        state["processed_ids"] = list(processed_ids)
        state["last_check"] = datetime.now().isoformat()
        save_state(state)
        
        # Log summary
        if new_emails:
            print(f"\n✅ Processed {len(new_emails)} important emails")
            for e in new_emails:
                print(f"   - [{e['priority']}] {e['subject']}")
        
        mail.logout()
        
    except Exception as e:
        print(f"❌ Error checking inbox: {e}")
        import traceback
        traceback.print_exc()

def send_daily_digest():
    """Send daily summary of emails."""
    state = load_state()
    processed = state.get("processed_ids", [])
    last_check = state.get("last_check")
    
    message = f"""📊 *Daily Email Digest*

*Processed today:* {len(processed)} emails
*Last check:* {last_check or 'Never'}

Reply "REPORT" for detailed breakdown."""
    
    send_whatsapp_alert(CONFIG["rod_phone"], message)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--digest":
        send_daily_digest()
    else:
        check_inbox()
