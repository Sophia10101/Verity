"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client";
import { BEHAVIORAL_QUESTIONS } from "@/lib/questionnaire";

export default function QuestionnairePage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setPending(true);
    setError(null);

    const formData = new FormData(event.currentTarget);
    const raw_answers: Record<string, number> = {};
    for (const question of BEHAVIORAL_QUESTIONS) {
      raw_answers[question.id] = Number(formData.get(question.id));
    }

    const supabase = createClient();
    const {
      data: { user },
    } = await supabase.auth.getUser();

    if (!user) {
      setError("You must be logged in.");
      setPending(false);
      return;
    }

    const { error: insertError } = await supabase.from("behavioral_responses").insert({
      user_id: user.id,
      raw_answers,
    });

    setPending(false);

    if (insertError) {
      setError(insertError.message);
      return;
    }

    router.push("/results");
  }

  return (
    <div className="mx-auto w-full max-w-lg px-4 py-16">
      <h1 className="text-2xl font-semibold text-foreground">
        Behavioral questionnaire
      </h1>
      <p className="mt-1 text-sm text-foreground/60">
        There are no right answers — this helps us understand how you tend to
        react to risk and loss.
      </p>

      <form onSubmit={handleSubmit} className="mt-8 space-y-8">
        {BEHAVIORAL_QUESTIONS.map((question, index) => (
          <fieldset key={question.id}>
            <legend className="text-sm font-medium">
              {index + 1}. {question.prompt}
            </legend>
            <div className="mt-3 flex items-center justify-between gap-2">
              <span className="text-xs text-foreground/50">
                {question.scaleLabels[0]}
              </span>
              <div className="flex gap-3">
                {[1, 2, 3, 4, 5].map((value) => (
                  <label
                    key={value}
                    className="flex flex-col items-center gap-1 text-xs"
                  >
                    <input
                      type="radio"
                      name={question.id}
                      value={value}
                      required
                    />
                    {value}
                  </label>
                ))}
              </div>
              <span className="text-xs text-foreground/50">
                {question.scaleLabels[1]}
              </span>
            </div>
          </fieldset>
        ))}

        {error && <p className="text-sm text-red-600 dark:text-red-400">{error}</p>}

        <button
          type="submit"
          disabled={pending}
          className="w-full rounded-md bg-foreground px-3 py-2 text-sm font-medium text-background disabled:opacity-60"
        >
          {pending ? "Saving…" : "See my results"}
        </button>
      </form>
    </div>
  );
}
