-- Core personal facts about Zach including name, age, occupation and education
CREATE TABLE identity.profile (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT,
    gender TEXT,
    date_of_birth DATE,
    age INTEGER,
    location TEXT,
    hometown TEXT,
    occupation TEXT,
    employer TEXT,
    education_level TEXT,
    languages TEXT[],
    nationality TEXT,
    description TEXT,
    updated_at TIMESTAMPTZ
);

-- Personality traits, values, communication style, motivators and drainers
CREATE TABLE identity.personality (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    personality_traits TEXT[],
    core_values TEXT[],
    communication_styles TEXT,
    thinking_style TEXT,
    strengths TEXT[],
    weaknesses TEXT[],
    love_languages TEXT[],
    motivators TEXT[],
    drainers TEXT[],
    notes TEXT,
    updated_at TIMESTAMPTZ
);

-- Visual preferences, design sensibility, color palette and aesthetic influences
CREATE TABLE identity.aesthetics (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    visual_style TEXT,
    interior_style TEXT[],
    color_palette TEXT[],
    design_sensibility TEXT,
    influences TEXT[],
    avoid TEXT[],
    notes TEXT,
    updated_at TIMESTAMPTZ
);

-- Current life chapter including headspace, tone, focus, challenges, energy level and working style
CREATE TABLE identity.context (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    life_stage TEXT,
    current_headspace TEXT,
    living_situation TEXT,
    financial_situation TEXT,
    working_style TEXT,
    work_environment TEXT,
    tone TEXT,
    vocabulary TEXT,
    avoid_phrases TEXT[],
    humor_style TEXT,
    current_focus TEXT[],
    current_challenges TEXT[],
    energy_level TEXT,
    notes TEXT,
    updated_at TIMESTAMPTZ
);

-- Personal, professional, creative, financial and health goals with status and target dates
CREATE TABLE identity.goals (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    goal TEXT NOT NULL,
    type TEXT,
    status TEXT,
    target_date DATE,
    progress_notes TEXT,
    embedding VECTOR(1536),
    updated_at TIMESTAMPTZ
);

-- People in Zachs life including friends, family, colleagues and mentors
CREATE TABLE identity.relationships (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    relationship_type TEXT,
    closeness INTEGER,
    shared_interests TEXT[],
    birthday DATE,
    contact_frequency TEXT,
    location TEXT,
    last_interacted DATE,
    notes TEXT,
    embedding VECTOR(1536),
    updated_at TIMESTAMPTZ
);

-- Active and past side projects including projects for fun and startups
CREATE TABLE identity.projects (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_name TEXT NOT NULL,
    project_type TEXT,
    status TEXT,
    description TEXT,
    tech_stack TEXT[],
    role TEXT,
    goals TEXT[],
    url TEXT,
    notes TEXT,
    start_date DATE,
    end_date DATE,
    embedding VECTOR(1536),
    updated_at TIMESTAMPTZ
);

-- Technical, creative and philosophical skills with proficiency levels
CREATE TABLE identity.skills (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    skill_name TEXT NOT NULL,
    category TEXT,
    proficiency_level INTEGER,
    related_projects INTEGER[],
    notes TEXT,
    embedding VECTOR(1536),
    updated_at TIMESTAMPTZ
);

-- Hobbies, media, music, film and things Zach is into
CREATE TABLE identity.interests (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    interest_name TEXT NOT NULL,
    category TEXT,
    subcategory TEXT,
    description TEXT,
    examples TEXT[],
    notes TEXT,
    embedding VECTOR(1536),
    updated_at TIMESTAMPTZ
);

-- Daily routines and habits with triggers and steps
CREATE TABLE identity.routines (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    routine_name TEXT NOT NULL,
    category TEXT,
    trigger TEXT,
    steps JSONB,
    frequency TEXT,
    is_active BOOLEAN,
    streak_count INTEGER,
    updated_at TIMESTAMPTZ
);

-- Budget priorities and tracked subscriptions; live balances and transactions come from Plaid via thea.integrations
CREATE TABLE identity.finances (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category TEXT,
    item_name TEXT,
    amount NUMERIC,
    priority_rank INTEGER,
    frequency TEXT,
    status TEXT,
    notes TEXT,
    updated_at TIMESTAMPTZ
);

-- Allergies, medications, dietary restrictions, sleep and fitness context
CREATE TABLE identity.health (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    height TEXT,
    weight TEXT,
    blood_type TEXT,
    dietary_restrictions TEXT[],
    allergies TEXT[],
    medications TEXT[],
    sleep_schedule TEXT,
    avg_sleep_hours NUMERIC,
    body_fat_percent TEXT,
    notes TEXT,
    updated_at TIMESTAMPTZ
);
