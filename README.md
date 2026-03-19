# 🤖 frankomaticlaw

> Agentic system for family business automation — dual-agent (Discord + WhatsApp),
> inference router with tiered model escalation, 5 modular skills, $50/mo budget cap.
> Built on OpenClaw for GrowBiz Media.

Built by **Rod & Karine** — immigrants, entrepreneurs, building a media empire
one YAML file at a time.

---

## 📋 Table of Contents

- [The Business](#the-business)
- [The System](#the-system)
- [Agents](#agents)
- [Inference Router](#inference-router)
- [Skills](#skills)
- [Memory](#memory)
- [Budget](#budget)
- [Getting Started](#getting-started)
- [File Structure](#file-structure)
- [License](#license)

---

## The Business

### GrowBiz Media

> *"We build systems that let people tell their stories, grow their businesses,
> and create legacies — without losing themselves in the process."*

GrowBiz Media is a family-owned media and technology company operating at the
intersection of storytelling, automation, and entrepreneurship. Founded by an
immigrant couple in New Jersey with a purpose: to help people grow — in business,
in identity, and in life.

**Mission:** Create world-class media content and AI-powered business tools that
help immigrant entrepreneurs and small businesses build visibility, income, and
lasting legacy.

**Vision:** A world where your origin is your advantage, not your obstacle.

### The Portfolio

| Brand | What It Does | Owner |
|---|---|---|
| 🎙️ **Imigrou** | Brazilian diaspora media channel (YouTube-first) | Karine |
| 🎬 **GrowBiz Studios** | Video production company (Sony FX3, full pipeline) | Karine |
| 📰 **GrowBiz Magazine** | Digital publication for immigrant entrepreneurs (Next.js + Sanity + Vercel) | Both |
| ⚡ **ClipIQ** | AI content automation — long-form → short-form clips at scale | Rod |
| 🎬 **Vaptlux** | AI multi-camera video editing agent | Rod |
| 📍 **GrowBiz Services** | AI-powered local SEO for small businesses ($297–$997/mo) | Rod |
| 🖊️ **DoodleType** | Creative brand / digital products | Both |
| 🤖 **ZecaOS** | AI assistant platform (Microsoft-aligned) | Rod |

---

## The System

Two agents. Five skills. Three model tiers. One $50/month budget.

```
┌──────────────┐          ┌────────────────────┐
│   Discord    │──────────▶  INFERENCE ROUTER   │
│   (Frank)    │          │  Classify → Route   │
├──────────────┤          │  → Budget Guard     │
│  WhatsApp    │──────────▶                     │
│  (Jarbas) 🎤 │          └────────┬────────────┘
└──────────────┘                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
              ┌──────────┐  ┌──────────┐  ┌──────────┐
              │  TIER 1  │  │  TIER 2  │  │  TIER 3  │
              │ Ollama   │  │ DeepSeek │  │ Gemini   │
              │ $20 flat │  │ $3-12/mo │  │ $2-6/mo  │
              │ 80-85%   │  │ 10-15%   │  │ <5%      │
              └──────────┘  └──────────┘  └──────────┘
                    │
                    ▼
    ┌───────────────────────────────────────┐
    │            5 SKILLS                   │
    │ TaskMaster · SocialClaw · MailMate    │
    │ BizGuard · CodeForge                 │
    └───────────────────────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────────────┐
    │          4 MEMORY LAYERS              │
    │ Session · Personal · Shared · Project │
    └───────────────────────────────────────┘
```

### Design Principles

| Principle | What It Means |
|---|---|
| **Cheap first** | 80%+ of requests use flat-rate Ollama Pro. Escalate only when confidence drops |
| **No AI swarm** | Max 2 agents. Zero subagents. More skills, fewer agents |
| **Budget is law** | Hard cap $50/mo. System pauses/aborts before exceeding |
| **Approval gates** | Humans approve writes. AI drafts, humans ship |
| **Voice-first for family** | WhatsApp voice messages are Jarbas's primary input |
| **Brand-aware** | Every skill knows which brand it's working for and matches the voice |

### Hard Rules

- ❌ No Claude, no GPT — ever
- ❌ No local Ollama — cloud only (`:cloud` tagged)
- ❌ No subagents — skills only
- ✅ Max 2 top-level agents
- ✅ $50/month total budget cap
- ✅ Karine's voice is sacred — never auto-publish without her approval

---

## Agents

### Frankomatic5007 (Primary — Discord)

Rod's main brain. Full orchestrator across all brands, all skills, all model tiers.

| Property | Value |
|---|---|
| **Channel** | Discord |
| **Permissions** | Full read, write, approve, all tiers |
| **Personality** | Casual, sharp, sarcastic, short answers |
| **Default model** | `kimi-k2.5:cloud` |

### Jarbas (Secondary — WhatsApp)

Karine's capable assistant. Full access to content, email, social, and QuickBooks.
Not a dumbed-down proxy — a respectful extension of a woman who ran corporate
boardrooms before she ran a production studio.

| Property | Value |
|---|---|
| **Channel** | WhatsApp (voice-first 🎤) |
| **Permissions** | Content, email, social, QuickBooks (capped at $500) |
| **Personality** | Warm, precise, pt-BR fluent, culturally aware |
| **Default model** | `kimi-k2.5:cloud` (Tier 1 only) |

### Approval Matrix

| Action | Frank | Karine via Jarbas |
|---|---|---|
| Personal / calendar / groceries | ✅ Auto | ✅ Karine approves |
| Read / analyze / draft | ✅ Auto | ✅ Auto |
| Send email | ✅ Approves | ✅ Karine approves |
| Publish social | ✅ Approves | ✅ Karine approves |
| QuickBooks (≤$500) | ✅ Approves | ✅ Karine approves |
| QuickBooks (>$500) / reconcile | ✅ Approves | 🔒 Forward to Frank |
| Grant submissions | ✅ Approves | 🔒 Forward to Frank |
| Code deploys / PR merges | ✅ Approves | 🔒 Forward to Frank |

---

## Inference Router

Runs **FIRST** on every request. No exceptions.

| Condition | Route | Models |
|---|---|---|
| Confidence > 0.75, L1–L3 | **Tier 1** | kimi-k2.5, minimax-m2.7, qwen3.5 (all :cloud) |
| Confidence 0.50–0.75, L3–L4 | **Tier 2** | deepseek-chat, deepseek-reasoner |
| Confidence < 0.50, vision/search fail | **Tier 3** | gemini-2.5-pro |
| From Jarbas | **Force Tier 1** | kimi-k2.5:cloud (always) |

### Guards

| Guard | Trigger | Action |
|---|---|---|
| Auto-summarize | Input > 3k tokens | Compress before routing |
| Latency skip | Ollama Pro > 30s | Skip to DeepSeek |
| Cache enforce | DeepSeek repeated context | Force summary reuse |
| Budget pause | Monthly > $35 | Pause Tier 3 |
| Budget abort | Monthly > $48 | Abort non-Tier-1 |
| Gemini cap | Weekly > $8 | Hard stop Tier 3 |

---

## Skills

All skills follow ClawHub template format. Zero subagents.

| Skill | Purpose | Key Brands | Model |
|---|---|---|---|
| **TaskMaster** | Central task backbone, brand-aware routing | All | Any |
| **SocialClaw** | Multi-brand social media + ClipIQ integration | Imigrou, GrowBiz, DoodleType | kimi-k2.5:cloud |
| **MailMate** | Email ops, outreach sequences, grant follow-ups | Services, Studios, Imigrou | qwen3.5:cloud |
| **BizGuard** | QuickBooks, grants, MRR tracking, tax, equipment | Services, Studios, All | qwen3.5 → deepseek |
| **CodeForge** | GitHub, deploys, content engine, multi-product | ClipIQ, Vaptlux, Magazine, ZecaOS | minimax-m2.7:cloud |

See individual skill files in `skills/` for full configuration.

---

## Memory

| Layer | Access | Persistence | Purpose |
|---|---|---|---|
| **Session** | Frank + Jarbas | Conversation lifetime | Current context |
| **Frank-Personal** | Frank only | Permanent | Strategy, credentials, grant drafts |
| **Family-Shared** | Frank + Jarbas | Permanent | Calendar, kids, budgets, shared notes |
| **Project-Tagged** | Frank (rw), Jarbas (r) | 30-day TTL | Per-task context, DeepSeek cache |

---

## Budget

### Monthly Allocation ($50 Hard Cap)

| Component | Cost | Share |
|---|---|---|
| Ollama Pro (flat) | $20 | 40% |
| DeepSeek API | $3–$12 | 20% |
| Gemini 2.5 Pro | $2–$6 | 10% |
| Hosting (Docker/VPS) | $5–$8 | 15% |
| Buffer | $2–$5 | 10% |
| **Target range** | **$32–$46** | |

---

## Getting Started

```bash
# Clone
git clone https://github.com/frankomatic5000/frankomaticlaw.git
cd frankomaticlaw

# Configure
cp .env.example .env
# Edit .env with your API keys

# Run
docker pull openclaw/openclaw:latest
docker run -d \
  --name frankomaticlaw \
  -p 18789:18789 \
  -v $(pwd):/app/workspace \
  --env-file .env \
  openclaw/openclaw:latest
```

See [docs/SETUP.md](docs/SETUP.md) for the full step-by-step guide.
See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for system diagrams.

---

## File Structure

```
frankomaticlaw/
├── SOUL.md                      # Agent identities & personality
├── README.md                    # This file
├── .clawopenrc                  # OpenClaw runtime config
├── .env.example                 # Environment variable template
├── config/
│   ├── agents.yaml              # Agent definitions & permissions
│   ├── router.yaml              # Inference router tiers & guards
│   ├── memory.yaml              # Memory layer configuration
│   └── budget.yaml              # Budget thresholds & alerts
├── skills/
│   ├── taskmaster.skill.yaml    # Central task backbone
│   ├── socialclaw.skill.yaml    # Social media intelligence
│   ├── mailmate.skill.yaml      # Email triage & sending
│   ├── bizguard.skill.yaml      # QuickBooks, grants, tax
│   └── codeforge.skill.yaml     # GitHub & code implementation
├── memory/
│   ├── frank-personal.md        # Rod's private notes
│   ├── family-shared.md         # Shared family context
│   └── projects/                # Per-task context files
└── docs/
    ├── ARCHITECTURE.md          # System architecture & diagrams
    └── SETUP.md                 # Full setup guide
```

---

## License

MIT — do whatever you want, just don't blame Rod when it gets sarcastic.

---

<p align="center">
  Built with 🧠 by Rod & Karine · Powered by <a href="https://github.com/ollama/ollama">OpenClaw</a> · GrowBiz Media<br>
  <em>"A world where your origin is your advantage, not your obstacle."</em>
</p>