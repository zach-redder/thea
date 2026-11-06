# Auto-generated from THEA DB.xlsx via app/schema_reader.py. Do not hand-edit; re-run generate_models.py.

from sqlalchemy import Boolean, Column, DateTime, Integer, Text

from app.models.base import Base


class SchemaRegistry(Base):
    __tablename__ = "schema_registry"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    schema_name = Column(Text)
    description = Column(Text)
    last_updated = Column(DateTime(timezone=True))


class TableRegistry(Base):
    __tablename__ = "table_registry"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    schema_id = Column(Integer)
    table_name = Column(Text)
    description = Column(Text)
    last_updated = Column(DateTime(timezone=True))


class ColumnRegistry(Base):
    __tablename__ = "column_registry"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    table_id = Column(Integer)
    column_name = Column(Text, nullable=False)
    data_type = Column(Text)
    description = Column(Text)
    example_value = Column(Text)
    nullable = Column(Boolean)
    last_updated = Column(DateTime(timezone=True))
