# Archive

The original READMEs of the six repos that were merged into this monorepo,
kept word for word. They still use the old names (`thea-heart`, `thea-senses`,
...) and old paths, so read them as history, not current instructions.

Their content has been folded into the current docs:

| Original | Became |
|---|---|
| [`thea-heart.md`](original-readmes/thea-heart.md) | `services/agent`: [architecture](../architecture.md), [api](../api.md) |
| [`thea-senses.md`](original-readmes/thea-senses.md) | `services/voice` + `services/vision`: [voice pipeline](../voice-pipeline.md) |
| [`thea-muscles.md`](original-readmes/thea-muscles.md) | `services/home` (+ speech output in `services/voice`) |
| [`thea-brain.md`](original-readmes/thea-brain.md) | `packages/thea-db`: [data model](../data-model.md) |
| [`thea-body.md`](original-readmes/thea-body.md) | `apps/web`: [api](../api.md), [remote access](../remote-access.md) |
| [`thea-bones.md`](original-readmes/thea-bones.md) | root `docker-compose.yml`, `.github/`, `infra/`: [development](../development.md) |

Every repo's full commit history is preserved in this repo's git history.
`git log --all -- <old path>` finds it.
