# 0008: `.env` holds secrets only; behavior lives in `thea.config`

**Status:** accepted (2026-11-05). Adopted from Hermes Agent's contributor guide.

## Context

Tuning an assistant (which model, which voice, the DND window, privacy mode)
should be quick, auditable, and possible from THEA's own UI, or even by
asking her. Environment variables need a restart, are invisible to the app,
and blur the line between secret and setting.

## Decision

- `.env` (via `pydantic-settings`) contains only credentials and service
  addresses.
- Every behavioral setting is a column in `thea.config` (or a row in
  `thea.prompts` / `thea.tools`), read at runtime.

## Consequences

- Changing behavior is an UPDATE, not a redeploy.
- Settings are visible in the dashboard and can be changed by THEA herself
  (with confirmation).
- New behavior flags require a schema change via the workbook. That's
  intentional friction.
