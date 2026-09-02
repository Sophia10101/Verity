-- Adds the monthly contribution field the Monte Carlo simulation needs:
-- how much money is actually being invested over time, not just the goal
-- amount. monthly_contribution_range is nullable ("I don't have a monthly
-- goal" leaves it unset); estimated_monthly_contribution is always
-- populated, either from the bucket midpoint or derived from income
-- (15% of estimated annual income / 12) when no range was picked.
-- 0001_init.sql was updated for future fresh setups; this brings an
-- already-applied 0001 up to date.

alter table public.financial_profiles
  add column if not exists monthly_contribution_range text,
  add column if not exists estimated_monthly_contribution numeric not null default 0;

alter table public.financial_profiles
  alter column estimated_monthly_contribution drop default;
