-- Core THEA system settings including model, wake word, voice and behavior toggles
CREATE TABLE thea.config (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT,
    version TEXT,
    voice TEXT,
    response_style TEXT,
    wake_word TEXT,
    is_listening BOOLEAN,
    default_model TEXT,
    fast_model TEXT,
    max_context_tokens INTEGER,
    temperature NUMERIC,
    max_response_length INTEGER,
    location TEXT,
    timezone TEXT,
    units TEXT,
    privacy_mode BOOLEAN,
    do_not_disturb BOOLEAN,
    do_not_disturb_start TIME,
    do_not_disturb_end TIME,
    notes TEXT,
    updated_at TIMESTAMPTZ
);

-- System prompts per context that define how THEA thinks and responds
CREATE TABLE thea.prompts (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    context TEXT,
    prompt TEXT NOT NULL,
    active BOOLEAN NOT NULL,
    notes TEXT,
    updated_at TIMESTAMPTZ
);

-- External service connections including Notion, Spotify, Plaid and Google Calendar
CREATE TABLE thea.integrations (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT,
    enabled BOOLEAN,
    api_endpoint TEXT,
    auth_type TEXT,
    scopes TEXT[],
    last_synced TIMESTAMPTZ,
    status TEXT,
    notes TEXT,
    updated_at TIMESTAMPTZ
);

-- Functions THEA can call during conversations with confirmation requirements
CREATE TABLE thea.tools (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    integration_id INTEGER,
    schema JSONB,
    enabled BOOLEAN,
    requires_confirm BOOLEAN,
    notes TEXT,
    updated_at TIMESTAMPTZ,
    FOREIGN KEY (integration_id) REFERENCES thea.integrations(id)
);

-- Distilled episodic memories from conversations and ambient events, embedded for semantic recall (NOT YET IN LIVE SHEET -- sync it)
CREATE TABLE thea.memories (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(1536),
    occurred_at TIMESTAMPTZ,
    source TEXT,
    related_table TEXT,
    related_id INTEGER,
    salience INTEGER,
    notes TEXT,
    created_at TIMESTAMPTZ
);
