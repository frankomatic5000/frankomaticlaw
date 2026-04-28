---
name: family-calendar
description: Family calendar management for Severino — school, activities, appointments, sync with Google Calendar
metadata:
  {
    "openclaw":
      {
        "emoji": "📅",
        "requires": { "tools": ["read", "write", "exec"], "skills": ["gog", "advanced-calendar"] },
        "primaryEnv": "GOOGLE_CALENDAR_CREDENTIALS"
      }
  }
---

# family-calendar

The Rezende family calendar. Antonio, Rebecca, school, activities, appointments—all in one place.

## Family Members

**Rod**
- Work: GrowBiz Media
- Travel: Business + family
- Preferences: Advance notice, conflict alerts

**Karine**
- Work: Imigrou, Studios
- Travel: Content shoots + family
- Preferences: Voice-first updates, Portuguese OK

**Antonio (12)**
- School: Warren Middle School
- Activities: Jiu Jitsu, Tennis, Coding
- Pickup: 3:15 PM school days
- Conflicts: Tuesdays (Jiu Jitsu + Tennis overlap)

**Rebecca (8)**
- School: Angelo L Thomaso
- Activities: Ballet, Tennis, Singing, Drawing
- Pickup: 2:45 PM school days
- Birthday: March 27 (highest priority)

## Calendar Sources

- Google Calendar (primary)
- School portals (Warren, ALT)
- Activity schedules (dojos, clubs)
- Manual entries (Karine/Rod)

## Conflict Detection

**Auto-detect conflicts:**
- Two events at same time
- Travel time insufficient
- Back-to-back activities (tired kids)
- No pickup coverage

**Conflict Resolution:**
```
⚠️ Conflict detected
Tuesday 3:30 PM:
• Antonio: Jiu Jitsu
• Rebecca: Tennis

Options:
1. Rod picks up Antonio late (4:00 PM)
2. Karine leaves work early
3. Ask another parent for ride

Confirm: [Option 1] [Option 2] [Option 3]
```

## Reminder Cascade

**Standard reminders:**
- 24 hours: "Tomorrow: [event]"
- 2 hours: "Soon: [event]"
- 30 minutes: "Now: [event]"

**Pickup reminders:**
- Rod: Discord 1 hour before
- Karine: WhatsApp (Jarbas) 30 minutes before

**Special:**
- Birthday: 30 days, 7 days, day before
- Travel: 1 week, 2 days, day before
- Medical: 1 day, 2 hours

## Quick Queries

```
What's the schedule Tuesday?
```
→ Shows all 4 family members' events

```
When is Rebecca's next ballet?
```
→ Next occurrence + recurring pattern

```
Any conflicts this week?
```
→ Flags scheduling issues

```
Add [event] on [date] at [time]
```
→ Creates event, asks who else

## School Calendar Integration

**Warren Middle (Antonio):**
- Early dismissal days
- Parent-teacher conferences
- Testing schedules
- Breaks/holidays

**Angelo L Thomaso (Rebecca):**
- Same as above
- + Kinder-specific events

Sync: Import iCal feeds, parse PDFs if needed

## Activity Schedules

**Jiu Jitsu (Antonio):**
- Tuesdays, Thursdays: 4:00-5:30 PM
- Saturday: 10:00-11:30 AM

**Tennis (both):**
- Varies by season
- Check club schedule

**Ballet (Rebecca):**
- Mondays, Wednesdays: 4:00-5:00 PM
- Recital: May (mark early)

**Singing (Rebecca):**
- Fridays: 3:30-4:30 PM

**Drawing (Rebecca):**
- Saturdays: 9:00-10:30 AM

## Recurring Patterns

**School year:**
- Sep-Jun (check district calendar)
- Holidays: federal + state + snow days

**Summer:**
- Camps, travel, downtime
- Different routine

**Travel blocks:**
- Mark as "away"
- Pause conflicting activities
- Arrange coverage

## Language

- Rod: English
- Karine: Portuguese
- Events: English (Rod's primary), Portuguese note if Karine's

## Tool Usage

```javascript
// Add event
await skills.gog.calendar.create({
  summary: 'Antonio Jiu Jitsu',
  start: '2026-03-25T16:00:00',
  end: '2026-03-25T17:30:00',
  recurrence: 'weekly',
  attendees: ['rod@growbiz.media']
});

// Check conflicts
const conflicts = await skills.advanced_calendar.checkConflicts('2026-03-25');

// Send reminder
await tools.sessions_send({
  sessionKey: 'main',
  message: 'Reminder: Antonio pickup in 30 min'
});
```

## Files

- Master: Google Calendar (Rezende Family)
- Local cache: `~/.openclaw/workspace-severino/calendar/`
- School feeds: `~/.openclaw/workspace-severino/feeds/`
- Activity schedules: `~/.openclaw/workspace-severino/schedules/`

## ARP Integration

Called by:
- Severino directly (Rod's Discord requests)
- Jarbas → Severino (Karine's family requests)

Returns:
- Formatted schedule
- Conflict warnings
- Confirmation of changes
