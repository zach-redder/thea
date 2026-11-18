# Memory

Persistent memory is requirement #1. The goal is a working understanding of
Zach that deepens over time, not a transcript archive. This doc is the design;
[data-model.md](data-model.md) has the tables.

## The four layers

| Layer | Store | Lifetime | Holds | Think of it as |
|---|---|---|---|---|
| **Working** | Redis | minutes to hours (TTL) | The active conversation, last N turns, presence, "what we were just doing", pending approvals | What's in her head right now |
| **Episodic** | Postgres `thea.memories` + pgvector | permanent, decays in salience | Distilled events and exchanges: "decided to move the launch to Friday" | What happened |
| **Semantic** | Postgres `identity.*`, `wardrobe.*`, `environment.*` | permanent, edited in place | Structured facts: profile, people, goals, projects, routines, home, devices | What's true |
| **Narrative** | Postgres `identity.context` | rewritten nightly | A living summary of Zach's current chapter: headspace, focus, challenges, tone | Where he is in life |

A fifth, derived layer, **stats** (habits, sleep, spending, activity), is
described in [stats-and-dashboard.md](stats-and-dashboard.md).

## Redis (working memory)

Redis is the fast, disposable layer. Losing it must never lose knowledge.

| Key pattern | Value | TTL |
|---|---|---|
| `session:{id}` | Conversation turns (the messages sent to the model) | 24 h, refreshed on use |
| `session:{id}:meta` | channel, room, started_at, summary-so-far | 24 h |
| `presence` | room → last-seen timestamp, speaker | 15 min |
| `approval:{id}` | A pending tool call awaiting a yes/no | 10 min |
| `ctx:cache:{hash}` | Recently assembled retrieval results | 5 min |
| `stream:{session}` | Pub/sub for streaming replies to clients | none |

- A single logical **session spans channels**: if Zach speaks in the living
  room and then opens the web app within the continuity window, the session id
  carries over (looked up by user + recency, not by device). That's
  cross-context continuity in practice.
- On session end (idle timeout), the turns are flushed to the durable log
  (see below) and handed to the extraction pass.

## Postgres (long-term memory)

### Writing: the extraction pass

After a conversation goes quiet, the agent runs a cheap, fast-model pass:

1. Read the session's turns plus relevant existing facts.
2. Emit a structured list of **operations**, not free text:
   - `remember` → new episodic memory (`content`, `salience` 1–5,
     `occurred_at`, `source`, optional `related_table`/`related_id`)
   - `update_fact` → change a semantic row (a new goal status, a project's
     state, a relationship's last-contacted)
   - `link` → attach a memory to a person/project/goal row
   - `forget` → mark a memory superseded (soft; see below)
3. A **deduplication** step compares the candidate embedding to existing
   memories, so "I'm tired" a hundred times doesn't become a hundred rows
   (merge or bump salience instead).
4. The **writer** embeds (Voyage, 1536-d) and inserts.

Rules for what's worth remembering:
- Decisions, commitments, preferences, corrections, life events, ongoing
  projects, and people-details Zach would expect her to know.
- Not: small talk, anything said to someone else, content from a call,
  secrets he asked her to forget, or whatever `privacy_mode` was covering.
- When Zach **corrects** her, the correction wins and the old fact is
  superseded, never silently kept.

### Reading: retrieval

Per turn, the context builder gathers candidates and ranks them:

```
score = similarity(query, memory.embedding)
      × recency_decay(occurred_at)
      × salience_weight(salience)
      + boost if linked to an entity named in the turn
```

- Run **two retrievals** in parallel: semantic (pgvector, top-k) and
  entity-linked (rows connected to people/projects mentioned).
- Pull only a handful (default ≈ 6) into the prompt, with the oldest
  summarized. Memory should feel like recall, not a data dump.
- A **fast path** skips retrieval entirely for trivial intents (lights).

### Maintenance

- **Consolidation (nightly):** merge near-duplicate memories, summarize old
  clusters ("March: trip planning" → one memory), decay salience of untouched
  items, and refresh `identity.context` (the narrative layer).
- **Forgetting:** supported and honored. "Forget that" marks the memory
  `superseded` and removes its embedding. The memory browser in the web app
  can delete anything. (Needs a `status` column; see schema additions in
  [data-model.md](data-model.md#planned-schema-additions).)
- **Provenance:** every memory records `source` (channel, session) so it can
  be audited and explained ("I remember because you told me on Tuesday").

## The durable conversation log

Separate from memory: a complete, boring record of what was said and which
tools ran, for the logs page, debugging and approvals audit. Tables
`thea.conversations`, `thea.messages`, `thea.tool_calls` (planned; see
data-model). Memory is *derived from* this log, not the same thing.

## Account-derived memory

Information flowing in from GitHub, calendar, social and the phone isn't
"conversation", but it feeds the same stores:

- Structured, queryable facts and time series → semantic + stats tables.
- Notable events ("PR merged", "stream went live", "flight booked") →
  episodic memories with `source='integration:github'` and so on.
- She doesn't have to be asked to know these things, since they're already in
  her context when relevant.

## Privacy

- Raw audio/video are never stored. Memory comes only from transcripts the
  agent chose to act on, so ambient speech she wasn't addressed in isn't
  recorded by default.
- Guests: if a non-owner voice is present, no memory is written from that
  turn.
- Everything is local to the home server's Postgres. Only the text needed for
  a turn goes to Claude and Voyage.

## Cross-context continuity: the checklist

A new surface is "continuous" if it:
1. authenticates against the same agent API,
2. uses the same session lookup (user + recency),
3. gets the same persona prompt (only the channel style differs),
4. reads and writes the same Postgres and Redis.

If all four hold, nothing else is needed for consistency. That's why
surfaces are thin channel adapters.
