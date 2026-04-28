# SKILL.md - TaskMaster

## Name
taskmaster

## Description
Central task backbone for GrowBiz Media operations. Tracks tasks across all portfolio brands — Imigrou, Studios, Magazine, ClipIQ, Vaptlux, Services, DoodleType, ZecaOS. Every action flows through TaskMaster with brand-aware routing.

## When to Use
- Creating new tasks for any brand
- Updating task status or priority
- Listing pending tasks
- Getting task details
- Prioritizing tasks by revenue impact

## Inputs
| Name | Type | Required | Options |
|------|------|----------|---------|
| action | enum | yes | create, update, close, list, get, prioritize |
| title | string | yes | - |
| owner | enum | no | rod, karine, both (default: rod) |
| brand | enum | yes | imigrou, studios, magazine, clipiq, vaptlux, services, doodletype, zecaos, growbiz-general, family |
| domain | enum | no | content, production, code, seo, editorial, finance, grants, social, client-work, family, general |
| urgency | enum | no | low, medium, high, critical (default: medium) |
| parent_task_id | string | no | - |
| revenue_impact | enum | no | none, indirect, direct (default: none) |

## Outputs
Task object with: id, owner, brand, status, domain, model_tier, confidence, approval_needed, revenue_impact, summary, timestamps, parent_id

## Logic
- Auto-increment IDs: TASK-{counter:04d}
- Karine's tasks (imigrou, studios, family): auto-approved
- Client-work in services brand: auto-set to high urgency
- Direct revenue impact: flagged as 💰 Revenue task
- On create: notify owner via channel + tag to brand project memory

## Access Control
- **Frank:** All actions (create, update, close, list, get, prioritize)
- **Jarbas:** All actions (create, update, close, list, get, prioritize)

## Triggers
- "create task"
- "new task"
- "task for imigrou"
- "task for clipiq"
- "what's pending"

## Permissions
- memory_read
- memory_write
- notify_channels

## Preferred Model
any (router decides based on complexity)
