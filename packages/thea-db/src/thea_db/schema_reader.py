from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from openpyxl import load_workbook

TYPE_MAP = {
    "int": "INTEGER",
    "text": "TEXT",
    "bool": "BOOLEAN",
    "timestamp": "TIMESTAMPTZ",
    "date": "DATE",
    "time": "TIME",
    "numeric": "NUMERIC",
    "jsonb": "JSONB",
}

# Sheet-side type bugs documented in docs/data-model.md "Known schema issues".
# Fix the sheet, then remove these.
TYPE_OVERRIDES: dict[tuple[str, str], str] = {
    ("config", "name"): "TEXT",
    ("config", "temperature"): "NUMERIC",
    ("config", "do_not_disturb_start"): "TIME",
    ("config", "do_not_disturb_end"): "TIME",
}

REFERENCES_RE = re.compile(r"references\s+(\w+)\.(\w+)\.(\w+)", re.IGNORECASE)


@dataclass
class Column:
    id: int
    table_id: int
    name: str
    raw_type: str
    description: str
    nullable: bool
    example_value: str | None = None


@dataclass
class Table:
    id: int
    schema_id: int
    name: str
    description: str
    schema: Schema
    columns: list[Column] = field(default_factory=list)


@dataclass
class Schema:
    id: int
    name: str
    description: str
    tables: list[Table] = field(default_factory=list)


@dataclass
class Registry:
    schemas: list[Schema]

    def schema(self, name: str) -> Schema:
        return next(s for s in self.schemas if s.name == name)


def _data_rows(ws: Any) -> Iterator[tuple[Any, ...]]:
    for row in ws.iter_rows(values_only=True):
        if not row or row[0] in (None, ""):
            continue
        if not isinstance(row[0], (int, float)):
            continue
        yield row


def load_registry(xlsx_path: Path) -> Registry:
    wb = load_workbook(xlsx_path, data_only=True, read_only=True)

    schemas: dict[int, Schema] = {}
    for row in _data_rows(wb["schema_registry"]):
        sid = int(row[0])
        schemas[sid] = Schema(id=sid, name=str(row[1]).strip(), description=(row[2] or "").strip())

    tables: dict[int, Table] = {}
    for row in _data_rows(wb["table_registry"]):
        tid = int(row[0])
        schema_id = int(row[1])
        table = Table(
            id=tid,
            schema_id=schema_id,
            name=str(row[2]).strip(),
            description=(row[3] or "").strip(),
            schema=schemas[schema_id],
        )
        tables[tid] = table
        schemas[schema_id].tables.append(table)

    for row in _data_rows(wb["column_registry"]):
        table_id = int(row[1])
        nullable = bool(row[6])
        column = Column(
            id=int(row[0]),
            table_id=table_id,
            name=str(row[2]).strip(),
            raw_type=str(row[3]).strip(),
            description=(row[4] or "").strip(),
            example_value=row[5],
            nullable=nullable,
        )
        tables[table_id].columns.append(column)

    for table in tables.values():
        table.columns.sort(key=lambda c: c.id)

    return Registry(schemas=sorted(schemas.values(), key=lambda s: s.id))


def read_table_rows(xlsx_path: Path, sheet_name: str) -> list[dict[str, Any]]:
    wb = load_workbook(xlsx_path, data_only=True, read_only=True)
    ws = wb[sheet_name]
    rows = list(ws.iter_rows(values_only=True))
    header = [h.strip() if isinstance(h, str) else h for h in rows[2]]
    data_rows = []
    for row in rows[4:]:
        if not row or row[0] in (None, "", "PK"):
            continue
        if not isinstance(row[0], (int, float)):
            continue
        data_rows.append(dict(zip(header, row, strict=False)))
    return data_rows


def default_xlsx_path() -> Path:
    import os

    env_path = os.environ.get("THEA_SCHEMA_XLSX")
    if env_path:
        return Path(env_path)
    # packages/thea-db/src/thea_db/schema_reader.py -> parents[5] is the folder that holds thea/
    return Path(__file__).resolve().parents[5] / "THEA DB.xlsx"


def require_xlsx_path(cli_arg: Path | None) -> Path:
    xlsx_path = cli_arg or default_xlsx_path()
    if not xlsx_path.exists():
        raise SystemExit(
            f"Schema source not found: {xlsx_path}\nSet --xlsx or THEA_SCHEMA_XLSX to THEA DB.xlsx's location."
        )
    return xlsx_path
