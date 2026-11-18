# Deploy

**Target:** a small always-on home server running the same Docker Compose
stack as local development. Planned hardware is a Beelink SER7 or an Intel NUC
13 Pro with 32 GB RAM and a 1 TB NVMe drive. Add a GPU box later if local STT
or vision needs it.

> **Status:** not configured. `.github/workflows/deploy.yml` is a placeholder
> that fails on purpose.

## Plan

1. **Server:**
   - Ubuntu Server LTS, Docker Engine + the Compose plugin
   - `TZ=UTC`
   - Tailscale ([docs/remote-access.md](../../docs/remote-access.md))
2. **Code and secrets:**
   - Clone the repo to `/opt/thea`.
   - Put `.env` there with `chmod 600`, owned by the deploy user.
3. **Run:** `docker compose up -d` (add `--profile perception` once mics and
   cameras are attached).
4. **Data:**
   - Load the seed once: `just seed` on your PC, then copy the file over and
     `psql` it in. Never commit it.
   - Back up the `pgdata` volume nightly with `pg_dump` to a second disk or
     encrypted offsite storage.
5. **Deploy pipeline:** a GitHub Actions **self-hosted runner** on the server
   (no inbound ports needed) runs `git pull && docker compose up -d --build`
   on `workflow_dispatch` or on pushes to `main`.
6. **Expose:** `tailscale serve` for HTTPS on the tailnet only. Open no
   ports on the router.

## Hardware notes from the original `thea-bones` plan

- Migration from laptop to server is meant to be a straight copy of the
  compose setup. Keep it that way: no server-only configuration outside `.env`.
- Per-room hardware:
  - a ReSpeaker-style USB mic array
  - a Snapcast client (Raspberry Pi + speaker)
  - optional IP cameras (RTSP) for vision
