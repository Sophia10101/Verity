// Placeholder behavioral questionnaire content (Grable-Lytton-style risk
// tolerance items plus loss-aversion / overconfidence probes). Project plan
// Step 4 calls for finalized question wording in Phase 1/3 — swap this array
// out then. Answers are stored as-is in behavioral_responses.raw_answers.

export type QuestionnaireItem = {
  id: string;
  prompt: string;
  // 1 = strongly disagree / most conservative, 5 = strongly agree / most risk-seeking
  scaleLabels: [string, string];
};

export const BEHAVIORAL_QUESTIONS: QuestionnaireItem[] = [
  {
    id: "q1",
    prompt:
      "In general, how would you describe your willingness to take financial risks?",
    scaleLabels: ["Not at all willing", "Very willing"],
  },
  {
    id: "q2",
    prompt:
      "If a friend recommended an investment, you'd want to research it thoroughly before committing money.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
  {
    id: "q3",
    prompt:
      "Imagine your investments lost 20% of their value in a single month. How likely are you to sell to prevent further losses?",
    scaleLabels: ["Very unlikely to sell", "Very likely to sell"],
  },
  {
    id: "q4",
    prompt:
      "I would rather have a smaller, guaranteed gain than a chance at a much larger but uncertain gain.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
  {
    id: "q5",
    prompt:
      "I'm confident I can pick investments that will outperform the overall market.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
  {
    id: "q6",
    prompt:
      "Losing money makes me feel worse than gaining the same amount makes me feel good.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
  {
    id: "q7",
    prompt:
      "When investment values drop, I tend to check my accounts more frequently than usual.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
];
