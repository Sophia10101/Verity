-- Fixes "permission denied for table ..." errors: RLS policies control
-- which rows a role can see, but Postgres also requires base table-level
-- grants before it evaluates those policies at all. 0001_init.sql was
-- missing these; this brings an already-applied 0001 up to date.

grant usage on schema public to authenticated;
grant select, insert on public.financial_profiles to authenticated;
grant select, insert on public.behavioral_responses to authenticated;
grant select, insert on public.risk_scores to authenticated;
grant select, insert on public.portfolios to authenticated;
grant select, insert on public.simulation_results to authenticated;
