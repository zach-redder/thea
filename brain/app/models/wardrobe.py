# Auto-generated from THEA DB.xlsx via app/schema_reader.py. Do not hand-edit; re-run generate_models.py.

from pgvector.sqlalchemy import Vector
from sqlalchemy import ARRAY, Boolean, Column, Date, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import Base


class Clothing(Base):
    __tablename__ = "clothing"
    __table_args__ = {"schema": "wardrobe"}

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    brand = Column(Text)
    category = Column(Text)
    subcategory = Column(Text)
    color_primary = Column(Text)
    color_secondary = Column(Text)
    color_accent = Column(Text)
    material = Column(ARRAY(Text))
    pattern = Column(Text)
    silhouette = Column(Text)
    length = Column(Text)
    size_label = Column(Text)
    occasions = Column(ARRAY(Text))
    description = Column(Text)
    condition = Column(Text)
    owned = Column(Boolean)
    embedding = Column(Vector(1536))


class Shoes(Base):
    __tablename__ = "shoes"
    __table_args__ = {"schema": "wardrobe"}

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    brand = Column(Text)
    category = Column(Text)
    subcategory = Column(Text)
    color_primary = Column(Text)
    color_secondary = Column(Text)
    color_accent = Column(Text)
    material = Column(ARRAY(Text))
    silhouette = Column(Text)
    toe_shape = Column(Text)
    heel_type = Column(Text)
    size_us = Column(Text)
    occasions = Column(ARRAY(Text))
    description = Column(Text)
    condition = Column(Text)
    owned = Column(Boolean)
    embedding = Column(Vector(1536))


class Jewelry(Base):
    __tablename__ = "jewelry"
    __table_args__ = {"schema": "wardrobe"}

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    brand = Column(Text)
    category = Column(Text)
    subcategory = Column(Text)
    color_primary = Column(Text)
    material = Column(ARRAY(Text))
    stone_type = Column(Text)
    finish = Column(Text)
    dimensions = Column(Text)
    occasions = Column(ARRAY(Text))
    sentimental = Column(Boolean)
    description = Column(Text)
    condition = Column(Text)
    owned = Column(Boolean)
    embedding = Column(Vector(1536))


class Accessories(Base):
    __tablename__ = "accessories"
    __table_args__ = {"schema": "wardrobe"}

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    brand = Column(Text)
    category = Column(Text)
    subcategory = Column(Text)
    color_primary = Column(Text)
    color_secondary = Column(Text)
    color_accent = Column(Text)
    material = Column(ARRAY(Text))
    dimensions = Column(Text)
    occasions = Column(ARRAY(Text))
    description = Column(Text)
    condition = Column(Text)
    owned = Column(Boolean)
    specs = Column(JSONB)
    embedding = Column(Vector(1536))


class Outfits(Base):
    __tablename__ = "outfits"
    __table_args__ = {"schema": "wardrobe"}

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    occasion = Column(Text)
    shoe_id = Column(Integer)
    clothing_ids = Column(ARRAY(Integer))
    jewelry_ids = Column(ARRAY(Integer))
    accessory_ids = Column(ARRAY(Integer))
    notes = Column(Text)
    rating = Column(Integer)
    worn_count = Column(Integer)
    last_worn = Column(Date)
    embedding = Column(Vector(1536))
    updated_at = Column(DateTime(timezone=True))
