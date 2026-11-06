-- Tops, bottoms, outerwear and all clothing items with styling metadata
CREATE TABLE wardrobe.clothing (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT,
    brand TEXT,
    category TEXT,
    subcategory TEXT,
    color_primary TEXT,
    color_secondary TEXT,
    color_accent TEXT,
    material TEXT[],
    pattern TEXT,
    silhouette TEXT,
    length TEXT,
    size_label TEXT,
    occasions TEXT[],
    description TEXT,
    condition TEXT,
    owned BOOLEAN,
    embedding VECTOR(1536)
);

-- All footwear with style, silhouette and sizing details
CREATE TABLE wardrobe.shoes (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT,
    brand TEXT,
    category TEXT,
    subcategory TEXT,
    color_primary TEXT,
    color_secondary TEXT,
    color_accent TEXT,
    material TEXT[],
    silhouette TEXT,
    toe_shape TEXT,
    heel_type TEXT,
    size_us TEXT,
    occasions TEXT[],
    description TEXT,
    condition TEXT,
    owned BOOLEAN,
    embedding VECTOR(1536)
);

-- Rings, necklaces, bracelets and earrings with material and finish details
CREATE TABLE wardrobe.jewelry (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT,
    brand TEXT,
    category TEXT,
    subcategory TEXT,
    color_primary TEXT,
    material TEXT[],
    stone_type TEXT,
    finish TEXT,
    dimensions TEXT,
    occasions TEXT[],
    sentimental BOOLEAN,
    description TEXT,
    condition TEXT,
    owned BOOLEAN,
    embedding VECTOR(1536)
);

-- Bags, watches, sunglasses, gloves and other accessories
CREATE TABLE wardrobe.accessories (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT,
    brand TEXT,
    category TEXT,
    subcategory TEXT,
    color_primary TEXT,
    color_secondary TEXT,
    color_accent TEXT,
    material TEXT[],
    dimensions TEXT,
    occasions TEXT[],
    description TEXT,
    condition TEXT,
    owned BOOLEAN,
    specs JSONB,
    embedding VECTOR(1536)
);

-- Saved outfit combinations with ratings and wear history
CREATE TABLE wardrobe.outfits (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT,
    occasion TEXT,
    shoe_id INTEGER,
    clothing_ids INTEGER[],
    jewelry_ids INTEGER[],
    accessory_ids INTEGER[],
    notes TEXT,
    rating INTEGER,
    worn_count INTEGER,
    last_worn DATE,
    embedding VECTOR(1536),
    updated_at TIMESTAMPTZ,
    FOREIGN KEY (shoe_id) REFERENCES wardrobe.shoes(id)
);
