# Seed data

`local_seed.sql` is generated from `THEA DB.xlsx` and holds **real personal
data**: the identity profile, THEA's config, system prompts, and the
wardrobe/environment inventory. The root `.gitignore` (`**/seed/local_seed.sql`)
and `.dockerignore` both exclude it, and it must never be committed or baked
into an image. Only the schema *structure* is version-controlled, in
`../migrations/`.

## Regenerating

From the repo root:

```bash
just seed
# or
uv run --package thea-db python packages/thea-db/seed/import_from_sheet.py
```

By default this reads `THEA DB.xlsx` from the folder that **contains** the
`thea/` repo (a sibling of the repo, never inside it). Override it with
`--xlsx <path>` or the `THEA_SCHEMA_XLSX` environment variable.

## Loading into Postgres

Run the migrations first (`just migrate`), then:

```bash
psql "$DATABASE_URL" -f packages/thea-db/seed/local_seed.sql
```

Each `INSERT` uses `OVERRIDING SYSTEM VALUE` to keep the sheet's row IDs,
because some rows reference each other by ID (for example, `thea.tools`
references `thea.integrations`). A `setval()` call then advances each table's
identity sequence past the inserted IDs, so later inserts don't collide.
