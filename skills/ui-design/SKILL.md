# SKILL.md - ui-design

## Name
ui-design

## Description
UI/UX design and frontend development for GrowBiz Media projects. Handles design systems, component architecture, user flows, and visual polish. Optimized for Qwen 3.5's strengths in design reasoning and component thinking.

## When to Use
- Designing new page layouts
- Component architecture decisions
- Design system updates
- UX flow improvements
- Accessibility audits
- Mobile responsiveness issues
- Visual polish and refinements
- Design-to-code handoffs

## Preferred Model
**qwen3.5:cloud** — Optimized for design reasoning, component architecture, and visual problem-solving

## Model Routing
- **Tier 1 (UI/UX tasks):** qwen3.5:cloud
- **Tier 2 (Complex logic):** deepseek-chat-v3
- **Fallback:** kimi-k2.5:cloud

## Inputs
| Name | Type | Required | Options |
|------|------|----------|---------|
| action | enum | yes | design_review, component_arch, layout_design, accessibility_audit, mobile_optim, design_system |
| project | enum | yes | growbiz.media, doodletype, clipiq, vaptlux, imigrou, growbizmagazine |
| platform | enum | no | web, mobile, app |
| framework | enum | no | nextjs, react, vue, vanilla |

## Design Principles
1. **Mobile-first** — Design for thumb, scale up
2. **Accessibility** — WCAG 2.1 AA minimum
3. **Performance** — Fast loads, lazy images
4. **Brand-consistent** — Match GrowBiz aesthetic
5. **Component-driven** — Reusable, maintainable

## Outputs
- Design recommendations
- Component architecture
- CSS/Tailwind suggestions
- Accessibility fixes
- Mobile breakpoints

## Access Control
- **RodZilla:** Full access (implements designs)
- **Frank:** Can request reviews
- **FrankCMO:** Can request landing page designs

## Triggers
- "design review"
- "component"
- "layout"
- "mobile"
- "responsive"
- "UX"
- "UI"
- "accessibility"

## Permissions
- memory_read
- memory_write
- file_read (design assets)

## Example
```
User: "Review the hero section on growbiz.media"
Skill: ui-design
Model: qwen3.5:cloud
Output: Design recommendations with specific CSS fixes
```
