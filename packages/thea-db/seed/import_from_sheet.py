#!/usr/bin/env python3
"""Extracts populated data rows from THEA DB.xlsx into seed/local_seed.sql.

This file is gitignored on purpose (see seed/README.md) -- the sheet
contains real personal data, not fixtures. Re-run this locally whenever
you want fresh seed data; nothing here should ever be committed.
"""
from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path

from app.schema_reader import load_registry, read_table_rows, require_xlsx_path

SEED_FILE = Path(__file__).parent / "local_seed.sql"


def sql_literal(value) -> str:
    if value is None or value == "":
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, float) and value.is_integer():
        return repr(int(value))
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, (date, datetime)):
        return f"'{value.isoformat()}'"
    text = str(value).replace("'", "''")
    return f"'{text}'"


def render_insert(schema_name: str, table_name: str, rows: list[dict]) -> str | None:
    if not rows:
        return None
    columns = [c for c in rows[0].keys() if c is not None]
    has_id = "id" in columns
    overriding = " OVERRIDING SYSTEM VALUE" if has_id else ""
    lines = [f"INSERT INTO {schema_name}.{table_name} ({', '.join(columns)}){overriding} VALUES"]
    value_rows = []
    for row in rows:
        values = ", ".join(sql_literal(row.get(c)) for c in columns)
        value_rows.append(f"    ({values})")
    statement = "\n".join(lines) + "\n" + ",\n".join(value_rows) + ";"
    if has_id:
        # explicit ids via OVERRIDING SYSTEM VALUE don't advance the identity
        # sequence, so later un-overridden inserts would collide with these.
        statement += (
            f"\nSELECT setval(pg_get_serial_sequence('{schema_name}.{table_name}', 'id'), "
            f"(SELECT MAX(id) FROM {schema_name}.{table_name}));"
        )
    return statement


def generate(xlsx_path: Path) -> str:
    registry = load_registry(xlsx_path)
    header_comment = (
        "-- Generated from THEA DB.xlsx by seed/import_from_sheet.py."
        " Contains real personal data -- never commit this file."
    )
    blocks = [header_comment]
    for schema in registry.schemas:
        if schema.name == "public":
            continue
        for table in schema.tables:
            rows = read_table_rows(xlsx_path, table.name)
            insert = render_insert(schema.name, table.name, rows)
            if insert:
                blocks.append(insert)
    return "\n\n".join(blocks) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xlsx", type=Path, default=None)
    args = parser.parse_args()

    xlsx_path = require_xlsx_path(args.xlsx)
    content = generate(xlsx_path)
    SEED_FILE.write_text(content, encoding="utf-8", newline="\n")
    print(f"wrote {SEED_FILE} ({len(content.splitlines())} lines) -- gitignored, not committed")


if __name__ == "__main__":
    main()
