# Roadmap

The one-screen version. The detailed tasks, file paths and acceptance tests
are in [implementation-plan.md](implementation-plan.md); the product they
serve is in [vision.md](vision.md).

Each phase ends with something Zach can use. Build them in order.

| Phase | Name | Ends with | Capabilities from the vision |
|---|---|---|---|
| **0** ✅ | Foundation | Monorepo, schema, service skeletons, auth, CI, web shell, docs | n/a |
| **1** | She talks | Text chat in the web app with her real voice (persona), sessions that survive refresh and span devices | Natural conversation, Postgres access, Redis sessions, frontend |
| **2** | She remembers | Facts told in one session come back later; corrections stick; nightly consolidation | Persistent memory, cross-context continuity |
| **3** | She can do things | Tools with approvals; calendar and GitHub connected; audit log | Account awareness, calendar, autonomy basics |
| **4** | Phone and life dashboard | Installed on the phone over Tailscale; Today, Stats, Habits, Life log | Phone connection, stats, habits, easy-to-reach frontend |
| **5** | She speaks and hears | ElevenLabs voice in the app, then push-to-talk, then room mics and the wake word | AI voice, microphones, wake word, fast response |
| **6** | She runs the house | Lights and devices by voice; scenes; presence | Home control |
| **7** | She's on your desktop | Tauri app, global shortcut, PC bridge with confirmations | Desktop connection |
| **8** | Aware and proactive | Knows when he's talking to her; ambient noticing; cameras; morning brief | Addressee detection, cameras, autonomy, "picks up on things" |
| **9** | More accounts, hardening | Twitch, social, per-device tokens, backups, monitoring | Social media, production |

Where to start: **Phase 1**, whose first task is a workbook change that needs
Zach (see the plan's "Things that need Zach").
