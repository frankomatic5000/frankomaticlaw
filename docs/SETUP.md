# 🚀 Setup Guide — Frank + Jarbas

> GrowBiz Media · OpenClaw Platform

---

## Prerequisites

| Requirement | Details |
|---|---|
| Docker | Required for self-hosted OpenClaw gateway |
| Ollama Pro | $20/mo cloud subscription — 3 model slots |
| DeepSeek API key | [platform.deepseek.com](https://platform.deepseek.com) |
| Gemini API key | [Google AI Studio](https://aistudio.google.com) |
| Discord bot token | [Discord Developer Portal](https://discord.com/developers) |
| WhatsApp Business API | Verified number + API access |
| QuickBooks OAuth | Developer app + OAuth credentials |
| GitHub PAT | Personal access token with repo scope |
| Node.js 18+ | For any local tooling |
| Git | For repo management |

---

## Phase 1: Repository Setup

```bash
# Clone the repo
git clone https://github.com/frankomatic5000/frankomaticlaw.git
cd frankomaticlaw

# Copy environment template
cp .env.example .env

# Edit .env with your real values
# Use your editor of choice
nano .env
```

### Required .env Variables (minimum to start)

```bash
# Models — need these first
OLLAMA_PRO_KEY=your_key
DEEPSEEK_API_KEY=your_key
GEMINI_API_KEY=your_key

# Channels — need these for agents to respond
DISCORD_BOT_TOKEN=your_token
WHATSAPP_API_TOKEN=your_token
```

---

## Phase 2: Install OpenClaw

```bash
# Pull and run OpenClaw via Docker
docker pull openclaw/openclaw:latest

# Run with config pointing to this repo
docker run -d \
  --name frankomaticlaw \
  -p 18789:18789 \
  -v $(pwd):/app/workspace \
  --env-file .env \
  openclaw/openclaw:latest

# Verify it's running
docker logs frankomaticlaw
```

### Verify OpenClaw reads the config

```bash
# Check that SOUL.md is loaded
curl http://localhost:18789/health

# Check that skills are detected
curl http://localhost:18789/skills

# Expected: taskmaster, socialclaw, mailmate, bizguard, codeforge
```

---

## Phase 3: Configure Model Providers

### Tier 1 — Ollama Pro Cloud ($20/mo flat)

1. Subscribe at [ollama.com](https://ollama.com)
2. Enable cloud model slots
3. Verify these models are available:
   - `kimi-k2.5:cloud` (default/general)
   - `minimax-m2.7:cloud` (code)
   - `qwen3.5:cloud` (content/email)
4. Add `OLLAMA_PRO_KEY` to `.env`

### Tier 2 — DeepSeek API (~$3-12/mo usage)

1. Sign up at [platform.deepseek.com](https://platform.deepseek.com)
2. Create an API key
3. Add `DEEPSEEK_API_KEY` to `.env`
4. Available models:
   - `deepseek-chat` (complex reasoning)
   - `deepseek-reasoner` (deep thinking)

### Tier 3 — Gemini 2.5 Pro (~$2-6/mo usage)

1. Get API key from [Google AI Studio](https://aistudio.google.com)
2. Add `GEMINI_API_KEY` to `.env`
3. Set weekly cap: `GEMINI_WEEKLY_CAP=8` in `.env`

---

## Phase 4: Set Up Channels

### Discord (Frank)

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create new application: `Frankomatic5007`
3. Go to Bot → Create Bot
4. Copy token → `DISCORD_BOT_TOKEN` in `.env`
5. Enable these Privileged Gateway Intents:
   - Message Content Intent
   - Server Members Intent
6. Generate OAuth2 URL with `bot` scope + `Send Messages`, `Read Messages`
7. Invite bot to your Discord server

### WhatsApp (Jarbas)

1. Set up WhatsApp Business API via Meta Business Suite
2. Register and verify your phone number
3. Get API token → `WHATSAPP_API_TOKEN` in `.env`
4. Get phone number ID → `WHATSAPP_PHONE_NUMBER_ID` in `.env`
5. Configure webhook URL to point to OpenClaw gateway:
   `https://your-domain:18789/whatsapp/webhook`
6. Enable voice message support (for Karine's voice notes)

### Voice Transcription (Whisper)

Jarbas needs to transcribe Karine's voice messages:

```bash
# Whisper runs inside the OpenClaw container
# Configure in .env:
WHISPER_MODEL=large-v3
WHISPER_LANGUAGES=pt,en
```

---

## Phase 5: Connect Integrations

### QuickBooks (BizGuard)

1. Create app at [developer.intuit.com](https://developer.intuit.com)
2. Set up OAuth2 flow
3. Add credentials to `.env`:
   ```
   QUICKBOOKS_CLIENT_ID=your_id
   QUICKBOOKS_CLIENT_SECRET=your_secret
   QUICKBOOKS_REFRESH_TOKEN=your_token
   QUICKBOOKS_REALM_ID=your_realm
   ```

### Email (MailMate)

1. Set up Gmail App Password or SMTP credentials
2. Add to `.env`:
   ```
   EMAIL_SMTP_HOST=smtp.gmail.com
   EMAIL_SMTP_PORT=587
   EMAIL_USERNAME=your_email
   EMAIL_PASSWORD=your_app_password
   ```

### Social Platforms (SocialClaw)

Add API tokens for each platform to `.env`:
- Twitter/X API key + secret
- Instagram access token
- LinkedIn access token
- TikTok access token

### GitHub (CodeForge)

1. Create a Personal Access Token with `repo` scope
2. Add to `.env`: `GITHUB_PAT=your_token`

---

## Phase 5: Test Everything

### Test 1: Frank on Discord

Send a message in your Discord server:
```
@Frankomatic5007 what's my engineering status?
```

**Expected:** Frank responds with pipeline status across products,
routed through Tier 1 (`minimax-m2.7:cloud`), task ID assigned.

### Test 2: Jarbas on WhatsApp

Send a voice note to the Jarbas WhatsApp number:
> "Jarbas, agenda o post do Imigrou pra quinta-feira"

**Expected:** Jarbas transcribes, confirms in pt-BR:
*"Entendi — quer que eu agende o post do Imigrou pra quinta. Correto?"*

### Test 3: Approval Flow

Ask Frank on Discord:
```
@Frankomatic5007 deploy magazine to production
```

**Expected:** Frank asks for approval before executing (deploy requires Rod's approval).

### Test 4: Budget Guard

Check budget status:
```
@Frankomatic5007 budget check
```

**Expected:** Dashboard showing spend by tier, remaining budget, any alerts.

### Test 5: Cross-Agent Forward

Send via Jarbas (WhatsApp):
> "Submit the NJEDA grant application"

**Expected:** Jarbas responds:
*"That needs Frank's approval. Forwarded to Frank task #XXXX — confirm?"*

---

## Troubleshooting

| Problem | Solution |
|---|---|
| OpenClaw won't start | Check Docker logs: `docker logs frankomaticlaw` |
| Skills not loading | Verify `skills/` directory is mounted and YAML is valid |
| SOUL.md not found | Check `.clawopenrc` → `[soul] path = SOUL.md` |
| Discord bot offline | Verify token, check intents are enabled |
| WhatsApp not receiving | Check webhook URL, verify Meta app is in Live mode |
| Voice transcription fails | Check Whisper model is downloaded, language config correct |
| Budget alerts not firing | Check `config/budget.yaml` thresholds and schedule |
| Model timeout | Tier 1 latency guard should auto-skip to Tier 2 after 30s |
| QuickBooks auth expired | Refresh OAuth token — check `QUICKBOOKS_REFRESH_TOKEN` |

---

## File Structure Reference

```
frankomatic5000/frankomaticlaw/
├── SOUL.md                          # Agent identities & personality
├── README.md                        # Project overview
├── .clawopenrc                      # OpenClaw runtime config
├── .env.example                     # Environment variable template
├── .gitignore                       # Git ignore rules
├── config/
│   ├── agents.yaml                  # Agent definitions & permissions
│   ├── router.yaml                  # Inference router tiers & guards
│   ├── memory.yaml                  # Memory layer configuration
│   └── budget.yaml                  # Budget thresholds & alerts
├── skills/
│   ├── taskmaster.skill.yaml        # Central task backbone
│   ├── socialclaw.skill.yaml        # Social media intelligence
│   ├── mailmate.skill.yaml          # Email triage & sending
│   ├── bizguard.skill.yaml          # QuickBooks, grants, tax
│   └── codeforge.skill.yaml         # GitHub & code implementation
├── memory/
│   ├── frank-personal.md            # Rod's private notes
│   ├── family-shared.md             # Shared family context
│   └── projects/                    # Per-task context files
│       └── .gitkeep
└── docs/
    ├── ARCHITECTURE.md              # System architecture & diagrams
    └── SETUP.md                     # This file
```

---

<p align="center">
  Built with 🧠 by Rod & Karine · Powered by OpenClaw · GrowBiz Media
</p>