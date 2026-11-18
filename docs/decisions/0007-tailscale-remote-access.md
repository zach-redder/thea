# 0007: Tailscale for remote access; nothing on the public internet

**Status:** accepted (2026-11-05)

## Context

THEA must be reachable from your phone anywhere. She can also unlock doors,
read finances and control your PC. Port-forwarding or public tunnels would
put all of that one leaked token away from the internet.

## Decision

- The home server and your devices join one Tailscale tailnet (a WireGuard
  mesh).
- THEA is served on the server's tailnet name with HTTPS from `tailscale serve`.
- No ports are opened on the router.
- The phone uses the installable PWA, plus Shortcuts / Tasker against the same
  API.

## Consequences

- Each device needs the Tailscale app installed and signed in.
- Network-level access control comes on top of the API token (defense in
  depth).
- Sharing THEA with another person means adding them to the tailnet, which is
  deliberately inconvenient.
