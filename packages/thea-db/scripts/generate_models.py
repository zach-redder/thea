#!/usr/bin/env python3
"""Regenerates app/models/*.py from THEA DB.xlsx. Do not hand-edit the output."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from thea_db.schema_reader import TYPE_MAP, TYPE_OVERRIDES, Column, Table, load_registry, require_xlsx_path

MODELS_DIR = Path(__file__).resolve().parents[1] / "src" / "thea_db" / "models"

HEADER_COMMENT = (
    "# Auto-generated from THEA DB.xlsx via app/schema_reader.py. Do not hand-edit; re-run generate_models.py."
)

SQLALCHEMY_TYPE_MAP = {
    "INTEGER": "Integer",
    "TEXT": "Text",
    "BOOLEAN": "Boolean",
    "TIMESTAMPTZ": "DateTime(timezone=True)",
    "DATE": "Date",
    "TIME": "Time",
    "NUMERIC": "Numeric",
    "JSONB": "JSONB",
}

NN_SUFFIX_RE = re.compile(r"\s*:\s*\(NN\)\s*$", re.IGNORECASE)


def python_class_name(table_name: str) -> str:
    return "".join(part.capitalize() for part in table_name.split("_"))


def postgres_type(table_name: str, column: Column) -> str:
    override = TYPE_OVERRIDES.get((table_name, column.name))
    if override:
        return override
    raw = NN_SUFFIX_RE.sub("", column.raw_type).strip().lower()
    is_array = raw.endswith("[]")
    base = raw[:-2] if is_array else raw
    pg_type = base.upper() if base.startswith("vector(") else TYPE_MAP.get(base, base.upper())
    return f"{pg_type}[]" if is_array else pg_type


def sqlalchemy_type(table_name: str, column: Column) -> tuple[str, set[str]]:
    imports: set[str] = set()
    pg_type = postgres_type(table_name, column)
    is_array = pg_type.endswith("[]")
    base = pg_type[:-2] if is_array else pg_type

    if base.startswith("VECTOR("):
        dim = base[len("VECTOR(") : -1]
        imports.add("from pgvector.sqlalchemy import Vector")
        py_type = f"Vector({dim})"
    else:
        sub_type = SQLALCHEMY_TYPE_MAP.get(base, "Text")
        if sub_type == "JSONB":
            imports.add("from sqlalchemy.dialects.postgresql import JSONB")
        else:
            class_name = sub_type.split("(")[0]
            imports.add(f"from sqlalchemy import {class_name}")
        py_type = sub_type

    if is_array:
        imports.add("from sqlalchemy import ARRAY")
        return f"ARRAY({py_type})", imports
    return py_type, imports


def render_column(table: Table, column: Column) -> tuple[str, set[str]]:
    if column.name == "id":
        return "    id = Column(Integer, primary_key=True)", {"from sqlalchemy import Column, Integer"}
    py_type, imports = sqlalchemy_type(table.name, column)
    imports.add("from sqlalchemy import Column")
    args = [py_type]
    if not column.nullable:
        args.append("nullable=False")
    return f"    {column.name} = Column({', '.join(args)})", imports


def render_table_class(table: Table) -> tuple[str, set[str]]:
    imports: set[str] = {"from sqlalchemy import Column"}
    lines = [
        f"class {python_class_name(table.name)}(Base):",
        f'    __tablename__ = "{table.name}"',
        f'    __table_args__ = {{"schema": "{table.schema.name}"}}',
        "",
    ]
    for column in table.columns:
        col_line, col_imports = render_column(table, column)
        lines.append(col_line)
        imports |= col_imports
    return "\n".join(lines), imports


def render_module(
    schema_name: str,
    tables: list[Table],
    extra_imports: set[str] | None = None,
    extra_classes: list[str] | None = None,
) -> str:
    all_imports: set[str] = {"from thea_db.models.base import Base"} | (extra_imports or set())
    class_blocks: list[str] = []
    for table in tables:
        block, imports = render_table_class(table)
        class_blocks.append(block)
        all_imports |= imports
    class_blocks.extend(extra_classes or [])

    first_party = sorted(i for i in all_imports if i.startswith("from thea_db."))
    third_party = sorted(i for i in all_imports if not i.startswith("from thea_db."))

    sqlalchemy_imports = [i for i in third_party if i.startswith("from sqlalchemy import")]
    other_third_party = sorted(i for i in third_party if not i.startswith("from sqlalchemy import"))
    merged_names: set[str] = set()
    for imp in sqlalchemy_imports:
        merged_names |= set(imp.removeprefix("from sqlalchemy import ").split(", "))

    third_party_lines = other_third_party + [f"from sqlalchemy import {', '.join(sorted(merged_names))}"]
    third_party_lines.sort()

    import_block = "\n".join(third_party_lines) + "\n\n" + "\n".join(first_party)
    return HEADER_COMMENT + "\n\n" + import_block + "\n\n\n" + "\n\n\n".join(class_blocks) + "\n"


BASE_MODULE = f"""{HEADER_COMMENT}
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
"""

# thea.memories isn't in the live sheet yet (see README.md "Known open items" #1) —
# mirrors the hardcoded fallback in generate_migrations.py.
MEMORIES_FALLBACK_CLASS = """class Memories(Base):
    __tablename__ = "memories"
    __table_args__ = {"schema": "thea"}

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1536))
    occurred_at = Column(DateTime(timezone=True))
    source = Column(Text)
    related_table = Column(Text)
    related_id = Column(Integer)
    salience = Column(Integer)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True))"""


def generate(xlsx_path: Path) -> dict[str, str]:
    registry = load_registry(xlsx_path)
    output = {"base.py": BASE_MODULE}
    for schema in registry.schemas:
        if schema.name == "thea":
            content = render_module(
                schema.name,
                schema.tables,
                extra_imports={"from pgvector.sqlalchemy import Vector"},
                extra_classes=[MEMORIES_FALLBACK_CLASS],
            )
        else:
            content = render_module(schema.name, schema.tables)
        output[f"{schema.name}.py"] = content
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xlsx", type=Path, default=None)
    args = parser.parse_args()

    xlsx_path = require_xlsx_path(args.xlsx)
    files = generate(xlsx_path)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    for old in MODELS_DIR.glob("*.py"):
        if old.name != "__init__.py":
            old.unlink()
    for name, content in files.items():
        (MODELS_DIR / name).write_text(content, encoding="utf-8", newline="\n")
        print(f"wrote src/thea_db/models/{name}")


if __name__ == "__main__":
    main()
