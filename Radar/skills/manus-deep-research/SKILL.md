# SKILL.md - manus-deep-research

## Name
manus-deep-research

## Description
Comprehensive Instagram channel analysis using Manus AI's deep research capabilities. Performs detailed evaluation of performance metrics, content strategy, audience engagement, and technical optimization. Delivers actionable recommendations for growth and improvement.

## Capabilities

- **Deep Research:** Gathers and synthesizes information from Instagram channels
- **Data Analysis:** Processes Instagram metrics and engagement data
- **Technical Writing:** Generates structured, data-driven reports with clear insights
- **Competitor Benchmarking:** Comparative analysis against specified competitors

## Input Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| instagram_handle | string | Instagram handle (e.g., @imigrou) to analyze | Yes |
| competitor_handle | string | Competitor handle for comparative analysis | No |

## Output

Comprehensive Markdown report (`instagram_analysis_report_[handle].md`) containing:

### 1. Executive Summary
- Overview of key findings and top recommendations

### 2. Profile Optimization
- **Bio Analysis:** Clarity, effectiveness, and call-to-action (CTA)
- **Branding Consistency:** Profile picture, highlights, visual identity
- **Link-in-Bio Strategy:** Effectiveness of external links and traffic generation

### 3. Content Strategy Analysis
- **Top-Performing Content:** Identification of successful posts (Reels, static, carousels)
- **Engagement Metrics:** Detailed breakdown of likes, comments, shares, saves
- **Posting Schedule:** Analysis of frequency and optimal timing
- **Visual & Voice:** Evaluation of aesthetic, brand voice, content quality

### 4. Audience & Community Engagement
- **Follower Growth:** Trends, demographics, growth patterns
- **Audience Sentiment:** Analysis of comments and interactions
- **Community Interaction:** Brand responsiveness and engagement

### 5. Technical & Growth Factors
- **Hashtag Performance:** Effectiveness of hashtag usage and discovery
- **Keyword Optimization:** Presence and impact of keywords in captions
- **Competitor Benchmarking** (if competitor_handle provided):
  - Comparison of key metrics and strategies

### 6. Actionable Recommendations
- **SWOT Analysis:** Strengths, Weaknesses, Opportunities, Threats
- **Quick Wins:** Immediate, high-impact suggestions
- **Long-Term Strategy:** Sustainable recommendations for growth

## API Configuration

**Base URL:** `https://api.manus.im/v1`  
**Auth Header:** `API_KEY: {your-manus-key}`  
**Method:** Async task creation + polling  
**SDK:** OpenAI Python SDK 1.100.2+

## Workflow

1. **Input Validation:** Verify instagram_handle is valid
2. **Data Collection:** Access Instagram data via Manus research
3. **Metric Calculation:** Compute engagement rates, growth percentages
4. **Content Categorization:** Classify posts by type and analyze performance
5. **Qualitative Analysis:** Evaluate bio, aesthetic, brand voice, community
6. **Report Generation:** Compile findings into structured Markdown
7. **Recommendation Formulation:** Develop actionable insights

## Expected Runtime

| Task Complexity | Time |
|----------------|------|
| Simple analysis | 5-15 min |
| Medium research | 30-60 min |
| Deep analysis | 2-24 hours |
| Complex multi-step | 24-48 hours |

## Cost Tracking

- **Credits:** Displayed in `metadata.credit_usage`
- **Typical:** 20-100 credits per comprehensive analysis
- **Monitor:** Check task_url in Manus dashboard

## Triggers

- "Deep Instagram analysis of @[handle]"
- "Research Instagram channel @[handle] with Manus"
- "Analyze @[handle] and competitor @[competitor]"
- "Manus investigation into Instagram strategy for @[handle]"

## Output Format

Returns structured analysis with:
- Executive summary
- Profile optimization insights
- Content strategy evaluation
- Audience engagement metrics
- Technical factors assessment
- Competitor comparison (if requested)
- Actionable SWOT analysis
- Quick wins and long-term recommendations

## Integration with Radar

Radar spawns this skill → Manus works asynchronously → Results posted to Teams → Report saved locally

## Error Handling

- **Timeout:** After 48 hours, report failure
- **Invalid handle:** Validate before submission
- **Rate limits:** Respect 429 responses, exponential backoff
- **Error status:** Log and retry with simplified query

## Environment Variables

```bash
MANUS_API_KEY="sk-..."
TEAMS_WEBHOOK_URL="https://imigrou.webhook.office.com/..."
```

## Files

- `scripts/manus_research.py` - Python handler
- `scripts/submit_manus_task.sh` - Submission wrapper
- `logs/` - Execution logs
- `instagram_analysis_report_*.md` - Generated reports

## Preferred Model

Uses Manus API directly (manus-1.6 agent profile)

---

*Comprehensive Instagram analysis when you need deep strategic insights.*
