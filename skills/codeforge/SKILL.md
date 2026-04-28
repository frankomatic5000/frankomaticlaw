# SKILL.md - CodeForge

## Name
codeforge

## Description
Engineering operations for GrowBiz Media's tech products: ClipIQ (content automation), Vaptlux (AI video editing), GrowBiz Magazine (Next.js + Sanity), GrowBiz Services (SEO platform), DoodleType (digital products), and ZecaOS (AI assistant). Plus this very repo — frankomaticlaw.

## When to Use
- Syncing with product repos
- Generating code
- Reviewing code
- Creating PRs (requires approval)
- Merging PRs (requires approval)
- Creating/updating issues
- Deploying (requires approval)
- Explaining code
- Refactoring
- Checking pipeline status
- Checking content engine status

## Inputs
| Name | Type | Required | Options |
|------|------|----------|---------|
| action | enum | yes | sync, generate, review, pr_create, pr_merge, issue_create, issue_update, deploy, explain, refactor, pipeline_status, content_engine |
| product | enum | yes | clipiq, vaptlux, magazine, services-platform, doodletype, zecaos, frank-jarbas, other |
| repo | string | yes | Format: owner/repo |
| branch | string | no | default: main |
| file_path | string | no | - |
| code_content | string | no | - |
| language | enum | no | python, typescript, javascript, yaml, markdown, go, rust, nextjs, sanity-groq, other |
| commit_message | string | no | - |
| issue_body | string | no | - |

## Outputs
Result with: action_completed, generated_code, review_feedback, pr_url, issue_url, deploy_status, pipeline_health, approval_status

## Product Context
- **clipiq:** Next.js 14, content pipeline, Teams integration
- **vaptlux:** AI video analysis, multi-camera processing
- **magazine:** Next.js 14 + Sanity CMS + Vercel
- **services-platform:** SEO tools, client dashboards
- **zecaos:** AI assistant, Microsoft ecosystem

## Access Control
- **Frank:** All actions
- **Jarbas:** sync, pipeline_status, content_engine only

## Triggers
- "code"
- "github"
- "deploy"
- "clipiq pipeline"
- "magazine content"
- "vaptlux"
- "engineering status"

## Permissions
- github_api_read
- github_api_write
- vercel_api
- sanity_api
- memory_read
- memory_write

## Preferred Model
ollama/qwen3-coder-next:cloud
## Escalation Model
deepseek-reasoner (for complex refactoring)
## Note
Uses Qwen3 Coder Next via Ollama Cloud for code tasks. DeepSeek for reasoning-heavy refactoring.
