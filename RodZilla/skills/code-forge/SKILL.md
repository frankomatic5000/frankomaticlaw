---
name: code-forge
description: Core engineering skill for RodZilla — generate, review, refactor code with product context
metadata:
  {
    "openclaw":
      {
        "emoji": "⚡",
        "requires": { "tools": ["exec", "read", "write", "edit", "sessions_spawn"], "skills": ["github"] },
        "primaryEnv": null
      }
  }
---

# code-forge

The engineering brain for GrowBiz Media. Code generation, review, and refactoring with deep product context.

## When to Use

- Generate new feature code
- Review existing code
- Refactor for clarity
- Debug and fix bugs
- Explain code (junior-readable)

## When NOT to Use

- Simple one-liner fixes (use edit tool directly)
- Production deployment (use code-ship)
- Git operations (use git-ops)
- Architecture decisions (escalate to deepseek-r1)

## Product Context

**ClipIQ:** AI content automation — Next.js, Sanity, Vercel
**Vaptlux:** Multi-camera video editing — Python, FFmpeg, Next.js
**GrowBiz Magazine:** Next.js 14, Sanity CMS, Vercel
**ZecaOS:** AI assistant platform — Microsoft-aligned
**GrowBiz Services:** SEO platform — Next.js, analytics APIs
**DoodleType:** Creative brand — Next.js, design systems

**Stack:**
- Next.js 14 + App Router
- TypeScript (strict)
- Tailwind CSS
- Sanity CMS
- Vercel deployment
- Node.js/Express for APIs

## Code Rules

**Rod's Law:**
> "If a junior developer can't read it, I rewrite it."

**Practices:**
- Clear variable names (no `x`, `data`, `temp`)
- Comments explain WHY, not WHAT
- Functions do ONE thing
- Early returns over nested ifs
- Async/await over callbacks
- Error handling ALWAYS

## Workflow

```
Request → Context gathering → Code → Review → Output
```

### 1. Context Gathering

Before coding, check:
- Existing code in repo
- Product requirements
- Similar implementations
- Style guide

### 2. Code Generation

Output:
- File path
- Complete code
- Explanation of approach
- Trade-offs considered

### 3. Review (if requested)

Check for:
- Security issues (input validation, XSS, injection)
- Performance (N+1 queries, unnecessary re-renders)
- Maintainability (complexity, duplication)
- Tests (are they needed?)

## Model Escalation

**Default:** kimi-k2.5:cloud (free, fast)

**Escalate to deepseek-r1 when:**
- Architecture redesign
- Security-critical code
- Complex algorithm
- Race conditions
- Performance optimization

## Example

**Request:** "Build a Sanity schema for Magazine articles with SEO fields"

**Output:**
```typescript
// schemas/article.ts
export default {
  name: 'article',
  title: 'Article',
  type: 'document',
  fields: [
    {
      name: 'title',
      title: 'Title',
      type: 'string',
      validation: (Rule) => Rule.required().max(70)
    },
    {
      name: 'slug',
      title: 'Slug',
      type: 'slug',
      options: { source: 'title' },
      validation: (Rule) => Rule.required()
    },
    {
      name: 'seo',
      title: 'SEO',
      type: 'seoFields' // reference to shared SEO schema
    },
    // ... more fields
  ]
}
```

**Explanation:** "Sanity schema with strict validation. SEO fields extracted to reusable schema. Slug auto-generated from title."

## Security Checklist

- [ ] Input validation on all APIs
- [ ] XSS protection (Sanity handles this)
- [ ] No secrets in code
- [ ] SQL injection prevention (parameterized queries)
- [ ] Auth checks on protected routes

## Testing Strategy

**Unit tests:**
- Pure functions
- Business logic

**Integration tests:**
- API endpoints
- Database queries

**E2E tests:**
- Critical user flows
- Smoke tests

## Documentation

Every significant code contribution gets:
- README update (if needed)
- Inline comments for complex logic
- CHANGELOG entry (if versioned)

## Tool Usage

```javascript
// Read existing code
const existing = await tools.read('/path/to/file.ts');

// Generate new file
await tools.write('/path/to/new/file.ts', generatedCode);

// Edit existing
await tools.edit('/path/to/file.ts', oldCode, newCode);

// Run tests
await tools.exec({ command: 'npm test' });

// Lint
await tools.exec({ command: 'npm run lint' });
```

## Integration

**With git-ops:**
- code-forge generates
- git-ops commits and PRs

**With code-ship:**
- code-forge develops
- code-ship deploys (after approval)

**With security-guard:**
- Security scan runs on generated code
- Blocks if CRITICAL findings

## Files

- Code: Respective product repos
- Snippets: `~/.openclaw/workspace-rodzilla/snippets/`
- Templates: `~/.openclaw/workspace-rodzilla/templates/`

## ARP Integration

Called by Frank via sessions_spawn:
```javascript
await tools.sessions_spawn({
  agentId: 'rodzilla',
  task: 'Build feature X',
  model: 'ollama/kimi-k2.5:cloud' // or deepseek-r1 for complex
});
```

Returns:
- STATUS: complete with code/files
- STATUS: partial if needs more work
- STATUS: escalate if needs architecture
