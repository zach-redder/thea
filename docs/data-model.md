# Data model

THEA's long-term state lives in one PostgreSQL 16 database with the
`pgvector` extension. Short-term session state (the active conversation,
presence) lives in Redis and is safe to lose.

## Where the schema comes from

The schema isn't hand-written. It's generated from **`THEA DB.xlsx`**, a
self-describing workbook that lives **next to** the repo (`H:\codebases\THEA\THEA DB.xlsx`),
never inside it, because it also holds real personal data.

```
THEA DB.xlsx
 ├─ schema_registry / table_registry / column_registry   ← structure (one row per schema/table/column)
 └─ one tab per table                                     ← actual data rows (personal)
        │
        ├─ packages/thea-db/scripts/generate_migrations.py → packages/thea-db/migrations/000N_*.sql   (committed)
        ├─ packages/thea-db/scripts/generate_models.py     → packages/thea-db/src/thea_db/models/*.py (committed)
        └─ packages/thea-db/seed/import_from_sheet.py      → packages/thea-db/seed/local_seed.sql      (gitignored!)
```

- `column_registry.data_type` gives each column's Postgres type. A
  `(references schema.table.id)` marker in a column's description becomes a
  foreign key.
- The generators order tables topologically by foreign key and are
  idempotent: re-running on an unchanged workbook gives byte-identical output.
  `just check-schema` verifies this.
- The workbook is found via `--xlsx`, then the `THEA_SCHEMA_XLSX` env var, then
  the folder that contains `thea/`.

**To change the schema:** edit the registry tabs in the workbook, run
`just gen-schema`, review the diff, and commit the migrations and models
together. Never hand-edit generated files.

**To load your data locally:** `just db` (Postgres + migrations), then `just seed`, then
`psql "$DATABASE_URL" -f packages/thea-db/seed/local_seed.sql`.
See [`packages/thea-db/seed/README.md`](../packages/thea-db/seed/README.md).

## Schemas

| Schema | Holds | Changes when |
|---|---|---|
| `public` | The registry tables that describe everything else | The schema changes |
| `thea` | THEA herself: config, prompts, tools, integrations, memories | You tune her behavior; she remembers something |
| `identity` | You: profile, personality, aesthetics, current context, goals, people, projects, skills, interests, routines, finances, health | Life changes; the nightly synthesis rewrites `identity.context` |
| `wardrobe` | Clothing, shoes, jewelry, accessories, outfits | You buy, wear or rate things |
| `environment` | Rooms, items, smart devices, documents, supplies, food, places, vehicles | Your home and logistics change |

### The tables that drive behavior

- **`thea.config`** is a single row holding THEA's runtime settings: the
  default and fast models, temperature, voice, wake word, units, timezone,
  `privacy_mode`, and the do-not-disturb window. Edit the row to change
  behavior. No redeploy.
- **`thea.prompts`** holds named system prompts per context (default, morning
  brief, guest present, ...). `active` toggles them.
- **`thea.integrations`** lists external services (Notion, Spotify, Plaid,
  Google Calendar, Home Assistant) with auth type, scopes and sync status.
- **`thea.tools`** lists the callable tools. Each has a JSON `schema`, an
  `enabled` flag, an optional `integration_id`, and **`requires_confirm`**,
  which forces a human yes before the tool runs.
- **`thea.memories`** stores episodic memories with a `vector(1536)` embedding,
  `salience`, and an optional link (`related_table`, `related_id`) to the
  structured row a memory is about.

Several `identity` and `environment` tables also carry `embedding vector(1536)`
columns, so semantic search works over goals, projects and so on, not just
memories. Embeddings are produced by the agent (Voyage AI). The database only
stores and searches them.

## Table reference

Generated from the registry. Structure only, no data.

### `public`

Registry and metadata tables for THEA database self-documentation

| Table | Purpose | Columns |
|---|---|---|
| `public.schema_registry` | Registry of all schemas in the THEA database | `id`, `schema_name`, `description`, `last_updated` |
| `public.table_registry` | Registry of all tables across all schemas | `id`, `schema_id`, `table_name`, `description`, `last_updated` |
| `public.column_registry` | Registry of all columns across all tables | `id`, `table_id`, `column_name`, `data_type`, `description`, `example_value`, `nullable`, `last_updated` |

### `thea`

THEA system configuration including core behavior settings, system prompts and tool definitions

| Table | Purpose | Columns |
|---|---|---|
| `thea.config` | Core THEA system settings including model, wake word, voice and behavior toggles | `id`, `name`, `version`, `voice`, `response_style`, `wake_word`, `is_listening`, `default_model`, `fast_model`, `max_context_tokens`, `temperature`, `max_response_length`, `location`, `timezone`, `units`, `privacy_mode`, `do_not_disturb`, `do_not_disturb_start`, `do_not_disturb_end`, `notes`, `updated_at` |
| `thea.prompts` | System prompts per context that define how THEA thinks and responds | `id`, `name`, `context`, `prompt`, `active`, `notes`, `updated_at` |
| `thea.tools` | Functions THEA can call during conversations with confirmation requirements | `id`, `name`, `description`, `integration_id`, `schema`, `enabled`, `requires_confirm`, `notes`, `updated_at` |
| `thea.integrations` | External service connections including Notion, Spotify, Plaid and Google Calendar | `id`, `name`, `enabled`, `api_endpoint`, `auth_type`, `scopes`, `last_synced`, `status`, `notes`, `updated_at` |

### `identity`

Core personal profile, personality, aesthetics, goals and projects

| Table | Purpose | Columns |
|---|---|---|
| `identity.profile` | Core personal facts about Zach including name, age, occupation and education | `id`, `name`, `gender`, `date_of_birth`, `age`, `location`, `hometown`, `occupation`, `employer`, `education_level`, `languages`, `nationality`, `description`, `updated_at` |
| `identity.personality` | Personality traits, values, communication style, motivators and drainers | `id`, `personality_traits`, `core_values`, `communication_styles`, `thinking_style`, `strengths`, `weaknesses`, `love_languages`, `motivators`, `drainers`, `notes`, `updated_at` |
| `identity.aesthetics` | Visual preferences, design sensibility, color palette and aesthetic influences | `id`, `visual_style`, `interior_style`, `color_palette`, `design_sensibility`, `influences`, `avoid`, `notes`, `updated_at` |
| `identity.context` | Current life chapter including headspace, tone, focus, challenges, energy level and working style | `id`, `life_stage`, `current_headspace`, `living_situation`, `financial_situation`, `working_style`, `work_environment`, `tone`, `vocabulary`, `avoid_phrases`, `humor_style`, `current_focus`, `current_challenges`, `energy_level`, `notes`, `updated_at` |
| `identity.goals` | Personal, professional, creative, financial and health goals with status and target dates | `id`, `goal`, `type`, `status`, `target_date`, `progress_notes`, `embedding`, `updated_at` |
| `identity.relationships` | People in Zachs life including friends, family, colleagues and mentors | `id`, `name`, `relationship_type`, `closeness`, `shared_interests`, `birthday`, `contact_frequency`, `location`, `last_interacted`, `notes`, `embedding`, `updated_at` |
| `identity.projects` | Active and past side projects including projects for fun and startups | `id`, `project_name`, `project_type`, `status`, `description`, `tech_stack`, `role`, `goals`, `url`, `notes`, `start_date`, `end_date`, `embedding`, `updated_at` |
| `identity.skills` | Technical, creative and philosophical skills with proficiency levels | `id`, `skill_name`, `category`, `proficiency_level`, `related_projects`, `notes`, `embedding`, `updated_at` |
| `identity.interests` | Hobbies, media, music, film and things Zach is into | `id`, `interest_name`, `category`, `subcategory`, `description`, `examples`, `notes`, `embedding`, `updated_at` |
| `identity.routines` | Daily routines and habits with triggers and steps | `id`, `routine_name`, `category`, `trigger`, `steps`, `frequency`, `is_active`, `streak_count`, `updated_at` |
| `identity.finances` | Budget priorities and tracked subscriptions; live balances and transactions come from Plaid via thea.integrations | `id`, `category`, `item_name`, `amount`, `priority_rank`, `frequency`, `status`, `notes`, `updated_at` |
| `identity.health` | Allergies, medications, dietary restrictions, sleep and fitness context | `id`, `height`, `weight`, `blood_type`, `dietary_restrictions`, `allergies`, `medications`, `sleep_schedule`, `avg_sleep_hours`, `body_fat_percent`, `notes`, `updated_at` |

### `wardrobe`

All clothing, shoes, jewelry, accessories and outfit combinations

| Table | Purpose | Columns |
|---|---|---|
| `wardrobe.clothing` | Tops, bottoms, outerwear and all clothing items with styling metadata | `id`, `name`, `brand`, `category`, `subcategory`, `color_primary`, `color_secondary`, `color_accent`, `material`, `pattern`, `silhouette`, `length`, `size_label`, `occasions`, `description`, `condition`, `owned`, `embedding` |
| `wardrobe.shoes` | All footwear with style, silhouette and sizing details | `id`, `name`, `brand`, `category`, `subcategory`, `color_primary`, `color_secondary`, `color_accent`, `material`, `silhouette`, `toe_shape`, `heel_type`, `size_us`, `occasions`, `description`, `condition`, `owned`, `embedding` |
| `wardrobe.jewelry` | Rings, necklaces, bracelets and earrings with material and finish details | `id`, `name`, `brand`, `category`, `subcategory`, `color_primary`, `material`, `stone_type`, `finish`, `dimensions`, `occasions`, `sentimental`, `description`, `condition`, `owned`, `embedding` |
| `wardrobe.accessories` | Bags, watches, sunglasses, gloves and other accessories | `id`, `name`, `brand`, `category`, `subcategory`, `color_primary`, `color_secondary`, `color_accent`, `material`, `dimensions`, `occasions`, `description`, `condition`, `owned`, `specs`, `embedding` |
| `wardrobe.outfits` | Saved outfit combinations with ratings and wear history | `id`, `name`, `occasion`, `shoe_id`, `clothing_ids`, `jewelry_ids`, `accessory_ids`, `notes`, `rating`, `worn_count`, `last_worn`, `embedding`, `updated_at` |

### `environment`

Rooms, devices, items, collections

| Table | Purpose | Columns |
|---|---|---|
| `environment.rooms` | Physical rooms in Zachs living space | `id`, `name`, `floor`, `notes`, `updated_at` |
| `environment.items` | Furniture, fitness equipment and collectibles, combined by category and tracked per room | `id`, `item_name`, `category`, `brand`, `room_id`, `quantity`, `material`, `condition`, `purchase_price`, `specs`, `notes`, `embedding`, `updated_at` |
| `environment.devices` | Smart home devices Zach owns including lights, speakers and thermostats | `id`, `name`, `type`, `brand`, `room_id`, `device_address`, `integration_id`, `notes`, `updated_at` |
| `environment.documents` | Important documents including passport, lease, insurance and expiry dates | `id`, `name`, `category`, `location`, `expiry_date`, `notes`, `updated_at` |
| `environment.supplies` | Consumable supplies tracked by quantity with low stock alerts | `id`, `name`, `category`, `quantity`, `low_stock_alert`, `room_id`, `notes`, `updated_at` |
| `environment.food` | Pantry, fridge and freezer inventory with expiry tracking | `id`, `name`, `category`, `quantity`, `expiry_date`, `low_stock_alert`, `notes`, `updated_at` |
| `environment.locations` | Frequented places including coffee shops, gym, work and favourite spots | `id`, `name`, `category`, `address`, `neighborhood`, `city`, `visit_frequency`, `favorite`, `notes`, `embedding`, `updated_at` |
| `environment.vehicles` | Car info, service history, oil changes, tire rotations and upcoming maintenance | `id`, `make`, `model`, `year`, `vin`, `license_plate`, `mileage`, `last_oil_change`, `last_tire_rotation`, `next_service_due`, `insurance_provider`, `insurance_policy`, `notes`, `updated_at` |

## Planned schema additions

The [vision](vision.md) needs tables that aren't in `THEA DB.xlsx` yet. Add
them as rows in the registry tabs (`table_registry`, `column_registry`) plus a
data tab per table, then run `just gen-schema`. The workbook holds personal
data, so Zach edits it (or explicitly asks for it to be edited). These are the
proposed columns, in generator types.

| Table | Needed by | Columns |
|---|---|---|
| `thea.memories` (move into registry) | Phase 1 | existing columns, plus `status` TEXT (`active`/`superseded`), `superseded_by` INTEGER, `last_recalled_at` TIMESTAMPTZ |
| `thea.conversations` | Phase 1 | `id`, `channel` TEXT, `started_at` TIMESTAMPTZ, `ended_at` TIMESTAMPTZ, `summary` TEXT, `room` TEXT |
| `thea.messages` | Phase 1 | `id`, `conversation_id` (references thea.conversations.id), `role` TEXT, `content` TEXT, `tokens_in` INTEGER, `tokens_out` INTEGER, `model` TEXT, `latency_ms` INTEGER, `created_at` TIMESTAMPTZ |
| `thea.tool_calls` | Phase 1 / 3 | `id`, `conversation_id`, `tool_id` (references thea.tools.id), `arguments` JSONB, `result` JSONB, `status` TEXT (`pending`/`approved`/`denied`/`done`/`error`), `approved_by` TEXT, `created_at` TIMESTAMPTZ |
| `thea.integration_credentials` | Phase 3 | `id`, `integration_id` (references thea.integrations.id), `encrypted_token` TEXT, `expires_at` TIMESTAMPTZ, `scopes` TEXT[], `updated_at` TIMESTAMPTZ ([ADR 0009](decisions/0009-integration-credentials.md)) |
| `thea.tools` + `autonomy` | Phase 8 | add `autonomy` INTEGER (0-4, see [agent-runtime.md](agent-runtime.md#autonomy-levels)) |
| `thea.preferences` | Phase 8 | `id`, `key` TEXT, `value` JSONB, `context` TEXT, `source` TEXT, `updated_at` TIMESTAMPTZ (learned addressee thresholds, per-context behavior) |
| `identity.habit_logs` | Phase 4 | `id`, `routine_id` (references identity.routines.id), `logged_at` TIMESTAMPTZ, `status` TEXT (`done`/`skipped`/`missed`), `notes` TEXT |
| `stats` schema + `stats.metrics` | Phase 4 | `id`, `area` TEXT (sleep, steps, commits, ...), `name` TEXT, `value` NUMERIC, `unit` TEXT, `occurred_at` TIMESTAMPTZ, `source` TEXT |

Notes for whoever adds these:
- Follow the existing conventions: INTEGER identity keys, `TIMESTAMPTZ`,
  `TEXT` (not VARCHAR), snake_case, `(references schema.table.id)` markers for
  foreign keys.
- `identity.routines` already models habits ("daily routines and habits with
  triggers and steps"). `habit_logs` adds the missing history; don't create a
  parallel `habits` table.
- A new `stats` schema also needs a `schema_registry` row.
- Embedding columns stay `vector(1536)`.

## Known schema issues

These are tracked here rather than silently fixed:

1. **`thea.memories` isn't in the workbook yet.** Both generators hard-code it as
   a fallback. Add it to the registry, then delete the fallback.
2. **Four column types are patched in code.** `TYPE_OVERRIDES` in
   `thea_db/schema_reader.py` corrects `thea.config.name` (TEXT),
   `temperature` (NUMERIC) and `do_not_disturb_start` / `do_not_disturb_end`
   (TIME). Fix the workbook, then remove the overrides.
3. **`schema_registry` has `"environment "` with a trailing space.** It's
   stripped in code; fix it at the source.
4. **The keys differ from the conventions used elsewhere.** The generated
   schema uses `INTEGER GENERATED ALWAYS AS IDENTITY` primary keys and real
   `FOREIGN KEY` constraints. The broader house style elsewhere prefers UUID
   keys and no FK constraints. Integer keys are fine for a single-user,
   single-database system and match the workbook's IDs. Changing this is a
   deliberate future decision (workbook + generator), not a drive-by edit.
5. **There are no soft deletes or `created_at` columns** on most tables (only
   `updated_at`). Add them through the registry if history ever matters.
