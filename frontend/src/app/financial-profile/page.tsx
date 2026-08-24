"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client";
import {
  EXPERIENCE_LEVELS,
  GOAL_AMOUNT_BUCKETS,
  GOAL_TIMEFRAME_BUCKETS,
  INCOME_BUCKETS,
  midpointFor,
} from "@/lib/buckets";

export default function FinancialProfilePage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setPending(true);
    setError(null);

    const formData = new FormData(event.currentTarget);
    const age = Number(formData.get("age"));
    const income_range = String(formData.get("income_range"));
    const goal_amount_range = String(formData.get("goal_amount_range"));
    const goal_timeframe_range = String(formData.get("goal_timeframe_range"));
    const experience_level = String(formData.get("experience_level"));

    const supabase = createClient();
    const {
      data: { user },
    } = await supabase.auth.getUser();

    if (!user) {
      setError("You must be logged in.");
      setPending(false);
      return;
    }

    const { error: insertError } = await supabase.from("financial_profiles").insert({
      user_id: user.id,
      age,
      income_range,
      estimated_annual_income: midpointFor(INCOME_BUCKETS, income_range),
      goal_amount_range,
      estimated_goal_amount: midpointFor(GOAL_AMOUNT_BUCKETS, goal_amount_range),
      goal_timeframe_range,
      estimated_time_horizon_years: midpointFor(
        GOAL_TIMEFRAME_BUCKETS,
        goal_timeframe_range,
      ),
      experience_level,
    });

    setPending(false);

    if (insertError) {
      setError(insertError.message);
      return;
    }

    router.push("/questionnaire");
  }

  return (
    <div className="mx-auto w-full max-w-lg px-4 py-16">
      <h1 className="text-2xl font-semibold text-foreground">Financial profile</h1>
      <p className="mt-1 text-sm text-foreground/60">
        This helps us estimate how much risk your finances can support.
      </p>

      <form onSubmit={handleSubmit} className="mt-8 space-y-6">
        <div>
          <label htmlFor="age" className="block text-sm font-medium">
            Age
          </label>
          <input
            id="age"
            name="age"
            type="number"
            min={18}
            max={100}
            required
            className="mt-1 w-full rounded-md border border-black/10 bg-transparent px-3 py-2 text-sm outline-none focus:border-black/30 dark:border-white/15 dark:focus:border-white/30"
          />
        </div>

        <fieldset>
          <legend className="block text-sm font-medium">Annual income</legend>
          <div className="mt-2 space-y-2">
            {INCOME_BUCKETS.map((bucket) => (
              <label key={bucket.label} className="flex items-center gap-2 text-sm">
                <input
                  type="radio"
                  name="income_range"
                  value={bucket.label}
                  required
                />
                {bucket.label}
              </label>
            ))}
          </div>
        </fieldset>

        <fieldset>
          <legend className="block text-sm font-medium">Goal amount</legend>
          <div className="mt-2 space-y-2">
            {GOAL_AMOUNT_BUCKETS.map((bucket) => (
              <label key={bucket.label} className="flex items-center gap-2 text-sm">
                <input
                  type="radio"
                  name="goal_amount_range"
                  value={bucket.label}
                  required
                />
                {bucket.label}
              </label>
            ))}
          </div>
        </fieldset>

        <fieldset>
          <legend className="block text-sm font-medium">Goal timeframe</legend>
          <div className="mt-2 space-y-2">
            {GOAL_TIMEFRAME_BUCKETS.map((bucket) => (
              <label key={bucket.label} className="flex items-center gap-2 text-sm">
                <input
                  type="radio"
                  name="goal_timeframe_range"
                  value={bucket.label}
                  required
                />
                {bucket.label}
              </label>
            ))}
          </div>
        </fieldset>

        <fieldset>
          <legend className="block text-sm font-medium">Investing experience</legend>
          <div className="mt-2 space-y-2">
            {EXPERIENCE_LEVELS.map((level) => (
              <label key={level.value} className="flex items-center gap-2 text-sm">
                <input
                  type="radio"
                  name="experience_level"
                  value={level.value}
                  required
                />
                {level.label}
              </label>
            ))}
          </div>
        </fieldset>

        {error && <p className="text-sm text-red-600 dark:text-red-400">{error}</p>}

        <button
          type="submit"
          disabled={pending}
          className="w-full rounded-md bg-foreground px-3 py-2 text-sm font-medium text-background disabled:opacity-60"
        >
          {pending ? "Saving…" : "Continue to questionnaire"}
        </button>
      </form>
    </div>
  );
}
