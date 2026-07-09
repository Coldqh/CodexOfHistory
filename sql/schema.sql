-- CODEX OF HISTORY MVP v0.1
-- Scalable schema for cards, graph relations, campaigns, missions, quizzes and user progress.
-- Target: PostgreSQL / Supabase.

create extension if not exists pgcrypto;

-- ENUMS
create type card_type as enum (
  'PERSON','EVENT','BATTLE','STATE','EMPIRE','DYNASTY','IDEA','RELIGION','BOOK','CITY','CULTURE','ARTIFACT','ERA','FACTION','LAW','TERM','MYTH','SOURCE'
);

create type card_rarity as enum ('COMMON','RARE','EPIC','LEGENDARY','MYTHIC');
create type verification_status as enum ('DRAFT','NEEDS_REVIEW','FACT_CHECKED','PUBLISHED','ARCHIVED','DISPUTED');
create type relation_type as enum (
  'CAUSE','CONSEQUENCE','ALLY','ENEMY','PART_OF','RULED_BY','FOUNDED_BY','INFLUENCED','CONFLICT_WITH','LOCATED_IN','SAME_ERA','DYNASTIC_LINK','RELIGIOUS_LINK','CULTURAL_LINK','ECONOMIC_LINK','MILITARY_LINK','MYTH_VS_FACT','SOURCE_FOR','PRECEDES','FOLLOWS','COMMANDER_IN'
);

-- CONTENT CORE
create table eras (
  id text primary key,
  title text not null,
  date_start text,
  date_end text,
  description text
);

create table regions (
  id text primary key,
  title text not null,
  parent_region_id text references regions(id)
);

create table cards (
  id text primary key,
  slug text unique not null,
  type card_type not null,
  title text not null,
  subtitle text,
  era_id text references eras(id),
  region_id text references regions(id),
  date_start text,
  date_end text,
  date_precision text default 'unknown',
  date_label text,
  summary text not null,
  importance text,
  rarity card_rarity not null default 'COMMON',
  difficulty int not null default 1 check (difficulty between 1 and 10),
  verification_status verification_status not null default 'DRAFT',
  version int not null default 1,
  search_text tsvector generated always as (
    setweight(to_tsvector('simple', coalesce(title,'')), 'A') ||
    setweight(to_tsvector('simple', coalesce(subtitle,'')), 'B') ||
    setweight(to_tsvector('simple', coalesce(summary,'')), 'C') ||
    setweight(to_tsvector('simple', coalesce(importance,'')), 'D')
  ) stored,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table card_attributes (
  card_id text primary key references cards(id) on delete cascade,
  attributes jsonb not null default '{}'::jsonb
);

create table card_stats (
  card_id text primary key references cards(id) on delete cascade,
  influence int check (influence between 0 and 10),
  complexity int check (complexity between 0 and 10),
  legacy int check (legacy between 0 and 10),
  military int check (military between 0 and 10),
  culture int check (culture between 0 and 10),
  politics int check (politics between 0 and 10),
  religion int check (religion between 0 and 10),
  economy int check (economy between 0 and 10),
  connections int check (connections between 0 and 10),
  source_reliability int check (source_reliability between 0 and 10)
);

create table card_facts (
  id uuid primary key default gen_random_uuid(),
  card_id text not null references cards(id) on delete cascade,
  fact_text text not null,
  fact_type text default 'core',
  is_disputed boolean not null default false,
  order_index int not null default 0
);

create table tags (
  id text primary key,
  title text not null,
  color text
);

create table card_tags (
  card_id text references cards(id) on delete cascade,
  tag_id text references tags(id) on delete cascade,
  primary key (card_id, tag_id)
);

-- GRAPH LAYER
create table card_relations (
  id text primary key,
  source_card_id text not null references cards(id) on delete cascade,
  target_card_id text not null references cards(id) on delete cascade,
  relation_type relation_type not null,
  strength int not null default 5 check (strength between 1 and 10),
  direction text not null default 'directed',
  description text,
  confidence int default 5 check (confidence between 1 and 10),
  source_id text,
  unique (source_card_id, target_card_id, relation_type)
);

-- SOURCES / FACTCHECK
create table sources (
  id text primary key,
  title text not null,
  author text,
  url text,
  source_type text,
  reliability text,
  language text,
  notes text
);

create table citations (
  id uuid primary key default gen_random_uuid(),
  card_id text references cards(id) on delete cascade,
  field_name text not null,
  source_id text references sources(id),
  note text,
  quote_short text
);

-- MEDIA
create table media_assets (
  id text primary key,
  card_id text references cards(id) on delete set null,
  type text not null,
  url text,
  local_path text,
  prompt text,
  license text,
  source text,
  style_tag text
);

-- MAP / TIMELINE
create table locations (
  id text primary key,
  title text not null,
  type text,
  latitude numeric,
  longitude numeric,
  ancient_name text,
  modern_name text,
  region_id text references regions(id)
);

create table card_locations (
  card_id text references cards(id) on delete cascade,
  location_id text references locations(id) on delete cascade,
  relation_type text not null,
  primary key (card_id, location_id, relation_type)
);

create table timeline_entries (
  id uuid primary key default gen_random_uuid(),
  card_id text references cards(id) on delete cascade,
  date_start text,
  date_end text,
  precision text,
  label text,
  importance int default 5 check (importance between 1 and 10)
);

-- CAMPAIGN LAYER
create table campaigns (
  id text primary key,
  slug text unique not null,
  title text not null,
  description text,
  era_id text references eras(id),
  region_id text references regions(id),
  difficulty int default 1 check (difficulty between 1 and 10),
  status text default 'DRAFT',
  cover_asset_id text references media_assets(id)
);

create table campaign_nodes (
  id text primary key,
  campaign_id text not null references campaigns(id) on delete cascade,
  node_type text not null,
  title text not null,
  order_index int not null,
  position_x int default 0,
  position_y int default 0,
  unlock_rules jsonb not null default '{}'::jsonb,
  completion_rules jsonb not null default '{}'::jsonb,
  reward_rules jsonb not null default '{}'::jsonb
);

create table campaign_node_cards (
  node_id text references campaign_nodes(id) on delete cascade,
  card_id text references cards(id) on delete cascade,
  role text default 'required',
  primary key (node_id, card_id)
);

create table missions (
  id text primary key,
  campaign_id text references campaigns(id) on delete cascade,
  node_id text references campaign_nodes(id) on delete cascade,
  title text not null,
  description text,
  mission_type text not null,
  required_actions jsonb not null default '[]'::jsonb,
  completion_rules jsonb not null default '{}'::jsonb,
  reward_rules jsonb not null default '{}'::jsonb
);

-- LESSONS
create table lessons (
  id text primary key,
  title text not null,
  campaign_id text references campaigns(id) on delete cascade,
  node_id text references campaign_nodes(id) on delete cascade,
  difficulty int default 1,
  estimated_minutes int default 5
);

create table lesson_blocks (
  id uuid primary key default gen_random_uuid(),
  lesson_id text not null references lessons(id) on delete cascade,
  block_type text not null,
  order_index int not null,
  content jsonb not null default '{}'::jsonb
);

-- STORY LAYER
create table story_episodes (
  id text primary key,
  campaign_id text references campaigns(id) on delete cascade,
  node_id text references campaign_nodes(id) on delete cascade,
  title text not null,
  text text not null,
  related_card_ids text[] default '{}',
  unlock_rules jsonb not null default '{}'::jsonb,
  choices jsonb not null default '[]'::jsonb
);

-- QUIZ ENGINE
create table quizzes (
  id text primary key,
  title text not null,
  related_card_id text references cards(id),
  difficulty int default 1 check (difficulty between 1 and 10),
  xp_reward int default 25
);

create table questions (
  id text primary key,
  quiz_id text references quizzes(id) on delete cascade,
  question_type text not null,
  related_card_id text references cards(id),
  difficulty int default 1 check (difficulty between 1 and 10),
  question_text text not null,
  answers jsonb not null,
  correct_answer jsonb not null,
  explanation text not null,
  source_id text references sources(id)
);

-- GAME LAYER
create table packs (
  id text primary key,
  title text not null,
  type text not null,
  era_id text references eras(id),
  region_id text references regions(id),
  rarity_rules jsonb not null default '{}'::jsonb
);

create table pack_drop_rules (
  id uuid primary key default gen_random_uuid(),
  pack_id text references packs(id) on delete cascade,
  card_type card_type,
  rarity card_rarity,
  weight int not null default 1,
  required_tags text[] default '{}',
  excluded_tags text[] default '{}'
);

-- USER LAYER
create table user_profiles (
  id uuid primary key default gen_random_uuid(),
  display_name text,
  xp int not null default 0,
  level int not null default 1,
  streak int not null default 0,
  created_at timestamptz default now()
);

create table user_card_progress (
  user_id uuid references user_profiles(id) on delete cascade,
  card_id text references cards(id) on delete cascade,
  is_unlocked boolean default false,
  is_read boolean default false,
  read_percent int default 0 check (read_percent between 0 and 100),
  quiz_mastery int default 0 check (quiz_mastery between 0 and 100),
  mastery_level int default 0 check (mastery_level between 0 and 5),
  favorite boolean default false,
  unlocked_at timestamptz,
  last_reviewed_at timestamptz,
  next_review_at timestamptz,
  primary key (user_id, card_id)
);

create table user_campaign_progress (
  user_id uuid references user_profiles(id) on delete cascade,
  campaign_id text references campaigns(id) on delete cascade,
  current_node_id text references campaign_nodes(id),
  completed_nodes text[] default '{}',
  unlocked_nodes text[] default '{}',
  completion_percent int default 0 check (completion_percent between 0 and 100),
  primary key (user_id, campaign_id)
);

create table user_quiz_attempts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references user_profiles(id) on delete cascade,
  quiz_id text references quizzes(id),
  score int not null,
  max_score int not null,
  answers jsonb not null default '[]'::jsonb,
  created_at timestamptz default now()
);

create table review_queue (
  user_id uuid references user_profiles(id) on delete cascade,
  card_id text references cards(id) on delete cascade,
  review_type text not null default 'card',
  due_at timestamptz not null,
  interval_days int default 1,
  ease_factor numeric default 2.5,
  last_result text,
  primary key (user_id, card_id, review_type)
);

-- INDEXES
create index idx_cards_type on cards(type);
create index idx_cards_rarity on cards(rarity);
create index idx_cards_difficulty on cards(difficulty);
create index idx_cards_era on cards(era_id);
create index idx_cards_region on cards(region_id);
create index idx_cards_search on cards using gin(search_text);
create index idx_card_attributes_json on card_attributes using gin(attributes);
create index idx_rel_source on card_relations(source_card_id);
create index idx_rel_target on card_relations(target_card_id);
create index idx_rel_type on card_relations(relation_type);
create index idx_campaign_nodes_campaign on campaign_nodes(campaign_id, order_index);
create index idx_user_card_progress_user on user_card_progress(user_id);
