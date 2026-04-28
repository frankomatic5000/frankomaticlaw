# SKILL.md - MailMate

## Name
mailmate

## Description
Email triage, drafting, and sending across all GrowBiz Media operations. Handles everything from Imigrou collaboration requests to GrowBiz Services client outreach to grant application follow-ups. Knows the difference between Rod's voice and Karine's voice.

## When to Use
- Triaging inbox by priority
- Drafting emails
- Replying to threads
- Sending emails (requires approval)
- Searching email history
- Summarizing threads
- Creating outreach sequences
- Following up on grant applications

## Inputs
| Name | Type | Required | Options |
|------|------|----------|---------|
| action | enum | yes | triage, draft, reply, send, search, summarize, outreach_sequence, grant_followup |
| mailbox | enum | no | rod-personal, karine-personal, growbiz-general, growbiz-services, imigrou, studios (default: growbiz-general) |
| to | string | no | - |
| subject | string | no | - |
| body | string | no | - |
| tone | enum | no | formal, friendly, brief, grant-style, sales-outreach, collaboration-pitch, diaspora-warm (default: friendly) |
| language | enum | no | en, pt-br, bilingual (default: en) |
| priority_filter | enum | no | all, urgent, unread, flagged, grant-related, client-related (default: unread) |

## Outputs
Result with: action_completed, triage_summary, draft_content, search_results, approval_status

## Voice Rules
- **rod-personal/growbiz-general:** Rod's voice. Short, direct, slightly nerdy.
- **karine-personal/imigrou/studios:** Karine's voice. Warm, professional, culturally aware. pt-BR if recipient is Brazilian.
- **growbiz-services:** Sales-professional. Value-first, no sleaze.
- **grant-style:** Professional but human. Show impact, numbers, vision.

## Access Control
- **Frank:** All actions
- **Jarbas:** All actions (Karine has full email access)

## Triggers
- "email"
- "inbox"
- "outreach"
- "grant follow"
- "draft email"
- "client email"

## Permissions
- email_api_read
- email_api_write
- memory_read

## Preferred Model
qwen3.5:cloud
## Escalation Model
deepseek-chat (for outreach sequences)
