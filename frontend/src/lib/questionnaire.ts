// Placeholder behavioral questionnaire content (Grable-Lytton-style risk
// tolerance items plus loss-aversion / overconfidence probes). Project plan
// Step 4 calls for finalized question wording in Phase 1/3, swap this array
// out then. Answers are stored as-is in behavioral_responses.raw_answers.
//
// q1-q10 are indirect psychological probes (impulsivity, regret sensitivity,
// need for certainty, gut vs. analysis, sensation seeking, herding, and
// follow-through), deliberately not about money, since people tend to
// answer money-framed questions aspirationally rather than honestly.
// q11-q17 are the original direct financial-risk items.

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
      "I often make decisions on the spur of the moment without thinking them through.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
  {
    id: "q2",
    prompt:
      "I find it hard to stick to a plan once something more exciting or urgent comes along.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
  {
    id: "q3",
    prompt: "I regret things I did more than things I didn't do.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
  {
    id: "q4",
    prompt:
      "I get uncomfortable when a plan doesn't have a clear, predictable outcome.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
  {
    id: "q5",
    prompt:
      "Not knowing how something will turn out is more stressful to me than knowing it'll turn out badly.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
  {
    id: "q6",
    prompt:
      "I trust my gut instinct over careful analysis when making an important decision.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
  {
    id: "q7",
    prompt: "I enjoy activities that involve an element of risk or unpredictability.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
  {
    id: "q8",
    prompt:
      "If most people around me are doing something, I assume it's probably the right call.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
  {
    id: "q9",
    prompt:
      "I feel more comfortable making a decision once I know others have made the same one.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
  {
    id: "q10",
    prompt: "Once I commit to something, I stick with it even when it gets uncomfortable.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
  {
    id: "q11",
    prompt:
      "In general, how would you describe your willingness to take financial risks?",
    scaleLabels: ["Not at all willing", "Very willing"],
  },
  {
    id: "q12",
    prompt:
      "If a friend recommended an investment, you'd want to research it thoroughly before committing money.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
  {
    id: "q13",
    prompt:
      "Imagine your investments lost 20% of their value in a single month. How likely are you to sell to prevent further losses?",
    scaleLabels: ["Very unlikely to sell", "Very likely to sell"],
  },
  {
    id: "q14",
    prompt:
      "I would rather have a smaller, guaranteed gain than a chance at a much larger but uncertain gain.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
  {
    id: "q15",
    prompt:
      "I'm confident I can pick investments that will outperform the overall market.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
  {
    id: "q16",
    prompt:
      "Losing money makes me feel worse than gaining the same amount makes me feel good.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
  {
    id: "q17",
    prompt:
      "When investment values drop, I tend to check my accounts more frequently than usual.",
    scaleLabels: ["Strongly disagree", "Strongly agree"],
  },
];
