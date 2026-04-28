# GrowBiz GitHub Organization

## Owner
**github.com/frankomatic5000** (Rod Rezende)

## Repositories

### Active Projects
| Repo | Purpose | Lead Agent |
|------|---------|------------|
| **frankomaticlaw** | Corporate OS — Agent configs, ARP protocols, system docs | Frank (CEO) |
| **clipiq** | MyClipIQ — Prompt-based video editor SaaS | RodZilla (CTO) |
| **global-visibility-marketplace** | GMV — SaaS marketplace for content creators | RodZilla (CTO) |
| **growbizmagazine** | GrowBiz Magazine — Next.js + Sanity stack | RodZilla (CTO) |
| **growbiz.media** | Main portfolio site | DaVinci (CMO) |
| **zecaos** | Technical pipelines and automation | RodZilla (CTO) |

### Brand Assets
| Repo | Purpose | Lead Agent |
|------|---------|------------|
| **pessoasglobais** | Imigrou / Pessoas Globais brand assets | Jarbas (CoS) |
| **pessoasglobais-design** | Design system and UI kit | DaVinci (CMO) |
| **pessoas-globais-collective** | Diaspora content collective | Jarbas (CoS) |

### Legacy / Archive
| Repo | Status |
|------|--------|
| **doodletype-website** | Legacy project |
| **growbizmagazinecom** | Redirect to growbizmagazine |

## Git Configuration
```bash
# Global git config
git config --global user.name "Rod Rezende"
git config --global user.email "rod@growbiz.media"
git config --global init.defaultBranch main

# Per-repo remotes
# All repos use https://github.com/frankomatic5000/<repo>.git
```

## Branch Protection (Enforced by X9)
- `main` branch: Requires PR review
- All pushes: X9 shadow audit for secrets
- No direct pushes to `main` from RodZilla

## SDLC Flow
1. **Develop:** Feature branch on RodZilla workspace
2. **Audit:** X9 scans diff via `git diff origin/main...HEAD`
3. **Push:** `git push origin feature/name`
4. **Review:** PR created, Jarbas/DaVinci review for cultural/UI changes
5. **Deploy:** Vercel preview → Production on merge

## Security Rules
- No hardcoded secrets in any repo
- Use GitHub Secrets or Azure Key Vault for API keys
- `.env` files in `.gitignore` (enforced by X9 pre-commit hook)
- All repos must have `LICENSE` (MIT) and `README.md`
