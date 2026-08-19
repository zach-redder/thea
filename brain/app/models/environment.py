# Auto-generated from THEA DB.xlsx via app/schema_reader.py. Do not hand-edit; re-run generate_models.py.

from pgvector.sqlalchemy import Vector
from sqlalchemy import ARRAY, Boolean, Column, Date, DateTime, Integer, Numeric, Text
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import Base


class Rooms(Base):
    __tablename__ = "rooms"
    __table_args__ = {"schema": "environment"}

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    floor = Column(Text)
    notes = Column(Text)
    updated_at = Column(DateTime(timezone=True))


class Items(Base):
    __tablename__ = "items"
    __table_args__ = {"schema": "environment"}

    id = Column(Integer, primary_key=True)
    item_name = Column(Text, nullable=False)
    category = Column(Text)
    brand = Column(Text)
    room_id = Column(Integer)
    quantity = Column(Integer)
    material = Column(ARRAY(Text))
    condition = Column(Text)
    purchase_price = Column(Numeric)
    specs = Column(JSONB)
    notes = Column(Text)
    embedding = Column(Vector(1536))
    updated_at = Column(DateTime(timezone=True))


class Devices(Base):
    __tablename__ = "devices"
    __table_args__ = {"schema": "environment"}

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    type = Column(Text)
    brand = Column(Text)
    room_id = Column(Integer)
    device_address = Column(Text)
    integration_id = Column(Integer)
    notes = Column(Text)
    updated_at = Column(DateTime(timezone=True))


class Documents(Base):
    __tablename__ = "documents"
    __table_args__ = {"schema": "environment"}

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    category = Column(Text)
    location = Column(Text)
    expiry_date = Column(Date)
    notes = Column(Text)
    updated_at = Column(DateTime(timezone=True))


class Supplies(Base):
    __tablename__ = "supplies"
    __table_args__ = {"schema": "environment"}

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    category = Column(Text)
    quantity = Column(Integer)
    low_stock_alert = Column(Integer)
    room_id = Column(Integer)
    notes = Column(Text)
    updated_at = Column(DateTime(timezone=True))


class Food(Base):
    __tablename__ = "food"
    __table_args__ = {"schema": "environment"}

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    category = Column(Text)
    quantity = Column(Text)
    expiry_date = Column(Date)
    low_stock_alert = Column(Boolean)
    notes = Column(Text)
    updated_at = Column(DateTime(timezone=True))


class Locations(Base):
    __tablename__ = "locations"
    __table_args__ = {"schema": "environment"}

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    category = Column(Text)
    address = Column(Text)
    neighborhood = Column(Text)
    city = Column(Text)
    visit_frequency = Column(Text)
    favorite = Column(Boolean)
    notes = Column(Text)
    embedding = Column(Vector(1536))
    updated_at = Column(DateTime(timezone=True))


class Vehicles(Base):
    __tablename__ = "vehicles"
    __table_args__ = {"schema": "environment"}

    id = Column(Integer, primary_key=True)
    make = Column(Text)
    model = Column(Text)
    year = Column(Integer)
    vin = Column(Text)
    license_plate = Column(Text)
    mileage = Column(Integer)
    last_oil_change = Column(Date)
    last_tire_rotation = Column(Date)
    next_service_due = Column(Date)
    insurance_provider = Column(Text)
    insurance_policy = Column(Text)
    notes = Column(Text)
    updated_at = Column(DateTime(timezone=True))
