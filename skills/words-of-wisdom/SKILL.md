# SKILL.md - words-of-wisdom

## Name
words-of-wisdom

## Description
Daily philosophical wisdom and inspirational quotes for Rod. Curates insights from history's greatest thinkers — ancient philosophers, religious teachers, literary giants, and modern wisdom. Delivered every morning to start the day with perspective.

## Sources

### Ancient Philosophers
- **Plato** — Idealism, the Forms, justice
- **Socrates** — Questioning, self-knowledge, virtue
- **Aristotle** — Ethics, habits, excellence
- **Confucius** — Relationships, virtue, social harmony
- **Laozi (Lao Tzu)** — Tao Te Ching, natural flow, simplicity
- **Marcus Aurelius** — Stoicism, duty, acceptance
- **Seneca** — Stoicism, time, mortality
- **Epictetus** — Control, freedom, resilience

### Religious & Spiritual Teachers
- **Jesus** — Love, forgiveness, humility, the Sermon on the Mount
- **Buddha** — Suffering, attachment, the Middle Way
- **Rumi** — Love, divine connection, presence

### Literary & Existential Thinkers
- **Fyodor Dostoevsky** — Suffering, free will, redemption
- **Leo Tolstoy** — Simplicity, purpose, moral action
- **Victor Frankl** — Meaning, suffering, choice
- **Friedrich Nietzsche** — Power, overcoming, individualism

### Modern Thinkers
- **C.S. Lewis** — Faith, imagination, virtue
- **G.K. Chesterton** — Wonder, gratitude, paradox
- **J.R.R. Tolkien** — Hope, fellowship, small acts
- **Jordan Peterson** — Responsibility, truth, meaning
- **Naval Ravikant** — Leverage, peace, compounding

## Daily Selection Method

1. **Random rotation** — Different philosopher each day
2. **Context-aware** — Match wisdom to current events (optional)
3. **Theme matching** — Monday: purpose, Friday: reflection, etc.
4. **Source diversity** — Rotate between ancient, religious, modern

## Format

```
🌅 Words of Wisdom — [Day], [Date]

"[Quote]"

— [Philosopher/Source]

💭 [Brief context or reflection]

[Optional: How this applies today]
```

## Examples

**Monday (Purpose/Action):**
```
🌅 Words of Wisdom — Monday, March 24, 2026

"We are what we repeatedly do. Excellence, then, is not an act, but a habit."

— Aristotle

💭 Your systems, your rituals, your daily actions — they compound. 

What habit are you building today?
```

**Tuesday (Struggle/Resilience):**
```
🌅 Words of Wisdom — Tuesday, March 25, 2026

"The cave you fear to enter holds the treasure you seek."

— Joseph Campbell

💭 Fear is a compass pointing toward growth.
```

**Wednesday (Simplicity/Focus):**
```
🌅 Words of Wisdom — Wednesday, March 26, 2026

"Simplicity is the ultimate sophistication."

— Leonardo da Vinci

💭 Complexity is easy. Clarity is hard.
```

**Thursday (Relationships/Love):**
```
🌅 Words of Wisdom — Thursday, March 27, 2026

"Do not be anxious about tomorrow, for tomorrow will be anxious for itself."

— Jesus (Matthew 6:34)

💭 Presence over worry. Today has enough trouble of its own.
```

**Friday (Reflection/Gratitude):**
```
🌅 Words of Wisdom — Friday, March 28, 2026

"The happiness of your life depends upon the quality of your thoughts."

— Marcus Aurelius

💭 Guard your mind. It's the garden you tend daily.
```

## Delivery Schedule

**Time:** 6:30 AM (before Pulse briefing at 7:30 AM)  
**Channel:** Discord (DM to Rod)  
**Language:** English (primary), occasional Portuguese for Karine/Jarbas crossover

## Philosophy Rotation

**Weekly Schedule:**
- **Monday:** Ancient Greek (Plato, Socrates, Aristotle) — Action, virtue
- **Tuesday:** Stoicism (Marcus Aurelius, Seneca, Epictetus) — Resilience
- **Wednesday:** Eastern (Confucius, Laozi, Buddha) — Flow, harmony
- **Thursday:** Religious/Spiritual (Jesus, Rumi) — Love, purpose
- **Friday:** Literary (Dostoevsky, Tolstoy, Frankl) — Meaning, suffering
- **Saturday:** Modern (Naval, Peterson, etc.) — Practical wisdom
- **Sunday:** Random/Seasonal — Surprise, reflection

## Special Occasions

- **Karine's birthday (March 27):** Love, family, feminine wisdom
- **Rebecca's birthday (April 12):** Children, innocence, future
- **Anniversaries:** Growth, journey, partnership
- **Business milestones:** Success, legacy, impact

## Content Sources

- **Primary:** Research from philosophical texts, verified quotes
- **Secondary:** Goodreads, BrainyQuote, verified collections
- **Tertiary:** Curated anthologies (like Daily Stoic, etc.)

## Verification

- **Double-check attribution** — Many quotes misattributed
- **Context matters** — Provide source work when possible
- **Accuracy over virality** — Prefer verified over popular

## Access Control

- **Rod:** Primary recipient
- **Karine (optional):** Can receive via Jarbas on special occasions
- **Team (optional):** Can broadcast to #morning-wisdom channel

## Permissions

- web_search (research quotes, verify attribution)
- memory_read (check previous quotes to avoid repetition)
- memory_write (log sent quotes, track rotation)
- cron (daily scheduling)

## Triggers

- "wisdom"
- "quote"
- "philosophy"
- "inspiration"
- "daily wisdom"
- Morning cron (automatic)

## Preferred Model

kimi-k2.5:cloud (fast, cheap, good for curation)

## Cron Schedule

**Daily:** 6:30 AM — "Words of Wisdom"

## Implementation Notes

- **Database of quotes:** Maintain 100+ verified quotes per philosopher
- **Rotation logic:** Track last sent date, rotate to avoid repetition
- **Seasonal themes:** Match wisdom to time of year (growth in spring, etc.)
- **User feedback:** If Rod favorites certain types, weight them higher

## Example First Week

| Day | Philosopher | Theme |
|-----|-------------|-------|
| Mon | Aristotle | Habits, excellence |
| Tue | Marcus Aurelius | Morning, duty |
| Wed | Confucius | Relationships |
| Thu | Jesus | Love, worry |
| Fri | Dostoevsky | Suffering, meaning |
| Sat | Naval Ravikant | Leverage, peace |
| Sun | Laozi | Flow, simplicity |

---

## Setup Checklist

- [ ] Create quote database (JSON/CSV)
- [ ] Verify attributions for top 20 quotes per philosopher
- [ ] Set up cron job (6:30 AM daily)
- [ ] Test first delivery
- [ ] Get Rod's feedback on format/timing

---

*Purpose: Start each day with wisdom that has stood the test of time.*
