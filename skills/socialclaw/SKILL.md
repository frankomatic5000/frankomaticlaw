# SKILL.md - SocialClaw

## Name
socialclaw

## Description
Multi-brand social media intelligence for the entire GrowBiz Media portfolio. Scrapes trends, analyzes engagement, drafts brand-aware content, and publishes across platforms. Knows that Imigrou is pt-BR diaspora content, GrowBiz Services is professional SEO outreach, DoodleType is creative/visual, and GrowBiz general is thought-leadership. Integrates with ClipIQ output for short-form content scheduling.

## When to Use
- Scraping social trends for any brand
- Analyzing content performance
- Drafting social media posts
- Scheduling content
- Checking engagement metrics
- Monitoring competitors
- Researching hashtags
- Repurposing ClipIQ clips for social

## Inputs
| Name | Type | Required | Options |
|------|------|----------|---------|
| action | enum | yes | scrape, analyze, draft, publish, schedule, metrics, competitor_watch, hashtag_research, repurpose |
| brand | enum | yes | imigrou, growbiz-media, growbiz-services, doodletype, personal-rod, personal-karine |
| platform | enum | no | youtube, instagram, tiktok, x-twitter, linkedin, threads, all (default: all) |
| content | string | no | - |
| media | file | no | - |
| tone | enum | no | professional, casual, inspirational, sarcastic, diaspora-authentic, seo-focused (default: casual) |
| language | enum | no | en, pt-br, bilingual (default: en) |
| clipiq_source | string | no | ClipIQ clip ID to repurpose |

## Outputs
Result with: action_completed, content_draft, analysis_summary, engagement_metrics, competitor_insights, hashtags, approval_status, scheduled_at

## Voice Rules by Brand
- **imigrou:** Karine's voice. Warm, authentic, diaspora-aware. pt-BR primary. NEVER sound corporate.
- **growbiz-media:** Rod + Karine together. Ambitious but accessible.
- **growbiz-services:** Professional but human. SEO-aware. Speak to skeptical small business owners.
- **doodletype:** Creative, playful, visual-forward.

## Access Control
- **Frank:** All actions
- **Jarbas:** All actions (Karine is the content queen)

## Triggers
- "post"
- "social"
- "imigrou post"
- "schedule content"
- "engagement"
- "competitor"
- "repurpose clip"

## Permissions
- internet_access
- platform_api_write
- vision_processing
- memory_read
- clipiq_api_read

## Preferred Model
kimi-k2.5:cloud
