-- Codex of History v0.2 notes
-- Static MVP uses inline JS + JSON exports.
-- For later Supabase/PostgreSQL migration, keep images as metadata, not hardcoded UI.

create table if not exists media_assets (
  id text primary key,
  card_id text not null,
  file_name text not null,
  source_url text,
  caption text,
  credit text,
  license text,
  created_at timestamptz default now()
);

create table if not exists localizations (
  id text primary key,
  entity_type text not null,
  entity_id text not null,
  locale text not null,
  field_name text not null,
  value text not null
);
