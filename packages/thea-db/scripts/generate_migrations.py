#!/usr/bin/env python3
"""Regenerates migrations/*.sql from THEA DB.xlsx. Do not hand-edit the output."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from thea_db.schema_reader import (
    REFERENCES_RE,
    TYPE_MAP,
    TYPE_OVERRIDES,
    Column,
    Registry,
    Schema,
    Table,
    load_registry,
    require_xlsx_path,
)

MIGRATIONS_DIR = Path(__file__).resolve().parents[1] / "migrations"

# thea.memories isn't in the live sheet yet (see README.md "Known open items" #1).
# Kept as a hardcoded fallback until the sheet is synced. vector(1536) to match
# every embedding column now that the sheet has moved off the old vector(1024).
MEMORIES_COMMENT = (
    "-- Distilled episodic memories from conversations and ambient events, embedded for"
    " semantic recall (NOT YET IN LIVE SHEET -- sync it)"
)
MEMORIES_FALLBACK_SQL = f"""{MEMORIES_COMMENT}
CREATE TABLE thea.memories (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(1536),
    occurred_at TIMESTAMPTZ,
    source TEXT,
    related_table TEXT,
    related_id INTEGER,
    salience INTEGER,
    notes TEXT,
    created_at TIMESTAMPTZ
);"""


NN_SUFFIX_RE = re.compile(r"\s*:\s*\(NN\)\s*$", re.IGNORECASE)


def sql_type(table_name: str, column: Column) -> str:
    override = TYPE_OVERRIDES.get((table_name, column.name))
    if override:
        return override
    raw = NN_SUFFIX_RE.sub("", column.raw_type).strip().lower()
    is_array = raw.endswith("[]")
    base = raw[:-2] if is_array else raw
    pg_type = base.upper() if base.startswith("vector(") else TYPE_MAP.get(base, base.upper())
    return f"{pg_type}[]" if is_array else pg_type


def column_ddl(table: Table, column: Column) -> tuple[str, str | None]:
    if column.name == "id":
        return "id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY", None
    pg_type = sql_type(table.name, column)
    not_null = "" if column.nullable else " NOT NULL"
    ddl = f"{column.name} {pg_type}{not_null}"
    fk = None
    match = REFERENCES_RE.search(column.description or "")
    if match and not pg_type.endswith("[]"):
        ref_schema, ref_table, ref_col = match.groups()
        fk = f"FOREIGN KEY ({column.name}) REFERENCES {ref_schema}.{ref_table}({ref_col})"
    return ddl, fk


def order_tables(tables: list[Table]) -> list[Table]:
    by_name = {t.name: t for t in tables}
    deps: dict[str, set[str]] = {t.name: set() for t in tables}
    for t in tables:
        for c in t.columns:
            match = REFERENCES_RE.search(c.description or "")
            if match and match.group(2) in by_name and match.group(2) != t.name:
                deps[t.name].add(match.group(2))

    ordered: list[Table] = []
    seen: set[str] = set()

    def visit(t: Table) -> None:
        if t.name in seen:
            return
        seen.add(t.name)
        for dep_name in sorted(deps[t.name]):
            visit(by_name[dep_name])
        ordered.append(t)

    for t in tables:
        visit(t)
    return ordered


def render_table(table: Table) -> str:
    lines: list[str] = []
    fks: list[str] = []
    for column in table.columns:
        ddl, fk = column_ddl(table, column)
        lines.append(f"    {ddl}")
        if fk:
            fks.append(f"    {fk}")
    body = ",\n".join(lines + fks)
    header = f"-- {table.description}\n" if table.description else ""
    return f"{header}CREATE TABLE {table.schema.name}.{table.name} (\n{body}\n);"


def render_public_schema(registry: Registry) -> str:
    public = registry.schema("public")
    header_comment = (
        "-- Auto-generated from THEA DB.xlsx via thea_db/schema_reader.py. "
        "Do not hand-edit; re-run generate_migrations.py."
    )
    lines = [header_comment, "CREATE EXTENSION IF NOT EXISTS vector;"]
    for schema in registry.schemas:
        lines.append(f"CREATE SCHEMA IF NOT EXISTS {schema.name};")
    lines.append("")
    for table in public.tables:
        lines.append(render_table(table))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_schema_migration(schema: Schema, add_memories_fallback: bool) -> str:
    ordered = order_tables(schema.tables)
    blocks = [render_table(t) for t in ordered]
    if add_memories_fallback:
        blocks.append(MEMORIES_FALLBACK_SQL)
    return "\n\n".join(blocks) + "\n"


def generate(xlsx_path: Path) -> dict[str, str]:
    registry = load_registry(xlsx_path)
    output: dict[str, str] = {"0001_extensions_and_public.sql": render_public_schema(registry)}

    non_public = [s for s in registry.schemas if s.name != "public"]
    for i, schema in enumerate(non_public, start=2):
        is_thea_schema = schema.name == "thea"
        content = render_schema_migration(schema, add_memories_fallback=is_thea_schema)
        output[f"{i:04d}_{schema.name}_schema.sql"] = content
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--xlsx",
        type=Path,
        default=None,
        help="Path to THEA DB.xlsx (defaults to THEA_SCHEMA_XLSX env var, or ../THEA DB.xlsx)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Print output without writing files; exit 1 if it would change anything",
    )
    args = parser.parse_args()

    xlsx_path = require_xlsx_path(args.xlsx)
    files = generate(xlsx_path)

    if args.check:
        changed = False
        for name, content in files.items():
            existing = (MIGRATIONS_DIR / name).read_text(encoding="utf-8") if (MIGRATIONS_DIR / name).exists() else None
            if existing != content:
                changed = True
                print(f"WOULD CHANGE: {name}")
        raise SystemExit(1 if changed else 0)

    MIGRATIONS_DIR.mkdir(exist_ok=True)
    for old in MIGRATIONS_DIR.glob("*.sql"):
        old.unlink()
    for name, content in files.items():
        (MIGRATIONS_DIR / name).write_text(content, encoding="utf-8", newline="\n")
        print(f"wrote migrations/{name}")


if __name__ == "__main__":
    main()
