#!/bin/bash
# Gmail Checker for Bob — Runs locally on Mac Mini
# Checks frankomatic5007@gmail.com and sends WhatsApp alerts via OpenClaw

EMAIL_ACCOUNT="frankomatic5007@gmail.com"
ROD_PHONE="+19082581356"
KARINE_PHONE="+18622520852"
PROCESSED_FILE="$HOME/.openclaw/workspace/Bob/data/processed-emails.txt"

# Ensure processed file exists
touch "$PROCESSED_FILE"

# Check if gmvault or similar is installed for Gmail access
# For now, using AppleScript to check Mail.app if configured
# Or use Google Apps Script webhook

echo "Gmail check started at $(date)"

# TODO: Implement Gmail IMAP check or Google Apps Script webhook
# This script serves as the local executor when Google Apps Script calls back

# Example: When Google Apps Script detects URGENT email, it calls this script:
# ./check-gmail.sh --urgent --from "client@example.com" --subject "URGENT: Help needed"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --urgent)
      PRIORITY="URGENT"
      shift
      ;;
    --sales)
      PRIORITY="SALES"
      shift
      ;;
    --content)
      PRIORITY="CONTENT"
      shift
      ;;
    --from)
      FROM="$2"
      shift 2
      ;;
    --subject)
      SUBJECT="$2"
      shift 2
      ;;
    --snippet)
      SNIPPET="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

# Send WhatsApp via OpenClaw CLI
if [[ "$PRIORITY" == "URGENT" ]]; then
  MESSAGE="🚨 URGENT EMAIL\n\nFrom: $FROM\nSubject: $SUBJECT\n\nReply CHECK to have Bob draft response."
  openclaw agent --to "$ROD_PHONE" --message "$MESSAGE" --deliver --channel whatsapp
  
elif [[ "$PRIORITY" == "SALES" ]]; then
  MESSAGE="💼 SALES LEAD\n\nFrom: $FROM\nSubject: $SUBJECT\n\nBob will draft a response. Reply APPROVE to send."
  openclaw agent --to "$ROD_PHONE" --message "$MESSAGE" --deliver --channel whatsapp
  
elif [[ "$PRIORITY" == "CONTENT" ]]; then
  MESSAGE="🎨 CONTENT EMAIL\n\nFrom: $FROM\nSubject: $SUBJECT\n\nReply CHECK to route to Jarbas for Karine's review."
  openclaw agent --to "$KARINE_PHONE" --message "$MESSAGE" --deliver --channel whatsapp
fi

echo "WhatsApp alert sent: $PRIORITY - $SUBJECT"
