---
name: task-capture
description: Simplified task creation for Karine — voice/text input, auto-routing to Frank or Severino
metadata:
  {
    "openclaw":
      {
        "emoji": "📝",
        "requires": { "tools": ["sessions_spawn", "write"] },
        "primaryEnv": null
      }
  }
---

# task-capture

Jarbas's lightweight task interface. Karine says it, Jarbas captures it, routes it correctly.

## When to Use

- Karine sends text message (not voice)
- Task needs to be tracked
- Unclear if it's family or business
- Quick capture without full voice processing

## When NOT to Use

- Voice notes (use voice-capture instead)
- Already classified as family (route to Severino directly)
- Complex multi-step workflow (escalate to Frank)

## Capture Format

```
TASK-[ID] captured from Karine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Source: WhatsApp text
Time: [timestamp]
Content: [original message]

Classified:
• Domain: [business|family|unclear]
• Urgency: [low|medium|high]
• Owner: [karine]
• Action: [brief summary]

Routing: [frank|severino|needs-confirmation]
```

## Classification Logic

**Keywords → Domain:**

| Family Keywords | Business Keywords |
|-----------------|-------------------|
| crianças, kids, família | trabalho, work, negócio |
| escola, school, aula | cliente, client, projeto |
| viagem, travel, férias | dinheiro, money, invoice |
| aniversário, birthday | post, publicar, marketing |
| Rebecca, Antonio | Imigrou, Studios, Magazine |

**Unclear** = ask Karine: "Isso é para família ou trabalho?"

## Routing Rules

```
IF domain == family:
  → spawn severino directly (ARP exception)
  → reply: "Enviado para o Severino cuidar da família ✓"

ELSE IF domain == business:
  → spawn frank with task
  → reply: "Encaminhado para o Frank organizar ✓"

ELSE:
  → ask for clarification
  → "Isso é para família ou trabalho?"
```

## Task Template

Every captured task gets:

```yaml
id: TASK-XXXX
created: 2026-03-20T13:30:00Z
source: jarbas
requester: karine
domain: [business|family]
status: captured
urgency: [low|medium|high]
title: [auto-generated summary]
description: [original message]
routed_to: [frank|severino]
```

## Quick Actions

Karine can use shortcuts:

| Shortcut | Meaning | Route |
|----------|---------|-------|
| "!f" or "!família" | Force family | Severino |
| "!t" or "!trabalho" | Force business | Frank |
| "!a" | Urgent | Frank + high priority |
| "?" | Question | Frank (general) |

Example:
> "!f preciso marcar o dentista da Rebecca"

→ Routes to Severino (family override)

## Confirmation Messages

**To Severino:**
```
📤 Enviado para Severino
Tarefa familiar registrada: [summary]
```

**To Frank:**
```
📤 Encaminhado para Frank
Solicitação de trabalho: [summary]
Prioridade: [urgency]
```

**Clarification needed:**
```
❓ Preciso de ajuda para classificar
Isso é para família ou trabalho?

[original message]
```

## Integration with voice-capture

voice-capture handles audio → this skill handles the routing decision

task-capture is called AFTER voice-capture produces transcription:

```javascript
// In voice-capture
const transcription = await transcribe(audio);
await skills.task_capture.process({
  source: 'voice',
  content: transcription.text,
  requester: 'karine'
});
```

## Statelessness

Jarbas doesn't track task lifecycle. After routing:
- Task state lives in destination agent
- Jarbas can query status (read-only)
- Updates come via Frank or Severino

## Language

- Karine writes in PT → Jarbas replies in PT
- Karine writes in EN → Jarbas replies in EN
- Mixed → primary language detected, reply in same

## Examples

**Input:** "preciso fazer o post de sexta"
**Classification:** business, marketing
**Route:** Frank → FrankCMO
**Reply:** "Encaminhado para Frank organizar o post ✓"

**Input:** "!f Rebecca tem aula de ballet amanhã?"
**Classification:** family (forced)
**Route:** Severino
**Reply:** "Enviado para Severino cuidar da agenda da Rebecca ✓"

**Input:** "me lembra depois"
**Classification:** unclear
**Route:** ask clarification
**Reply:** "❓ Me ajuda: isso é para família ou trabalho?"

## Files

- Captured tasks: `~/.openclaw/workspace-jarbas/tasks/captured/`
- Routing log: `~/.openclaw/workspace-jarbas/logs/routing.log`

## ARP Compliance

- ✅ Jarbas → Severino only for family domain
- ✅ All business routes through Frank
- ✅ Pre-fill: "wife request • urgency=medium • clarify budget first"
- ✅ Tier 1 only
