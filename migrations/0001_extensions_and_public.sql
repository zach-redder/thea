-- Auto-generated from STEVE_DB sheet via app/schema_reader.py. Do not hand-edit; re-run generate_migrations.py.
CREATE EXTENSION IF NOT EXISTS vector;
CREATE SCHEMA IF NOT EXISTS public;
CREATE SCHEMA IF NOT EXISTS steve;
CREATE SCHEMA IF NOT EXISTS identity;
CREATE SCHEMA IF NOT EXISTS wardrobe;
CREATE SCHEMA IF NOT EXISTS environment;

-- Registry of all schemas in the STEVE database
CREATE TABLE public.schema_registry (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    schema_name TEXT,
    description TEXT,
    last_updated TIMESTAMPTZ
);

-- Registry of all tables across all schemas
CREATE TABLE public.table_registry (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    schema_id INTEGER,
    table_name TEXT,
    description TEXT,
    last_updated TIMESTAMPTZ,
    FOREIGN KEY (schema_id) REFERENCES public.schema_registry(id)
);

-- Registry of all columns across all tables
CREATE TABLE public.column_registry (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    table_id INTEGER,
    column_name TEXT NOT NULL,
    data_type TEXT,
    description TEXT,
    example_value TEXT,
    nullable BOOLEAN,
    last_updated TIMESTAMPTZ,
    FOREIGN KEY (table_id) REFERENCES public.table_registry(id)
);
