# Behavior-Aware Portfolio Advisor — Project Plan

**Legend:** 🗣️ = do this in a Claude chat (thinking, designing, learning) · 💻 = do this in Claude Code (writing/running actual code)

---

## Phase 1 — Plan the website (🗣️ Claude)

Do this whole phase in a normal Claude conversation before touching code. The goal is a clear enough spec that Claude Code can build fast without you having to make design decisions mid-build.

**Step 1 — Map out every page and the user flow**
Work with Claude to list every page/screen and what happens on each:
- Landing page (what it says, why someone signs up)
- Sign up / Login
- Onboarding questionnaire (financial demographics + behavioral/psychometric questions)
- Risk profile results page (capacity score vs. behavioral score, the "tension" explanation)
- Recommended portfolio page (allocation chart + "why" explanation)
- Simulation results page (Monte Carlo: disciplined vs. reactive investor, dollar behavior gap)
- Account/profile settings page
Sketch the flow: what's the very first thing a new user sees, and what's the path from signup to their final results?

**Step 2 — Design the database schema**
Decide on tables and key columns, e.g.:
- `users` (handled mostly by Supabase auth)
- `financial_profiles` (income, age, net worth, time horizon, goal amount, goal date)
- `behavioral_responses` (raw questionnaire answers)
- `risk_scores` (capacity score, behavioral score, reconciled score)
- `portfolios` (asset weights, expected return, expected volatility)
- `simulation_results` (percentile outcomes, probability of success, both scenarios)

**Step 3 — Design the API contract**
List the backend endpoints you'll need, e.g.:
- `POST /score-capacity` — demographics in, capacity score out
- `POST /score-behavioral` — questionnaire answers in, behavioral score + bias flags out
- `POST /reconcile` — both scores in, blended score + explanation out
- `POST /build-portfolio` — risk score in, asset weights out
- `POST /simulate` — portfolio + goal in, Monte Carlo results out (both scenarios)

**Step 4 — Write the actual questionnaire content**
Draft the real financial demographic questions and the behavioral questions (based on the Grable-Lytton scale + loss-aversion/overconfidence items). Having final question wording now avoids reworking forms later.

**Output of Phase 1:** a one-page spec (pages, schema, endpoints, questions) you can hand to Claude Code.

---

## Phase 2 — Build the base site (💻 Claude Code)

Goal: get a working skeleton — accounts, empty pages, a database, a backend that responds — deployed end-to-end before adding any real logic. This de-risks the "plumbing" so nothing structural breaks later.

**Step 5 — Scaffold the Next.js project** 💻
**Step 6 — Set up Supabase (auth + database)** 💻 — mostly automatic, a few manual clicks in the Supabase dashboard (creating the project, grabbing API keys)
**Step 7 — Create the database tables from Step 2** 💻 (SQL migration via Claude Code)
**Step 8 — Build empty page routes for every page from Step 1** 💻
**Step 9 — Scaffold the FastAPI backend with placeholder endpoints from Step 3** 💻
**Step 10 — Connect the questionnaire form to Supabase** (so answers actually save) 💻
**Step 11 — Deploy the skeleton** (Vercel + Render/Railway + Supabase) 💻 — confirm signup → login → fill form → data saved all works before adding real ML

**Checkpoint:** you should be able to sign up, log in, fill out a (non-functional) questionnaire, and see the data land in Supabase. Nothing smart happens yet — that's fine, that's the point.

---

## Phase 3 — Build the real logic (alternate 🗣️ Claude and 💻 Claude Code)

For each feature: design/understand it with Claude first, then implement with Claude Code. Don't skip the 🗣️ step — understanding *why* the model/logic works is the whole point of this project for you.

**Step 12 — Find and clean a risk-tolerance survey dataset**
🗣️ evaluate dataset options (SCF-based, Kaggle alternatives), decide what to keep
💻 write the cleaning/preprocessing script

**Step 13 — Train the risk capacity model**
🗣️ decide model type, features, evaluation metric — and understand what it's actually learning
💻 implement training script, save the trained model

**Step 14 — Build behavioral questionnaire scoring**
🗣️ design the scoring rubric (how raw answers become a loss-aversion score, overconfidence flag, etc.)
💻 implement the scoring function

**Step 15 — Build the reconciliation logic**
🗣️ design the rules: when capacity and behavioral scores diverge, what should the blended recommendation be, and how should the explanation be worded?
💻 implement it

**Step 16 — Wire Steps 13–15 into the FastAPI endpoints** 💻

**Step 17 — Build the portfolio optimizer**
🗣️ understand Modern Portfolio Theory / the efficient frontier, decide which asset classes (ETFs) to use
💻 implement with `PyPortfolioOpt`, pull historical data with `yfinance`

**Step 18 — Build the Monte Carlo simulation (disciplined investor)**
🗣️ understand the simulation approach (random return paths, percentile outcomes, probability of reaching goal)
💻 implement it

**Step 19 — Build the Monte Carlo simulation (reactive/behavioral investor)** *(cut first if time is tight)*
🗣️ design how a loss-aversion score translates into simulated panic-selling behavior in some paths
💻 implement it

**Step 20 — Build the results UI** (risk profile explanation, portfolio chart, simulation comparison chart)
🗣️ help write clear, non-jargony explanation copy for the results
💻 build the actual charts/components

---

## Phase 4 — Polish, document, deploy

**Step 21 — End-to-end testing / bug fixing** 💻
**Step 22 — Write the README** 🗣️ (help explain the finance/psychology concepts clearly) — do the final polish yourself so it's in your voice
**Step 23 — Final deploy + get your live link** 💻
**Step 24 — (Stretch, only if time remains)** add the historical stress-test feature from earlier, or extra UI polish

---

## If time runs short, cut in this order
1. Step 19 (reactive investor simulation) — document it as "future work" instead
2. Step 24 (stretch stress-test feature)
3. UI polish — a plainer-looking but fully working app beats a beautiful broken one

## A note on tool switching
Anytime Claude Code gets something technically working but you don't understand *why* it works, or you're not sure if an approach is the right one, that's your cue to switch back to a Claude chat and ask before continuing. The building should never outrun your understanding — that's the whole point of this project being a learning tool, not just a deliverable.
