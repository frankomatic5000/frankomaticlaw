# 🏗️ Architecture — Frank + Jarbas Agentic System

> GrowBiz Media · OpenClaw Platform

---

## High-Level System Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        OPENCLAW GATEWAY (Control Plane)                     │
│                     TCP :18789 · Self-hosted · Docker                       │
│                                                                             │
│  ┌──────────────┐          ┌────────��─────────────────────────────────────┐ │
│  │   CHANNELS   │          │           INFERENCE ROUTER                   │ │
│  │              │          │     (First call on EVERY request)            │ │
│  │  ┌────────┐  │  Input   │                                              │ │
│  │  │Discord │──┼──────────▶  1. Classify: L1–L4 complexity              │ │
│  │  │(Frank) │  │          │  2. Score: confidence 0.0–1.0               │ │
│  │  └────────┘  │          │  3. Route: Tier 1 → 2 → 3 (cheap-first)    │ │
│  │  ┌────────┐  │          │  4. Guard: budget, latency, cache           │ │
│  │  │WhatsApp│──┼──────────▶                                              │ │
│  │  │(Jarbas)│  │  🎤 Voice│  ┌─────────────────────────────────────────┐ │ │
│  │  └────────┘  │  First!  │  │         BUDGET GUARD                    │ │ │
│  └──────────────┘          │  │  $50/mo cap · Weekly check              │ │ │
│                            │  │  Pause at $35 · Abort at $48            │ │ │
│                            │  └─────────────────────────────────────────┘ │ │
│                            └──────────┬───────────┬───────────┬──────────┘ │
│                                       │           │           │            │
│                                       ▼           ▼           ▼            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     MODEL TIERS (Escalation Chain)                  │   │
│  │                                                                     │   │
│  │  TIER 1 — Ollama Pro Cloud ($20/mo flat) — 80–85% of calls         │   │
│  │  ┌─────────────────┬──────────────────┬──────────────────────┐     │   │
│  │  │ kimi-k2.5:cloud │ minimax-m2.7     │ qwen3.5:cloud        │     │   │
│  │  │ General/Family  │ :cloud           │ Content/Grants/       │     │   │
│  │  │ Vision/Social   │ Coding/CodeForge │ Email/Multimodal      │     │   │
│  │  │ DEFAULT FALLBACK│ Architecture     │                       │     │   │
│  │  └─────────────────┴──────────────────┴──────────────────────┘     │   │
│  │                          │ escalate if conf < 0.75                  │   │
│  │                          ▼                                          │   │
│  │  TIER 2 — DeepSeek API (~$3–12/mo) — 10–15% of calls              │   │
│  │  ┌──────────────────────────────────────────────────────────┐      │   │
│  │  │ deepseek-chat (normal)  ·  deepseek-reasoner (thinking)  │      │   │
│  │  │ MANDATORY cache: "Reuse task #ID context: {summary}"     │      │   │
│  │  └──────────────────────────────────────────────────────────┘      │   │
│  │                          │ escalate if needs external info          │   │
│  │                          ▼                                          │   │
│  │  TIER 3 — Gemini 2.5 Pro (~$2–6/mo) — <5% of calls                │   │
│  │  ┌──────────────────────────────────────────────────────────┐      │   │
│  │  │ Vision/search failures only · Hard cap $8/week           │      │   │
│  │  └──────────────────────────────────────────────────────────┘      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                       │                                    │
│                                       ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                          SKILLS LAYER                               │   │
│  │  ┌───────────┐ ┌───────────┐ ┌────────┐ ┌────────┐ ┌───────────┐  │   │
│  │  │ TaskMaster│ │SocialClaw │ │MailMate│ │BizGuard│ │ CodeForge │  │   │
│  │  └───────────┘ └───────────┘ └────────┘ └────────┘ └───────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                       │                                    │
│                                       ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         MEMORY LAYERS                               │   │
│  │  Session · Frank-Personal · Family-Shared · Project-Tagged          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Portfolio → Skill Mapping

```
┌─────────────────────────────────────────────────────────────────────┐
│                    GROWBIZ MEDIA PORTFOLIO                           │
│                                                                     │
│  CONTENT LAYER (Karine-led)          TECH LAYER (Rod-led)           │
│  ┌─────────────┐ ┌──────────────┐   ┌───────────┐ ┌─────────────┐  │
│  │ 🎙️ Imigrou  │ │ 🎬 Studios   │   │ ⚡ ClipIQ  │ │ 🎬 Vaptlux  │  │
│  │ Diaspora    │ │ Production   │   │ Content   │ │ Multi-cam   │  │
│  │ media       │ │ company      │   │ automation│ │ AI editing  │  │
│  └──────┬──────┘ └──────┬───────┘   └─────┬─────┘ └──────┬──────┘  │
│         │               │                 │              │          │
│         └───────┬───────┘                 └──────┬───────┘          │
│                 │                                │                  │
│                 ▼                                ▼                  │
│  ┌──────────────────────┐          ┌──────────────────────────┐     │
│  │ 📰 GrowBiz Magazine  │          │ 📍 GrowBiz Services      │     │
│  │ Digital publication   │          │ AI-powered local SEO     │     │
│  │ Next.js + Sanity      │          │ $297–$997/mo             │     │
│  └──────────────────────┘          └──────────────────────────┘     │
│                                                                     │
│  ┌──────────────┐ ┌─────────────────────────────────────────────┐   │
│  │ 🖊️ DoodleType│ │ 🤖 ZecaOS — AI assistant (Microsoft-aligned)│   │
│  │ Creative brand│ └─────────────────────────────────────────────┘   │
│  └──────────────┘                                                   │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│              FRANK + JARBAS AGENTIC LAYER                           │
│                                                                     │
│  Skills route by brand context:                                     │
│  • SocialClaw → Imigrou (pt-BR), GrowBiz, DoodleType, Services     │
│  • MailMate → Studios collabs, Services outreach, grant follow-ups  │
│  • BizGuard → Services MRR, Studios projects, grants, equipment    │
│  • CodeForge → ClipIQ, Vaptlux, Magazine, Services platform, ZecaOS│
│  • TaskMaster → Everything, tagged by brand                         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Brand → Skill Matrix

| Brand | SocialClaw | MailMate | BizGuard | CodeForge | Primary Owner |
|---|---|---|---|---|---|
| 🎙️ Imigrou | ✅ pt-BR content | ✅ Collabs | ✅ Revenue | — | Karine |
| 🎬 Studios | ✅ BTS content | ✅ Client comms | ✅ Projects + grants | — | Karine |
| 📰 Magazine | ✅ Article promos | ✅ Contributors | ✅ Revenue | ✅ Next.js + Sanity | Both |
| ⚡ ClipIQ | ✅ Repurpose clips | — | ✅ Dev costs | ✅ Pipeline + code | Rod |
| 🎬 Vaptlux | — | — | ✅ Dev costs | ✅ AI video code | Rod |
| 📍 Services | ✅ B2B social | ✅ Sales outreach | ✅ MRR tracking | ✅ SEO platform | Rod |
| 🖊️ DoodleType | ✅ Creative posts | — | ✅ Revenue | ✅ Digital products | Both |
| 🤖 ZecaOS | — | ✅ Microsoft outreach | ✅ Fund tracking | ✅ Platform code | Rod |

---

## Approval Matrix

| Action | Frank (Discord) | Karine via Jarbas (WhatsApp) |
|---|---|---|
| Personal reminders, calendar, groceries | ✅ Auto | ✅ Karine approves |
| Read / analyze / draft | ✅ Auto | ✅ Auto |
| Send email | ✅ Approves | ✅ Karine approves |
| Publish social post | ✅ Approves | ✅ Karine approves |
| QuickBooks (invoices, expenses, balances) | ✅ Approves | ✅ Karine approves |
| QuickBooks reconciliation / writes >$500 | ✅ Approves | 🔒 Forward to Frank |
| Grant submissions | ✅ Approves | 🔒 Forward to Frank |