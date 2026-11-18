# thea-db

*Codename: brain.* THEA's long-term memory: the PostgreSQL 16 + pgvector
schema, SQLAlchemy models, repositories, and the Redis session store. It's a
**library** that only the agent imports, not a service.

```
migrations/          000N_*.sql, generated, applied in order by infra/migrate
scripts/             generate_migrations.py, generate_models.py
seed/                import_from_sheet.py -> local_seed.sql (gitignored, personal data)
src/thea_db/
  schema_reader.py   parses the registry tabs of THEA DB.xlsx
  models/            generated SQLAlchemy models, one module per schema
  repositories/      query functions, added as the agent needs them
  db.py              engine / session factory
  session_store.py   Redis short-term state
tests/
```

The schema is **generated from `THEA DB.xlsx`**, which lives beside the repo
and holds personal data:

```bash
just gen-schema      # regenerate migrations + models
just check-schema    # verify nothing is stale
just seed            # extract your data rows locally (never commit)
```

Never hand-edit `migrations/` or `models/`. Details, the table reference and
known schema issues: [docs/data-model.md](../../docs/data-model.md).
