# Remote access (your phone, away from home)

THEA runs on a home server. Reaching her from your phone has two parts: a
**private network path** to the server, and an **app** on the phone.

## Network: Tailscale

Use [Tailscale](https://tailscale.com) (a WireGuard mesh VPN). See [ADR 0007](decisions/0007-tailscale-remote-access.md).

1. Install Tailscale on the home server and on your phone, signed into the same
   account.
2. The server gets a stable private name, for example `thea-server.tail1234.ts.net`.
3. Give it HTTPS with Tailscale's built-in certificates: on the server, run
   `tailscale serve --bg 3000` for the web app, and serve `:8000` for the API
   (or put both behind one reverse proxy).
4. Set `NEXT_PUBLIC_THEA_API_URL` to the server's Tailscale URL when building the
   web app, and add that origin to the agent's `CORS_ORIGINS`.

Why not port-forwarding or a public tunnel: THEA can unlock doors, read your
finances and use your PC. Nothing about her should be reachable from the
public internet. Tailscale keeps every port off the internet while working
from anywhere.

## The phone app: install the PWA

The web app is an installable Progressive Web App (manifest, icon, standalone
display, safe-area aware, bottom tab bar):

- **iOS:** open the Tailscale URL in Safari → Share → *Add to Home Screen*.
- **Android:** open it in Chrome → *Install app*.

On first launch, paste your `THEA_API_TOKEN` once. It's stored on that device
only.

## Hands-free and automations

- **Siri / Shortcuts** and **Tasker** can call `POST /api/v1/chat` directly.
  [api.md](api.md#examples) has a ready-made shortcut.
- Location automations ("when I arrive home") can post a message the same way.

## Later

- Push notifications for approvals and proactive messages (Web Push from the
  agent).
- Per-device tokens, so a lost phone can be revoked alone.
- A native wrapper (Tauri 2 also targets iOS and Android) if the PWA hits limits
  such as background audio.
