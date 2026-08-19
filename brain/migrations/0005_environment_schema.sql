-- Physical rooms in Zachs living space
CREATE TABLE environment.rooms (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    floor TEXT,
    notes TEXT,
    updated_at TIMESTAMPTZ
);

-- Smart home devices Zach owns including lights, speakers and thermostats
CREATE TABLE environment.devices (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    brand TEXT,
    room_id INTEGER,
    device_address TEXT,
    integration_id INTEGER,
    notes TEXT,
    updated_at TIMESTAMPTZ,
    FOREIGN KEY (room_id) REFERENCES environment.rooms(id),
    FOREIGN KEY (integration_id) REFERENCES steve.integrations(id)
);

-- Furniture, fitness equipment and collectibles, combined by category and tracked per room
CREATE TABLE environment.items (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    item_name TEXT NOT NULL,
    category TEXT,
    brand TEXT,
    room_id INTEGER,
    quantity INTEGER,
    material TEXT[],
    condition TEXT,
    purchase_price NUMERIC,
    specs JSONB,
    notes TEXT,
    embedding VECTOR(1024),
    updated_at TIMESTAMPTZ,
    FOREIGN KEY (room_id) REFERENCES environment.rooms(id)
);

-- Important documents including passport, lease, insurance and expiry dates
CREATE TABLE environment.documents (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    location TEXT,
    expiry_date DATE,
    notes TEXT,
    updated_at TIMESTAMPTZ
);

-- Consumable supplies tracked by quantity with low stock alerts
CREATE TABLE environment.supplies (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    quantity INTEGER,
    low_stock_alert INTEGER,
    room_id INTEGER,
    notes TEXT,
    updated_at TIMESTAMPTZ,
    FOREIGN KEY (room_id) REFERENCES environment.rooms(id)
);

-- Pantry, fridge and freezer inventory with expiry tracking
CREATE TABLE environment.food (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    quantity TEXT,
    expiry_date DATE,
    low_stock_alert BOOLEAN,
    notes TEXT,
    updated_at TIMESTAMPTZ
);

-- Frequented places including coffee shops, gym, work and favourite spots
CREATE TABLE environment.locations (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    address TEXT,
    neighborhood TEXT,
    city TEXT,
    visit_frequency TEXT,
    favorite BOOLEAN,
    notes TEXT,
    embedding VECTOR(1024),
    updated_at TIMESTAMPTZ
);

-- Car info, service history, oil changes, tire rotations and upcoming maintenance
CREATE TABLE environment.vehicles (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    make TEXT,
    model TEXT,
    year INTEGER,
    vin TEXT,
    license_plate TEXT,
    mileage INTEGER,
    last_oil_change DATE,
    last_tire_rotation DATE,
    next_service_due DATE,
    insurance_provider TEXT,
    insurance_policy TEXT,
    notes TEXT,
    updated_at TIMESTAMPTZ
);
