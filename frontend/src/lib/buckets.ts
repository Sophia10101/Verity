// Bucketed range options for the financial profile form, each mapped to a
// single representative numeric estimate (per database_schema.md: "Range
// buckets + derived numbers"). The UI shows the label; estimated_* columns
// store the number.

export type BucketOption = { label: string; value: number };

export const INCOME_BUCKETS: BucketOption[] = [
  { label: "Less than $30,000", value: 25000 },
  { label: "$30,000 – $50,000", value: 40000 },
  { label: "$50,000 – $75,000", value: 62500 },
  { label: "$75,000 – $100,000", value: 87500 },
  { label: "$100,000 – $150,000", value: 125000 },
  { label: "$150,000+", value: 175000 },
];

export const GOAL_AMOUNT_BUCKETS: BucketOption[] = [
  { label: "Less than $10,000", value: 7500 },
  { label: "$10,000 – $50,000", value: 30000 },
  { label: "$50,000 – $100,000", value: 75000 },
  { label: "$100,000 – $500,000", value: 300000 },
  { label: "$500,000+", value: 750000 },
];

export const GOAL_TIMEFRAME_BUCKETS: BucketOption[] = [
  { label: "Less than 5 years", value: 3 },
  { label: "5–10 years", value: 7 },
  { label: "10–20 years", value: 15 },
  { label: "20+ years", value: 25 },
];

export const EXPERIENCE_LEVELS = [
  { label: "None", value: "none" },
  { label: "Some", value: "some" },
  { label: "Experienced", value: "experienced" },
] as const;

// Maps to the sector tags on the individual stocks in the portfolio
// optimizer's asset universe. Used to pick which stocks to consider for a
// given user; an empty selection means "open to anything."
export const INDUSTRY_OPTIONS = [
  "Technology",
  "Healthcare",
  "Financials",
  "Energy",
  "Consumer / Retail",
  "Communication / Media",
  "Utilities",
] as const;

export function midpointFor(buckets: BucketOption[], label: string): number {
  const match = buckets.find((b) => b.label === label);
  if (!match) {
    throw new Error(`Unknown bucket label: ${label}`);
  }
  return match.value;
}
