# Auto-generated from THEA DB.xlsx via app/schema_reader.py. Do not hand-edit; re-run generate_models.py.
from sqlalchemy import ARRAY, Boolean, Column, Date, DateTime, Integer, Numeric, Text
from app.models.base import Base
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import JSONB


class Profile(Base):
    __tablename__ = "profile"
    __table_args__ = {"schema": "identity"}

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    gender = Column(Text)
    date_of_birth = Column(Date)
    age = Column(Integer)
    location = Column(Text)
    hometown = Column(Text)
    occupation = Column(Text)
    employer = Column(Text)
    education_level = Column(Text)
    languages = Column(ARRAY(Text))
    nationality = Column(Text)
    description = Column(Text)
    updated_at = Column(DateTime(timezone=True))


class Personality(Base):
    __tablename__ = "personality"
    __table_args__ = {"schema": "identity"}

    id = Column(Integer, primary_key=True)
    personality_traits = Column(ARRAY(Text))
    core_values = Column(ARRAY(Text))
    communication_styles = Column(Text)
    thinking_style = Column(Text)
    strengths = Column(ARRAY(Text))
    weaknesses = Column(ARRAY(Text))
    love_languages = Column(ARRAY(Text))
    motivators = Column(ARRAY(Text))
    drainers = Column(ARRAY(Text))
    notes = Column(Text)
    updated_at = Column(DateTime(timezone=True))


class Aesthetics(Base):
    __tablename__ = "aesthetics"
    __table_args__ = {"schema": "identity"}

    id = Column(Integer, primary_key=True)
    visual_style = Column(Text)
    interior_style = Column(ARRAY(Text))
    color_palette = Column(ARRAY(Text))
    design_sensibility = Column(Text)
    influences = Column(ARRAY(Text))
    avoid = Column(ARRAY(Text))
    notes = Column(Text)
    updated_at = Column(DateTime(timezone=True))


class Context(Base):
    __tablename__ = "context"
    __table_args__ = {"schema": "identity"}

    id = Column(Integer, primary_key=True)
    life_stage = Column(Text)
    current_headspace = Column(Text)
    living_situation = Column(Text)
    financial_situation = Column(Text)
    working_style = Column(Text)
    work_environment = Column(Text)
    tone = Column(Text)
    vocabulary = Column(Text)
    avoid_phrases = Column(ARRAY(Text))
    humor_style = Column(Text)
    current_focus = Column(ARRAY(Text))
    current_challenges = Column(ARRAY(Text))
    energy_level = Column(Text)
    notes = Column(Text)
    updated_at = Column(DateTime(timezone=True))


class Goals(Base):
    __tablename__ = "goals"
    __table_args__ = {"schema": "identity"}

    id = Column(Integer, primary_key=True)
    goal = Column(Text, nullable=False)
    type = Column(Text)
    status = Column(Text)
    target_date = Column(Date)
    progress_notes = Column(Text)
    embedding = Column(Vector(1536))
    updated_at = Column(DateTime(timezone=True))


class Relationships(Base):
    __tablename__ = "relationships"
    __table_args__ = {"schema": "identity"}

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    relationship_type = Column(Text)
    closeness = Column(Integer)
    shared_interests = Column(ARRAY(Text))
    birthday = Column(Date)
    contact_frequency = Column(Text)
    location = Column(Text)
    last_interacted = Column(Date)
    notes = Column(Text)
    embedding = Column(Vector(1536))
    updated_at = Column(DateTime(timezone=True))


class Projects(Base):
    __tablename__ = "projects"
    __table_args__ = {"schema": "identity"}

    id = Column(Integer, primary_key=True)
    project_name = Column(Text, nullable=False)
    project_type = Column(Text)
    status = Column(Text)
    description = Column(Text)
    tech_stack = Column(ARRAY(Text))
    role = Column(Text)
    goals = Column(ARRAY(Text))
    url = Column(Text)
    notes = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    embedding = Column(Vector(1536))
    updated_at = Column(DateTime(timezone=True))


class Skills(Base):
    __tablename__ = "skills"
    __table_args__ = {"schema": "identity"}

    id = Column(Integer, primary_key=True)
    skill_name = Column(Text, nullable=False)
    category = Column(Text)
    proficiency_level = Column(Integer)
    related_projects = Column(ARRAY(Integer))
    notes = Column(Text)
    embedding = Column(Vector(1536))
    updated_at = Column(DateTime(timezone=True))


class Interests(Base):
    __tablename__ = "interests"
    __table_args__ = {"schema": "identity"}

    id = Column(Integer, primary_key=True)
    interest_name = Column(Text, nullable=False)
    category = Column(Text)
    subcategory = Column(Text)
    description = Column(Text)
    examples = Column(ARRAY(Text))
    notes = Column(Text)
    embedding = Column(Vector(1536))
    updated_at = Column(DateTime(timezone=True))


class Routines(Base):
    __tablename__ = "routines"
    __table_args__ = {"schema": "identity"}

    id = Column(Integer, primary_key=True)
    routine_name = Column(Text, nullable=False)
    category = Column(Text)
    trigger = Column(Text)
    steps = Column(JSONB)
    frequency = Column(Text)
    is_active = Column(Boolean)
    streak_count = Column(Integer)
    updated_at = Column(DateTime(timezone=True))


class Finances(Base):
    __tablename__ = "finances"
    __table_args__ = {"schema": "identity"}

    id = Column(Integer, primary_key=True)
    category = Column(Text)
    item_name = Column(Text)
    amount = Column(Numeric)
    priority_rank = Column(Integer)
    frequency = Column(Text)
    status = Column(Text)
    notes = Column(Text)
    updated_at = Column(DateTime(timezone=True))


class Health(Base):
    __tablename__ = "health"
    __table_args__ = {"schema": "identity"}

    id = Column(Integer, primary_key=True)
    height = Column(Text)
    weight = Column(Text)
    blood_type = Column(Text)
    dietary_restrictions = Column(ARRAY(Text))
    allergies = Column(ARRAY(Text))
    medications = Column(ARRAY(Text))
    sleep_schedule = Column(Text)
    avg_sleep_hours = Column(Numeric)
    body_fat_percent = Column(Text)
    notes = Column(Text)
    updated_at = Column(DateTime(timezone=True))
