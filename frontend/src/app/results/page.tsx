import Link from "next/link";
import { createClient } from "@/lib/supabase/server";

export default async function ResultsPage() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  const { data: riskScore } = await supabase
    .from("risk_scores")
    .select("*")
    .eq("user_id", user!.id)
    .order("created_at", { ascending: false })
    .limit(1)
    .maybeSingle();

  const { data: portfolio } = riskScore
    ? await supabase
        .from("portfolios")
        .select("*")
        .eq("risk_score_id", riskScore.id)
        .order("created_at", { ascending: false })
        .limit(1)
        .maybeSingle()
    : { data: null };

  const { data: simulation } = portfolio
    ? await supabase
        .from("simulation_results")
        .select("*")
        .eq("portfolio_id", portfolio.id)
        .order("created_at", { ascending: false })
        .limit(1)
        .maybeSingle()
    : { data: null };

  if (!riskScore) {
    return (
      <div className="mx-auto w-full max-w-lg px-4 py-24 text-center">
        <h1 className="text-2xl font-semibold text-foreground">
          No results yet
        </h1>
        <p className="mt-2 text-sm text-foreground/60">
          The scoring pipeline hasn&apos;t been wired up yet (that&apos;s
          Phase 3). Once your financial profile and questionnaire are
          submitted, this page will show your risk score, recommended
          portfolio, and simulation results.
        </p>
        <Link
          href="/financial-profile"
          className="mt-6 inline-block rounded-md bg-foreground px-4 py-2 text-sm font-medium text-background"
        >
          Fill out your profile
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto w-full max-w-2xl px-4 py-16">
      <h1 className="text-2xl font-semibold text-foreground">Your results</h1>

      <section className="mt-8">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-foreground/50">
          Risk score
        </h2>
        <dl className="mt-3 grid grid-cols-2 gap-4 sm:grid-cols-4">
          <Stat label="Capacity" value={riskScore.capacity_score} />
          <Stat label="Behavioral" value={riskScore.behavioral_score} />
          <Stat label="Loss aversion" value={riskScore.loss_aversion_score} />
          <Stat label="Reconciled" value={riskScore.reconciled_score} />
        </dl>
        {riskScore.explanation_text && (
          <p className="mt-4 text-sm text-foreground/70">
            {riskScore.explanation_text}
          </p>
        )}
      </section>

      {portfolio && (
        <section className="mt-10">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-foreground/50">
            Recommended portfolio
          </h2>
          <pre className="mt-3 overflow-x-auto rounded-md bg-black/5 p-4 text-xs dark:bg-white/5">
            {JSON.stringify(portfolio.asset_weights, null, 2)}
          </pre>
        </section>
      )}

      {simulation && (
        <section className="mt-10">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-foreground/50">
            Simulation
          </h2>
          <dl className="mt-3 grid grid-cols-2 gap-4">
            <Stat
              label="Disciplined success prob."
              value={simulation.disciplined_success_prob}
            />
            <Stat
              label="Reactive success prob."
              value={simulation.reactive_success_prob}
            />
          </dl>
        </section>
      )}
    </div>
  );
}

function Stat({ label, value }: { label: string; value: number | null }) {
  return (
    <div>
      <dt className="text-xs text-foreground/50">{label}</dt>
      <dd className="text-lg font-medium text-foreground">{value ?? "—"}</dd>
    </div>
  );
}
