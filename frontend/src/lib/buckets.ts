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

export const MONTHLY_CONTRIBUTION_BUCKETS: BucketOption[] = [
  { label: "$0 – $100", value: 50 },
  { label: "$100 – $250", value: 175 },
  { label: "$250 – $500", value: 375 },
  { label: "$500 – $1,000", value: 750 },
  { label: "$1,000 – $2,500", value: 1750 },
  { label: "$2,500 – $5,000", value: 3750 },
  { label: "$5,000 – $10,000", value: 7500 },
  { label: "$10,000+", value: 12500 },
];

// Sentinel radio value for "I don't have a monthly goal." When selected,
// monthly_contribution_range is stored as null and estimated_monthly_contribution
// is derived from income instead (see estimateMonthlyContributionFromIncome).
export const NO_MONTHLY_GOAL = "no_monthly_goal";

// Common savings-rate benchmark used to derive a monthly contribution when
// the user has no specific monthly goal in mind.
const DEFAULT_SAVINGS_RATE = 0.15;

export function estimateMonthlyContributionFromIncome(
  estimatedAnnualIncome: number,
): number {
  return (estimatedAnnualIncome * DEFAULT_SAVINGS_RATE) / 12;
}

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
