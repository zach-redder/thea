# Seed data

`local_seed.sql` is generated from `THEA DB.xlsx` and contains real personal
data (identity profile, THEA's config, system prompts, wardrobe/environment
inventory). It is gitignored and must never be committed — the schema
structure is version-controlled via `../migrations/`, but the data itself
stays local-only.

## Regenerating

```
uv run --package brain python seed/import_from_sheet.py
```

By default this reads `THEA DB.xlsx` from the parent of the `thea/` repo
(i.e. a sibling of this repo, not inside it). Override with `--xlsx <path>`
or the `THEA_SCHEMA_XLSX` environment variable.

## Loading into Postgres

Run the migrations first (`../migrations/*.sql`, in order), then:

```
psql $THEA_DATABASE_URL -f seed/local_seed.sql
```

Each `INSERT` uses `OVERRIDING SYSTEM VALUE` to preserve the row IDs from
the sheet (since some rows reference each other by ID — e.g. `thea.tools`
references `thea.integrations`), followed by a `setval()` call to advance
each table's identity sequence past the inserted IDs so future inserts
don't collide.
