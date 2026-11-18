# 0006: Tauri 2 for the desktop app; a local MCP bridge for PC control

**Status:** accepted (2026-11-05)

## Context

"Desktop access" means a native THEA app on the PC, and also letting the agent
(running on the home server) use that PC. Electron is the common choice but
ships a whole Chromium (about 150 MB, heavy RAM). The PC must never accept
inbound connections.

## Decision

- **Tauri 2:** a small Rust shell around the system webview (WebView2 on
  Windows) that loads the same UI as `apps/web`. It has first-class tray,
  global-shortcut and notification plugins, and a sidecar mechanism.
- **The desktop bridge** is a sidecar that runs a local **MCP server** on
  `127.0.0.1`. The agent's tool calls arrive over the app's own authenticated
  WebSocket and are relayed to the bridge after the user confirms in the
  window.

## Consequences

- One frontend everywhere; a desktop binary of a few MB.
- Building the desktop app needs the Rust toolchain. It's kept out of CI
  until it's actively developed.
- Desktop tools exist only while the app is open. That's a feature: closing
  the app revokes PC access.
