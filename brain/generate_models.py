#!/usr/bin/env python3
"""Regenerates app/models/*.py from THEA DB.xlsx. Do not hand-edit the output."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from app.schema_reader import TYPE_MAP, TYPE_OVERRIDES, Column, Table, default_xlsx_path, load_registry

MODELS_DIR = Path(__file__).parent / "app" / "models"

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
        return '    id = Column(Integer, primary_key=True)', {"from sqlalchemy import Column, Integer"}
    py_type, imports = sqlalchemy_type(table.name, column)
    imports.add("from sqlalchemy import Column")
    args = [py_type]
    if not column.nullable:
        args.append("nullable=False")
    return f"    {column.name} = Column({', '.join(args)})", imports


def render_table_class(table: Table) -> tuple[str, set[str]]:
    imports: set[str] = {"from sqlalchemy import Column"}
    lines = [
        f'class {python_class_name(table.name)}(Base):',
        f'    __tablename__ = "{table.name}"',
        f'    __table_args__ = {{"schema": "{table.schema.name}"}}',
        "",
    ]
    for column in table.columns:
        col_line, col_imports = render_column(table, column)
        lines.append(col_line)
        imports |= col_imports
    return "\n".join(lines), imports


def render_module(schema_name: str, tables: list[Table]) -> str:
    all_imports: set[str] = {"from app.models.base import Base"}
    class_blocks: list[str] = []
    for table in tables:
        block, imports = render_table_class(table)
        class_blocks.append(block)
        all_imports |= imports

    sqlalchemy_imports = sorted(i for i in all_imports if i.startswith("from sqlalchemy import"))
    other_imports = sorted(i for i in all_imports if not i.startswith("from sqlalchemy import"))
    merged_names: set[str] = set()
    for imp in sqlalchemy_imports:
        names = imp.removeprefix("from sqlalchemy import ").split(", ")
        merged_names |= set(names)
    header = "# Auto-generated from THEA DB.xlsx via app/schema_reader.py. Do not hand-edit; re-run generate_models.py.\n"
    import_lines = [f"from sqlalchemy import {', '.join(sorted(merged_names))}"] + other_imports
    return header + "\n".join(import_lines) + "\n\n\n" + "\n\n\n".join(class_blocks) + "\n"


BASE_MODULE = '''# Auto-generated from THEA DB.xlsx via app/schema_reader.py. Do not hand-edit; re-run generate_models.py.
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
'''

# thea.memories isn't in the live sheet yet (see README.md "Known open items" #1) —
# mirrors the hardcoded fallback in generate_migrations.py.
MEMORIES_FALLBACK_CLASS = '''class Memories(Base):
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
    created_at = Column(DateTime(timezone=True))'''


def generate(xlsx_path: Path) -> dict[str, str]:
    registry = load_registry(xlsx_path)
    output = {"base.py": BASE_MODULE}
    for schema in registry.schemas:
        content = render_module(schema.name, schema.tables)
        if schema.name == "thea":
            if "from pgvector.sqlalchemy import Vector" not in content:
                content = content.replace(
                    "from app.models.base import Base\n",
                    "from app.models.base import Base\nfrom pgvector.sqlalchemy import Vector\n",
                    1,
                )
            content = content.rstrip("\n") + "\n\n\n" + MEMORIES_FALLBACK_CLASS + "\n"
        output[f"{schema.name}.py"] = content
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xlsx", type=Path, default=None)
    args = parser.parse_args()

    xlsx_path = args.xlsx or default_xlsx_path()
    if not xlsx_path.exists():
        raise SystemExit(f"Schema source not found: {xlsx_path}\nSet --xlsx or THEA_SCHEMA_XLSX to THEA DB.xlsx's location.")

    files = generate(xlsx_path)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    for old in MODELS_DIR.glob("*.py"):
        if old.name != "__init__.py":
            old.unlink()
    for name, content in files.items():
        (MODELS_DIR / name).write_text(content, encoding="utf-8", newline="\n")
        print(f"wrote app/models/{name}")


if __name__ == "__main__":
    main()
