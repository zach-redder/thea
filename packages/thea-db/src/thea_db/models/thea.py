# Auto-generated from THEA DB.xlsx via app/schema_reader.py. Do not hand-edit; re-run generate_models.py.

from pgvector.sqlalchemy import Vector
from sqlalchemy import ARRAY, Boolean, Column, DateTime, Integer, Numeric, Text, Time
from sqlalchemy.dialects.postgresql import JSONB

from thea_db.models.base import Base


class Config(Base):
    __tablename__ = "config"
    __table_args__ = {"schema": "thea"}

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    version = Column(Text)
    voice = Column(Text)
    response_style = Column(Text)
    wake_word = Column(Text)
    is_listening = Column(Boolean)
    default_model = Column(Text)
    fast_model = Column(Text)
    max_context_tokens = Column(Integer)
    temperature = Column(Numeric)
    max_response_length = Column(Integer)
    location = Column(Text)
    timezone = Column(Text)
    units = Column(Text)
    privacy_mode = Column(Boolean)
    do_not_disturb = Column(Boolean)
    do_not_disturb_start = Column(Time)
    do_not_disturb_end = Column(Time)
    notes = Column(Text)
    updated_at = Column(DateTime(timezone=True))


class Prompts(Base):
    __tablename__ = "prompts"
    __table_args__ = {"schema": "thea"}

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    context = Column(Text)
    prompt = Column(Text, nullable=False)
    active = Column(Boolean, nullable=False)
    notes = Column(Text)
    updated_at = Column(DateTime(timezone=True))


class Tools(Base):
    __tablename__ = "tools"
    __table_args__ = {"schema": "thea"}

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    integration_id = Column(Integer)
    schema = Column(JSONB)
    enabled = Column(Boolean)
    requires_confirm = Column(Boolean)
    notes = Column(Text)
    updated_at = Column(DateTime(timezone=True))


class Integrations(Base):
    __tablename__ = "integrations"
    __table_args__ = {"schema": "thea"}

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    enabled = Column(Boolean)
    api_endpoint = Column(Text)
    auth_type = Column(Text)
    scopes = Column(ARRAY(Text))
    last_synced = Column(DateTime(timezone=True))
    status = Column(Text)
    notes = Column(Text)
    updated_at = Column(DateTime(timezone=True))


class Memories(Base):
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
    created_at = Column(DateTime(timezone=True))
