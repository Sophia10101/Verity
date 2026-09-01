-- Adds the industry-interest field for portfolio personalization: which
-- sectors the user wants represented among the individual stock picks
-- (empty array means "open to anything"). 0001_init.sql was updated to
-- include this column for future fresh setups; this brings an
-- already-applied 0001 up to date.

alter table public.financial_profiles
  add column if not exists industry_interests jsonb not null default '[]'::jsonb;
