# web

*Codename: body.* THEA's face. It has a talk screen (the orb, hold-to-talk,
chat), a memory browser, logs, and system health. It's an installable PWA, so
it's also the phone app, and the desktop app loads it too.

```bash
just web          # corepack pnpm --filter web dev -> http://localhost:3000
```

Set `NEXT_PUBLIC_THEA_API_URL` (see `.env.example`) when the agent isn't on
`localhost:8000`.

## Layout

```
app/
  layout.tsx, globals.css    shell, design tokens (ink / panel / ember / tide)
  page.tsx                   Talk
  memory/ logs/ health/      dashboard pages
components/                  orb, talk-panel, nav, placeholder-page
lib/
  api-client.ts              the only place that calls the agent (token, errors)
  case-convert.ts            snake_case <-> camelCase at the boundary
public/                      manifest.webmanifest, icon.svg
```

Stack: Next.js 16 (App Router), React 19, Tailwind CSS 4, TypeScript (strict).
Before committing: `pnpm --filter web lint`, `typecheck` and `build`.

More: [api](../../docs/api.md) · [remote access / phone install](../../docs/remote-access.md)
