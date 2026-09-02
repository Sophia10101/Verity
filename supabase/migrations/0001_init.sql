-- Verity — initial schema
-- Tables and RLS policies for database_schema.pdf.
--
-- `users` is not created here: Supabase Auth already maintains `auth.users`
-- with `id` and `email`, and every table below references it directly.
--
-- Design principles from the schema doc, reflected below:
--   - History over overwrite: no UPDATE/DELETE policies on result tables —
--     retakes insert new rows.
--   - JSONB for flexible data: raw_answers, asset_weights, percentiles.
--   - Chained references: financial/behavioral -> risk_scores -> portfolios
--     -> simulation_results.
--   - Range buckets + derived numbers: *_range (text) alongside
--     estimated_* (numeric) on financial_profiles.

create extension if not exists "pgcrypto";

-- financial_profiles ---------------------------------------------------

create table if not exists public.financial_profiles (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  age int not null,
  income_range text not null,
  estimated_annual_income numeric not null,
  goal_amount_range text not null,
  estimated_goal_amount numeric not null,
  goal_timeframe_range text not null,
  estimated_time_horizon_years int not null,
  experience_level text not null check (experience_level in ('none', 'some', 'experienced')),
  industry_interests jsonb not null default '[]'::jsonb,
  monthly_contribution_range text,
  estimated_monthly_contribution numeric not null,
  created_at timestamptz not null default now()
);

create index if not exists financial_profiles_user_id_idx
  on public.financial_profiles (user_id, created_at desc);

alter table public.financial_profiles enable row level security;

create policy "financial_profiles: select own rows"
  on public.financial_profiles for select
  to authenticated
  using (auth.uid() = user_id);

create policy "financial_profiles: insert own rows"
  on public.financial_profiles for insert
  to authenticated
  with check (auth.uid() = user_id);

-- behavioral_responses ---------------------------------------------------

create table if not exists public.behavioral_responses (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  raw_answers jsonb not null,
  created_at timestamptz not null default now()
);

create index if not exists behavioral_responses_user_id_idx
  on public.behavioral_responses (user_id, created_at desc);

alter table public.behavioral_responses enable row level security;

create policy "behavioral_responses: select own rows"
  on public.behavioral_responses for select
  to authenticated
  using (auth.uid() = user_id);

create policy "behavioral_responses: insert own rows"
  on public.behavioral_responses for insert
  to authenticated
  with check (auth.uid() = user_id);

-- risk_scores ---------------------------------------------------

create table if not exists public.risk_scores (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  capacity_score numeric not null,
  behavioral_score numeric not null,
  loss_aversion_score numeric not null,
  reconciled_score numeric not null,
  explanation_text text not null,
  created_at timestamptz not null default now()
);

create index if not exists risk_scores_user_id_idx
  on public.risk_scores (user_id, created_at desc);

alter table public.risk_scores enable row level security;

create policy "risk_scores: select own rows"
  on public.risk_scores for select
  to authenticated
  using (auth.uid() = user_id);

create policy "risk_scores: insert own rows"
  on public.risk_scores for insert
  to authenticated
  with check (auth.uid() = user_id);

-- portfolios ---------------------------------------------------

create table if not exists public.portfolios (
  id uuid primary key default gen_random_uuid(),
  risk_score_id uuid not null references public.risk_scores (id) on delete cascade,
  asset_weights jsonb not null,
  expected_return numeric not null,
  expected_volatility numeric not null,
  sharpe_ratio numeric not null,
  created_at timestamptz not null default now()
);

create index if not exists portfolios_risk_score_id_idx
  on public.portfolios (risk_score_id, created_at desc);

alter table public.portfolios enable row level security;

create policy "portfolios: select own rows"
  on public.portfolios for select
  to authenticated
  using (
    exists (
      select 1 from public.risk_scores rs
      where rs.id = portfolios.risk_score_id
        and rs.user_id = auth.uid()
    )
  );

create policy "portfolios: insert own rows"
  on public.portfolios for insert
  to authenticated
  with check (
    exists (
      select 1 from public.risk_scores rs
      where rs.id = portfolios.risk_score_id
        and rs.user_id = auth.uid()
    )
  );

-- simulation_results ---------------------------------------------------

create table if not exists public.simulation_results (
  id uuid primary key default gen_random_uuid(),
  portfolio_id uuid not null references public.portfolios (id) on delete cascade,
  disciplined_percentiles jsonb not null,
  reactive_percentiles jsonb not null,
  disciplined_success_prob numeric not null,
  reactive_success_prob numeric not null,
  behavior_gap_dollars numeric not null,
  created_at timestamptz not null default now()
);

create index if not exists simulation_results_portfolio_id_idx
  on public.simulation_results (portfolio_id, created_at desc);

alter table public.simulation_results enable row level security;

create policy "simulation_results: select own rows"
  on public.simulation_results for select
  to authenticated
  using (
    exists (
      select 1 from public.portfolios p
      join public.risk_scores rs on rs.id = p.risk_score_id
      where p.id = simulation_results.portfolio_id
        and rs.user_id = auth.uid()
    )
  );

create policy "simulation_results: insert own rows"
  on public.simulation_results for insert
  to authenticated
  with check (
    exists (
      select 1 from public.portfolios p
      join public.risk_scores rs on rs.id = p.risk_score_id
      where p.id = simulation_results.portfolio_id
        and rs.user_id = auth.uid()
    )
  );

-- grants ---------------------------------------------------
-- RLS policies control *which* rows a role can see; Postgres also requires
-- base table-level grants before it will evaluate those policies at all.

grant usage on schema public to authenticated;
grant select, insert on public.financial_profiles to authenticated;
grant select, insert on public.behavioral_responses to authenticated;
grant select, insert on public.risk_scores to authenticated;
grant select, insert on public.portfolios to authenticated;
grant select, insert on public.simulation_results to authenticated;
