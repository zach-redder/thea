# steve-bones

DevOps for STEVE — Dockerfiles, docker-compose orchestration, and CI/CD across all six repos.

## Overview

steve-bones is the one repo whose whole job is to know about all the others. It's not a service that runs as part of STEVE's request/response loop — it's the deployment layer that brings every other repo up together, on a laptop during development or on the eventual dedicated hardware (Beelink SER7 or Intel NUC 13 Pro).

## Role in the STEVE system

steve-bones doesn't participate in runtime request handling at all — it exists one level above the other five repos:

- Defines the `docker-compose.yml` that runs Postgres, Redis, and all six services together.
- Owns CI/CD (GitHub Actions) for the whole system, since it's the only place that can meaningfully build and test cross-repo integration.
- Every other repo's Dockerfile is expected to live here, not in the individual repos, so deployment configuration stays in one place.

## Tech stack

- **Docker** / **Docker Compose**
- **GitHub Actions** — CI/CD
- Target deployment hardware: Beelink SER7 or Intel NUC 13 Pro (32GB RAM, 1TB NVMe), migrating from laptop-based development via a straight copy of the compose setup

## Planned structure

```
steve-bones/
├── docker-compose.yml               # postgres, redis, and all 6 services
├── docker-compose.override.yml      # laptop dev overrides
├── dockerfiles/
│   ├── heart.Dockerfile
│   ├── senses.Dockerfile
│   ├── brain.Dockerfile
│   ├── muscles.Dockerfile
│   └── body.Dockerfile
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
└── .env.example
```

## Status

**Not yet implemented.** Should come together incrementally as each other repo reaches a runnable state, rather than all at once — start with a `docker-compose.yml` covering just Postgres + Redis + steve-brain, and add services as they exist.

## Related repos

All of them — steve-heart · steve-brain · steve-senses · steve-muscles · steve-body
