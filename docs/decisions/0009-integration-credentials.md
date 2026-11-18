# 0009: OAuth tokens live in an encrypted database store, not `.env`

**Status:** accepted (2026-11-05)

## Context

THEA connects to many accounts (Google, GitHub, Twitch, Spotify, social).
Static keys fit in `.env` ([ADR 0008](0008-env-for-secrets-only.md)), but
OAuth access tokens expire and refresh tokens rotate, so the app must *write*
them back at runtime. A hand-edited file is the wrong place for values that
change under the app, and containers shouldn't rewrite their own `.env`.

## Decision

- Static secrets (API keys, PATs, the encryption key itself) stay in `.env`.
- OAuth tokens go in `thea.integration_credentials` (provider, encrypted
  token blob, expiry, scopes), encrypted at rest with an authenticated cipher
  (Fernet/AES-GCM). The key is `CREDENTIAL_ENCRYPTION_KEY` in `.env`.
- Tools receive an authenticated client, never the raw token, and tokens
  are never logged or placed in prompts.
- A connect flow in the web app (Settings → Integrations) performs the OAuth
  dance, redirecting via the Tailscale URL.

## Consequences

- Refresh handled in one place; rotation is safe.
- The workbook gains one table (`thea.integration_credentials`).
- Losing `CREDENTIAL_ENCRYPTION_KEY` means re-connecting integrations. Back it
  up separately from the database.
- A database dump alone doesn't expose tokens.
