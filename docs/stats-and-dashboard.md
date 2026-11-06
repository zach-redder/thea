# Stats and the dashboard

Requirement: stats about Zach are **easily accessible** (from the phone or the
desktop), tied to his calendar, habits, and the documentation of his life,
with a simple and fun frontend he can pull up any time.

> **Status:** designed; only the shell exists (`apps/web`: talk, memory, logs,
> health). Phases 1, 4 and 8 of the [implementation plan](implementation-plan.md).

## Principles

- **Glanceable first.** One screen ("Today") answers "how am I doing?" in
  five seconds. Depth is a tap away.
- **Her voice, his numbers.** Every stat is also something she can say. "How
  did I sleep this week?" and the Sleep card show the same data from the
  same source.
- **Honest, not gamified-for-its-own-sake.** Streaks and flair are welcome
  (it should be fun), but never guilt. The tone is the persona's: dry, kind,
  on his side.
- **Local and private.** Stats are computed on the home server from data in
  his Postgres.

## What "stats about me" covers

| Area | Examples | Source |
|---|---|---|
| **Time & schedule** | Today's agenda, free blocks, meeting load, upcoming deadlines | Google Calendar |
| **Habits & routines** | Streaks, completion rate, best times, drift | `identity.routines` + habit log (new) |
| **Goals & projects** | Progress, next actions, stale items | `identity.goals`, `identity.projects` |
| **Health & body** | Sleep, steps, workouts, weight, energy trend | Phone/Health export, wearables, manual |
| **Focus & work** | Coding activity, commits, PRs, focus sessions, desktop screen-time | GitHub, desktop bridge |
| **Creator** | Stream hours, viewers, followers/subs trend, clip performance | Twitch, YouTube |
| **Social** | Mentions, follower trend, post performance | Social adapters |
| **Money** | Budget status, subscriptions, spend by category (live, not stored) | Plaid via `identity.finances` |
| **Home** | Energy, temperature, time in rooms, device uptime | Home Assistant |
| **THEA herself** | Conversations, memories added, tool calls, latency, cost/tokens | The agent's own logs |
| **Life log** | A timeline of notable events and memories ("the documentation of life") | `thea.memories`, Notion |

## The screens

```
apps/web/app/
  page.tsx            Talk          (exists)
  today/              Today         the daily glance: agenda, habits due, what changed overnight, THEA's one-line read
  stats/              Stats         the numbers: tabs per area above, time-range picker
  habits/             Habits        check-offs, streaks, history; one tap to log
  life/               Life log      a scrollable timeline of events and memories; search
  home/               Home          rooms and devices, scenes, presence; big tap targets
  memory/ logs/ health/             (exist) browser, audit log, integration + service status
  settings/           Settings      integrations (connect flows), autonomy levels, privacy toggles, persona knobs
```

Phone-first: bottom tab bar for the five most-used (Talk, Today, Habits,
Home, More), and a desktop layout that uses the width for side-by-side cards.
The orb stays a persistent presence (a small version in the header on every
page; tap to talk).

### "Fun" lives in
- The orb and its states.
- Micro-interactions on habit check-offs, streak flames, gentle confetti on a
  personal best (respecting reduced-motion).
- A **weekly review card** THEA narrates ("here's your week, in two
  sentences").
- Themes tied to time of day (the `ember`/`tide` palette shifts at night).

## Data flow

```
Integrations (sync) ─┐
Phone context ───────┼─▶ stats collectors ─▶ stats tables (Postgres, time-series) ─▶ aggregators ─▶ /api/v1/stats/* ─▶ web
Habit check-offs ────┤                                                                    ▲
Agent logs/costs ────┘                                                                    └── also read by the agent as tools ("how did I sleep?")
```

- **Collectors** run on the scheduler (`thea_agent/stats/collectors/`), one per
  source, idempotent, writing raw samples with a `source` and `occurred_at`.
- **Aggregators** (`stats/aggregators.py`) compute daily/weekly rollups
  (streaks, averages, trends) and cache them (Redis, short TTL; or a rollup
  table).
- **API:** read-only endpoints under `/api/v1/stats/*` and `/api/v1/today`,
  habit logging via `POST /api/v1/habits/log`.
- **The agent uses the same aggregator functions as tools**
  (`get_stats(area, range)`), so numbers can never disagree between what she
  says and what the dashboard shows.

## Planned API

All `GET` reads take query parameters; lists are `POST .../list` per
[api.md](api.md) conventions. Stubs exist (501) so the contract is fixed.

| Method | Path | Returns |
|---|---|---|
| GET | `/api/v1/today` | Agenda, habits due, highlights, THEA's one-liner |
| GET | `/api/v1/stats/summary` | Headline numbers across every area for a range |
| GET | `/api/v1/stats/series` | `?area=sleep&range=30d` → time series for a chart |
| POST | `/api/v1/habits/list` | Habits with streaks and today's status |
| POST | `/api/v1/habits/log` | Check a habit on or off |
| POST | `/api/v1/life/list` | Life-log timeline (search, filters, offset/limit) |

## Schema additions this needs

None of these exist in `THEA DB.xlsx` yet. See
[data-model.md](data-model.md#planned-schema-additions) for columns. In short:
`habit_logs`, `metrics` (generic time series), and conversation/message
tables. Add them to the workbook's registry tabs and run `just gen-schema`.

## Charts and tech

- Recharts or Visx for charts. Keep them small, accessible (labelled,
  patterned, not color-only) and theme-aware.
- Server Components fetch aggregates; interactive widgets are client
  components.
- Live updates (orb state, approvals, new events) arrive over the existing
  WebSocket.
