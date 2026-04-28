---
name: voice-capture
description: WhatsApp voice note → transcription → Portuguese/English intent classification → ARP routing
metadata:
  {
    "openclaw":
      {
        "emoji": "🎤",
        "requires": { "tools": ["sessions_spawn"], "skills": ["openai-whisper"] },
        "primaryEnv": null
      }
  }
---

# voice-capture

Jarbas's voice-first interface for Karine. Transcribes WhatsApp voice notes, classifies intent in Portuguese or English, and routes to the correct destination.

## When to Use

- Karine sends a voice note on WhatsApp
- Audio needs transcription
- Intent classification needed (task, question, family matter)
- Routing decision required (Frank vs Severino)

## When NOT to Use

- Karine types (use task-capture instead)
- Audio quality is too poor (ask for repeat)
- Code-switching is ambiguous (confirm with Karine)

## Workflow

```
WhatsApp Voice Note → whisper transcribe → intent classification → route
```

## Transcription

Uses bundled `openai-whisper` skill:
- Local processing (no API cost)
- Supports Portuguese (pt) language code
- Handles OGG, WAV, MP3

## Intent Classification

### Domains (Portuguese/English)

| Portuguese | English | Route To |
|------------|---------|----------|
| "tarefa", "preciso", "fazer" | "task", "need to", "do this" | Frank (via task-capture) |
| "família", "crianças", "viagem" | "family", "kids", "travel" | Severino (direct) |
| "post", "publicar", "imigrou" | "post", "publish", "imigrou" | Frank → FrankCMO |
| "dinheiro", "orçamento", "contas" | "money", "budget", "quickbooks" | Frank → FrankCFO |
| "código", "site", "bug" | "code", "website", "bug" | Frank → RodZilla |

### Pre-fill Template

Every task gets this prefix:

```
wife request • urgency=medium • clarify budget first
```

Override urgency:
- "urgente", "agora", "hoje" → urgency=high
- "quando puder", "depois" → urgency=low

## Routing Logic

```
IF intent == family:
  → spawn severino directly (ARP exception allowed)
ELSE IF intent == business:
  → spawn frank with task
ELSE:
  → confirm with Karine before routing
```

## Confirmation Flow

Before acting, Jarbas confirms understanding:

**Karine (PT):** "Preciso marcar a viagem para o Brasil em junho"

**Jarbas:**
```
Entendi! Você quer:
• Planejar viagem para o Brasil em junho
• Isso vai para o Severino (assuntos de família)

Posso enviar para ele? (sim/não)
```

**Karine:** "sim"

**Jarbas:** → Spawns Severino

## Code-Switching

Karine naturally switches mid-sentence:

> "Preciso fazer o post pro Imigrou about that thing we discussed"

**Handling**:
- Detect primary language (first clause = Portuguese)
- Extract intent: "post" + "Imigrou" → marketing task
- Route to Frank → FrankCMO
- Note: "that thing we discussed" requires memory search

## Audio Quality Handling

| Issue | Response |
|-------|----------|
| Kids in background | "Ouvi a maior parte, mas perdi um trecho com as crianças. Pode repetir a parte sobre [X]?" |
| Too quiet | "Não consegui ouvir direito. Pode mandar de novo mais alto?" |
| Car audio/wind | "O áudio do carro atrapalhou um pouco. Pode confirmar: você quer [summary]?" |

## Tool Usage

```javascript
// Step 1: Transcribe
const transcription = await skills.openai_whisper.transcribe(audioPath, { lang: 'pt' });

// Step 2: Classify intent
const intent = await classifyIntent(transcription.text);

// Step 3: Route
if (intent.domain === 'family') {
  await tools.sessions_spawn({
    agentId: 'severino',
    task: buildTask(transcription),
    // ...
  });
} else {
  await tools.sessions_spawn({
    agentId: 'main',
    task: buildTask(transcription),
    // ...
  });
}
```

## Memory

Jarbas doesn't store family state directly. It:
1. Captures voice
2. Classifies
3. Routes
4. Forgets (stateless)

Severino is the canonical family memory.

## Language Rules

- **Input**: Whatever Karine speaks (PT, EN, or mixed)
- **Output**: Match Karine's language
- **Internal**: English for routing logic
- **Never**: Ask Karine to type instead

## Error Handling

| Scenario | Action |
|----------|--------|
| Transcription confidence < 0.75 | Ask for repeat |
| Ambiguous intent | Present options, let Karine choose |
| Unknown domain | Escalate to Frank |
| Severino unavailable | Queue for retry, notify Frank |

## Integration

Called automatically when Jarbas receives WhatsApp voice message:

```javascript
// In Jarbas message handler
if (message.type === 'voice') {
  await skills.voice_capture.process(message);
}
```

## Files

- Temp audio: `~/.openclaw/workspace-jarbas/temp/`
- Transcriptions: `~/.openclaw/workspace-jarbas/memory/voice/`
- Intent logs: `~/.openclaw/workspace-jarbas/logs/voice-capture.log`

## Dependencies

- `openai-whisper` skill (bundled, local)
- `task-capture` skill (for Frank-bound tasks)
- `family-bridge` logic (for Severino direct routing)

## ARP v1.0 Compliance

- ✅ Jarbas → Severino is the ONLY permitted specialist-to-specialist path
- ✅ All other routes go through Frank
- ✅ Pre-fill template on every request
- ✅ Tier 1 only (kimi-k2.5:cloud)
