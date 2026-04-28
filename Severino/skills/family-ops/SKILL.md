---
name: family-ops
description: Family operations for Severino — travel, birthdays, household budget, canonical memory writes
metadata:
  {
    "openclaw":
      {
        "emoji": "🏠",
        "requires": { "tools": ["read", "write", "web_search", "sessions_send"] },
        "primaryEnv": null
      }
  }
---

# family-ops

The heart of family operations. Travel planning, birthday tracking, household budget, and the family's memory keeper.

## When to Use

- Plan family trip
- Track birthdays and gifts
- Log family memory (canonical writes)
- Check household budget
- Coordinate between Rod and Karine

## When NOT to Use

- Business travel (FrankCFO)
- QuickBooks (FrankCFO)
- Business expenses (FrankCFO)
- Code (RodZilla)

## Travel Planning

**Process:**
1. Capture intent (destination, dates, reason)
2. Research (flights, hotels, activities)
3. Build itinerary options
4. Present to Rod + Karine for approval
5. Book AFTER both approve (not before!)
6. Update calendar
7. Write memory

**Research includes:**
- Flight options (price, timing, airline)
- Hotels (location, reviews, family-friendly)
- Activities (kid-friendly, Karine's interests)
- Restaurants (gastronomy focus)
- Backup plans (rain days, delays)

**Output format:**
```markdown
# Brazil Trip — June 2026

## Flights
• Option A: $X,XXX (preferred)
• Option B: $X,XXX (backup)

## Hotels
• Option A: [hotel], [neighborhood], $XXX/night
• Option B: [hotel], [neighborhood], $XXX/night

## Itinerary
Day 1: Arrival, check-in, rest
Day 2: [activity], [restaurant]
...

## Budget
• Flights: $X,XXX
• Hotels: $X,XXX
• Activities: $XXX
• Food: $XXX
• Total: $X,XXX

⚠️ Requires approval: Rod + Karine
```

## Birthday Tracking

**Highest Priority:**
- Karine: March 27 (book early!)
- Antonio: [date]
- Rebecca: [date]
- Rod: [date]

**Lead Times:**
- 30 days: Start planning gifts, check travel
- 7 days: Finalize plans, confirm reservations
- Day before: Reminder + last-minute details
- Day of: Celebrate

**Gift Ideas Context:**
- Karine: Quality over quantity, experiences, books, art
- Rod: Tech, productivity tools, good food/wine
- Antonio: Games, coding, sports gear
- Rebecca: Art supplies, music, creative activities

**Logging:**
- What was gifted
- Reaction
- Next year ideas

## Household Budget

**Separate from FrankCFO's business finances:**

| Category | Monthly |
|----------|---------|
| Groceries | $XXX |
| Kids activities | $XXX |
| Household (maintenance, supplies) | $XXX |
| Family travel fund | $XXX |
| Personal savings | $XXX |
| Gifts/celebrations | $XXX |

**Rules:**
- Track expenses (manual entry or bank import)
- Monthly review with Rod and Karine
- Alert if over 80% of category
- Carry over unused funds

## Family Memory (Canonical Writes)

Severino is the **source of truth** for family state.

**After EVERY family task, write to `family-shared.md`:**

```markdown
## 2026-03-20: Brazil trip approved

- Destination: Brazil
- Dates: June 15-30, 2026
- Approved by: Rod + Karine
- Flights booked: LATAM, $2,400
- Hotels: [list]
- Kids excited: Yes

## 2026-03-18: Rebecca's birthday party

- Date: March 27, 2026
- Theme: Art studio
- Guests: [list]
- Gifts received: [list]
- Fun had: Maximum

## 2026-03-15: Antonio Jiu Jitsu belt test

- Result: Passed! Blue belt
- Mood: Proud
- Next: Keep training
```

**Write rules:**
- Timestamp every entry
- Include decision rationale
- Note who was involved
- Update status changes

**Others read from here:**
- Frank can read (orchestrator visibility)
- Jarbas relays to Karine
- No one else writes

## Confirmation Protocol

**Before booking anything >$100:**

```
Proposed: [action]
Cost: $XXX
Impact: [what happens]

Rod: [Approve] [Decline] [Modify]
Karine: [Approve] [Decline] [Modify]

Both must approve to proceed.
```

**Example:**
```
Proposed: Book flights to Brazil
Cost: $2,400
Impact: Non-refundable

Rod: ✅ Approved
Karine: ✅ Approved

→ Proceeding with booking
```

## Quick Commands

```
Plan a trip to [destination] in [month]
```
→ Research options, present for approval

```
When is [person]'s birthday?
```
→ Date + days remaining + gift ideas

```
Log: [family event]
```
→ Write to family-shared.md

```
What's our household budget?
```
→ Current status + categories

```
Confirm: [decision] with both
```
→ Queue for Rod + Karine approval

## Language

- Input: PT or EN (match sender)
- Output: Same language as query
- family-shared.md: EN (Rod reads), PT summaries for Karine

## Tool Usage

```javascript
// Research travel
const flights = await tools.web_search('flights to Brazil June 2026');

// Write memory
await tools.write('~/.openclaw/workspace-severino/memory/family-shared.md', entry);

// Query budget
const budget = await tools.read('~/.openclaw/workspace-severino/budget/current.json');

// Request approval
await tools.sessions_send({
  sessionKey: 'main',
  message: 'Approval needed: Brazil trip'
});
```

## Files

- Memory: `~/.openclaw/workspace-severino/memory/family-shared.md`
- Travel plans: `~/.openclaw/workspace-severino/travel/`
- Budget: `~/.openclaw/workspace-severino/budget/`
- Birthdays: `~/.openclaw/workspace-severino/birthdays/`

## ARP Integration

**Jarbas → Severino** (only permitted specialist-to-specialist path):
```javascript
await tools.sessions_spawn({
  agentId: 'severino',
  task: 'Family task from Karine: [description]',
  model: 'ollama/kimi-k2.5:cloud'
});
```

**Rod → Severino** (via Discord #familia):
Direct messages to Severino session.

Returns:
- STATUS: complete with memory written
- STATUS: needs-approval for spend
- Confirmation back to requester
