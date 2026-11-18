# desktop

The THEA desktop app, built with [Tauri 2](https://tauri.app). It has two jobs:

1. **A native window onto THEA.** It loads the same UI as `apps/web` (from the home
   server, or from `pnpm dev:web` locally), so there's one frontend for desktop,
   phone and browser. Planned: a tray icon and a global push-to-talk shortcut.
2. **The desktop bridge (planned).** A sidecar that runs a local MCP server on
   `127.0.0.1`, so the agent can use *this* PC: open apps and files, read the
   screen, run commands. Every action needs confirmation in the THEA window.
   Tauri starts and stops it with the app.

Design and safety rules: [`docs/desktop.md`](../../docs/desktop.md).

## Status

Scaffold only. The config and Rust entrypoint are in place but haven't been
built yet, and CI doesn't build this app. Prerequisites: the Rust toolchain
(`rustup`) and the [Tauri prerequisites](https://tauri.app/start/prerequisites/)
for Windows (WebView2, MSVC build tools).

```bash
pnpm --filter web dev        # terminal 1: the UI on :3000
pnpm --filter desktop dev    # terminal 2: the native window
```

Before the first build, generate icons from the web icon:
`pnpm --filter desktop exec tauri icon ../web/public/icon.svg`.

For a packaged build, set `build.frontendDist` in `src-tauri/tauri.conf.json`
to your THEA server's URL (for example its Tailscale name).
