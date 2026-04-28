# SKILL.md - grant-search

## Name
grant-search

## Description
Search for grants, funding opportunities, and financial aid for solo entrepreneurs, women-owned businesses, and minority-owned businesses. Focus on federal, state, and private grants applicable to GrowBiz Media and Imigrou.

## Search Categories

### Federal Grants
- SBA (Small Business Administration)
- USDA grants
- Minority Business Development Agency (MBDA)
- Women-Owned Small Business (WOSB) programs

### State/Local Grants
- NJEDA (New Jersey Economic Development Authority)
- State-specific minority/women business programs
- Local economic development grants

### Private/Foundation Grants
- IFundWomen
- Amber Grant
- FedEx Small Business Grant
- Comcast RISE
- NAACP grants
- NAWBO (National Association of Women Business Owners)

### Industry-Specific
- Media/content creation grants
- Tech/AI grants
- Immigrant entrepreneur programs

## Eligibility Criteria

Focus on grants where Karine/GrowBiz qualifies:
- ✅ Woman-owned business
- ✅ Immigrant/minority-owned
- ✅ Media/content creation
- ✅ Technology/AI focus
- ✅ New Jersey location
- ✅ Small business (< 50 employees)

## Search Parameters

| Field | Required | Notes |
|-------|----------|-------|
| grant_type | No | federal/state/private/industry |
| deadline | No | upcoming only? |
| amount_min | No | minimum grant amount |
| amount_max | No | maximum grant amount |
| location | No | NJ-specific? |
| women_owned | No | WOSB certified? |
| minority_owned | No | minority business? |

## Output Format

```
🎯 GRANT OPPORTUNITY

Name: [Grant Name]
Funder: [Organization]
Amount: $[Amount]
Deadline: [Date]
Eligibility: [Criteria]
Application: [Link/Process]
Fit Score: [1-10] — How well it matches GrowBiz

Action Items:
- [ ] Check eligibility requirements
- [ ] Gather documents
- [ ] Draft application
- [ ] Submit
```

## Triggers

- "Search for grants"
- "Find funding opportunities"
- "Women business grants"
- "Minority entrepreneur grants"
- "NJEDA grants"
- "Federal grants for media"

## Data Sources

- grants.gov
- SBA.gov
- NJEDA.com
- IFundWomen.com
- Foundation Directory Online
- Local NJ business resources

## Preferred Model

kimi-k2.5:cloud (fast web search)

---

*Find funding to grow GrowBiz Media.*
