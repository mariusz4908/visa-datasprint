# CardFlow: storyline and evidence map

How the CardFlow pitch fits together, where each claim is backed by the **Visa transaction data**, where it relies on
**external sources** (GUS, NBP, Gemius) and where it is an **assumption**. Use it to build the 10 slides, the demo and
the answers to the jury.

Legend used below:
- **[VISA]**: measured in the Visa data (notebook in `ml_readiness/` given in brackets)
- **[EXT]**: external public source (collected in the existing CardFlow analysis)
- **[ASSUMPTION]**: scenario input, not measured

All Visa figures come from the synthetic hackathon dataset (305.5M transactions, Jan 2025 - Jun 2026). They
demonstrate the method; on real Visa data the same pipeline would produce the real numbers.

---

## The pitch in one sentence

> Almost half of all online card payments still require typing a 16-digit card number, and that friction decides
> whether a new online customer stays with the card. Visa QR Pay removes the typing, and our machine-learning
> targeting tells banks exactly who should get it first.

---

## Story arc (10 slides)

| # | Slide | Key message | Backed by |
|---|---|---|---|
| 1 | Title | CardFlow: turning Visa transaction data into card adoption online | - |
| 2 | The problem | Cards win in stores but lose online | [EXT] market shares + [VISA] 36% of active cards never pay online |
| 3 | Why: friction | Online card payments mean typing the card number, and it is getting worse | [VISA] |
| 4 | Why it matters | The first online payment decides whether the customer stays | [VISA] |
| 5 | Solution | Visa QR Pay: scan and approve, no typing | product concept |
| 6 | Who first (ML) | Two audiences + new cards, found in the data | [VISA] rules + ML model |
| 7 | The model | Readiness model: what it does, how well it works, what drives it | [VISA] ML |
| 8 | Rollout and business case | In-app QR for typers now, QR on every new card, pilot with control group | [VISA] inputs + [ASSUMPTION] economics |
| 9 | Recommendations | For banks, merchants, Visa | [VISA] |
| 10 | Summary | Prototype vs next steps | - |

---

## Slide by slide

### 2. The problem: cards lose online

- **[EXT]** Cards dominate at physical points of sale, while BLIK leads Polish e-commerce (Gemius 2024: BLIK 67%,
  cards 16%). Keep these as *market context*: the Visa data contain only Visa cards, so they cannot show BLIK.
- **[VISA]** 36% of active Polish cards never made an online card purchase in 18 months; 21% did so only occasionally
  (`wallet_online.ipynb`, 759k active cards).
- **[VISA + EXT]** Compared with GUS (share of retail sales made online, April 2026), card payments online capture only
  part of e-commerce: clothing 24.4% online (GUS) vs 11.8% card-online (Visa, Polish merchants); press/books 20.4% vs
  7.3%; furniture/electronics 20.2% vs 15.5%. *Caveat:* marketplace purchases have their own merchant code and GUS
  classifies enterprises differently, so the gap is indicative.

**Say it like this:** "The card is in everyone's wallet, but a third of active cards never go online."

### 3. Why: friction at checkout

All **[VISA]** (`wallet_online.ipynb`, `ml_readiness` exploration):
- **45% of online card payments are a typed card number** (entry mode "Manual key entry"), not a saved card, and the
  share is **growing** (42% in early 2025 -> 45% in 2026).
- Typing is growing fastest where volume is highest: online marketplaces 58% -> 67%, taxi / ride-hailing 47% -> 57%
  (Polish merchants, H1 2025 vs H1 2026).
- **Polish merchants have more friction than foreign ones** in most large categories: travel agencies 97% typed vs 68%
  abroad, digital games 55% vs 18%, pay TV 37% vs 4%, restaurants 74% vs 57%.
- **The most digital customers type the most**: cards that pay mostly by phone in store type the card number *on a
  phone* in 49% of their online payments (3% for cards that never use a phone in store). They already have the card
  in a digital wallet, yet type it into a small screen.

**Say it like this:** "The problem is not the card. The problem is typing 16 digits and a CVV on a phone."

### 4. Why it matters: the first online payment decides

All **[VISA]** (`wallet_online.ipynb`):
- After a **first online payment made with a saved card (one-click)**, 45% keep paying online in at least 3 of the
  next 6 months; after a **typed** first payment only 31%. 25% vs 37% never pay online by card again.
- Honest version: part of this gap comes from *what* was bought (subscriptions are one-click by nature). **Within the
  same first-purchase category the advantage is +4 pp** (positive in 14 of 22 categories; electronics +45 pp,
  apps +16 pp, telecom +14 pp). Use +4 pp as the conservative and +14 pp as the optimistic effect.
- Friction matters at the **start**, not later: established online card users keep paying online (94-97%) whether
  they type or not.
- **New cards decide fast**: a card's chance of a first online payment is 28% in its first month, 18% in the second,
  10% in the third and below 5% after half a year. 49% of new cards pay online within 3 months and **70% of those first
  online payments are typed** (`target_audiences.ipynb`).

**Say it like this:** "If the first online payment is effortless, the customer stays. Today 7 out of 10 first online
payments of a new card are typed."

### 5. Solution: Visa QR Pay

Product concept (see `cardflow_app.py`, page "Visa QR Pay"). Data-driven requirement to add:
- **[VISA]** 86% of typed payments of the main audience happen **on a phone**, and 93% of the heaviest typers pay by
  phone in store. **QR Pay must work from the banking app / phone wallet**, not only from a QR printed on the plastic card.

### 6. Who first: audiences found in the data

**[VISA]** `target_audiences.ipynb`, active cards Jan-Jun 2026:

| Audience | Cards | Share of active cards | Share of typed online payments | Role |
|---|---|---|---|---|
| **A: mostly typing** (rule) | 190k | 22% | **80%** | **Wave 1**: QR in the banking app replaces 2.8 typed payments per card per month |
| **New cards** (overlay) | ~27k per month | 3% per month | - | **From issuance**: QR on every new card, first online payment without typing |
| **C: ready to start** (ML model) | 58k | 7% | - | **Wave 2**: ~14% will make a first online payment within 3 months; make it a QR payment |
| D: sometimes typing | 151k | 17% | 20% | wave 3 |
| E: not ready / F: already one-click / L: lapsed | 480k | 55% | 0% | not targeted |

- Contact order inside A: the heaviest 20% of typers (38k cards) make **63%** of the audience's typing.
- Where A types: online marketplaces 17%, taxi 17%, public transport tickets 11%, digital content 7%, food delivery 6%,
  fashion 5%. Marketplaces, tickets and food delivery are mostly Polish merchants (76-97%): the first QR merchants.
- Why A first and not only new cards: in year one A offers roughly **7x more typed payments to replace** (~537k per
  month immediately vs ~70k per month on average from new cards), the effect is measurable within weeks, and in-app QR
  needs no card re-issue. New cards are the cheapest way to **scale and build the habit**. Use both.

### 7. The model (the AI part)

**[VISA] machine learning** (`readiness_model.ipynb`, `ai_experiments.ipynb`). Explain it in three lines:

1. **What it does:** for every card that has never paid online, it estimates the chance of a first online card payment
   in the next 3 months, using only its in-store behaviour.
2. **How well:** tested on three later periods it had never seen (Oct 2025, Jan 2026, Apr 2026): AUC 0.74-0.76; the
   top 10% of cards start **3.5x** more often than an average card; the top 20% contain **55%** of all future
   starters. Probabilities are calibrated (predicted 4.9% = actual 4.9%). It beats logistic regression and a simple
   phone-use rule in every period.
3. **What drives it (SHAP):** a **new card** (first 90 days), **any phone payment in store**, evening activity, fast food
   and restaurants, fuel, public transport, payments abroad, money transfers / top-ups. Not how much people spend.

Supporting elements:
- **6 personas** (KMeans on in-store behaviour): phone-first city, travellers, active all-rounders, home & car,
  mall shoppers, everyday grocery. 61% of audience A is "phone-first city". Inside low-adoption personas the model still
  finds ready cards (its top picks start at 15-16% vs a 3% persona average), which persona targeting alone would miss.
- **What we tested and dropped:** a first-purchase recommender (did not beat a popularity list). Showing this makes the
  model choice credible.

**Say it like this:** "The model is the targeting engine: out of 340k cards that do not pay online yet, it points to
the one in five where more than half of the future online customers are."

**Positioning:** the model is **not** the heart of the pitch (the friction is). The model makes the rollout efficient
and measurable, and it is the only part of the project that is machine learning trained and validated on Visa data.

### 8. Rollout and business case

- **Now:** in-app QR for audience A, starting with the heaviest 20% of typers.
- **From issuance:** QR on every new card (~3% of active cards per month).
- **Wave 2:** model-selected ready cards (audience C) get QR at their first online payment.
- **Pilot design:** inside each audience the bank keeps a random ~10% without the campaign (control group). This
  measures what QR itself adds, which the data cannot tell today.
- **Business case** (`models.py`): keep the scenario simulation but **label it as a simulation**, not as predictive
  models, and replace assumptions with data where possible. `ml_readiness/results/target_audiences.json`
  (`roi_inputs`) provides:
  - audience sizes as shares of active cards (scale to the real Polish card base instead of an assumed 8M TAM),
  - online and typed payments per card per month for each audience,
  - expected first online payments of audience C,
  - new cards per month and their online start rate,
  - the retention effect of a one-click first payment (+4 pp conservative, +14 pp optimistic).
- Fees, costs, BLIK cannibalisation and adoption speed (Bass p, q) remain **[ASSUMPTION]**; say so on the slide.

Optional appendix: pilot regions with matched control regions (`pilot_regions.ipynb`): Warszawa vs Gdansk and
Wroclaw vs Poznan for replacing typing; Katowice vs Rzeszow and Lodz vs Lublin for first online payments.

### 9. Recommendations (all backed by [VISA])

- **Banks:** launch in-app QR for card numbers typed on phones; target the heaviest typers first; add QR to the
  onboarding of every new card (first 90 days).
- **Merchants / acquirers:** start QR checkout where typing is highest and volume is Polish: marketplaces, public
  transport tickets, food delivery; then travel and fashion, where Polish merchants lose to foreign ones on convenience.
- **Visa:** measure success as the share of first online payments made without typing (today 30% for new cards) and
  as the typing share of audience A (today 77%).

### 10. Prototype vs next steps

- **Working prototype:** data pipeline (DuckDB), friction analysis, readiness model with backtest, audiences, personas,
  pilot selection, dashboard.
- **Needs further development:** a real pilot with control groups (effect of QR itself), real (non-synthetic) data,
  QR product and merchant integration, economics with real fees and costs.

---

## Evidence map: claim -> source

| Claim | Type | Source |
|---|---|---|
| BLIK 67% / cards 16% of Polish e-commerce | [EXT] | Gemius 2024 (existing CardFlow analysis) |
| 36% of active cards never pay online by card | [VISA] | `wallet_online.ipynb` |
| 45% of online card payments are typed, growing | [VISA] | `wallet_online.ipynb`, exploration |
| Polish merchants type more than foreign | [VISA] | exploration (category x merchant country) |
| 49% of phone-first users' online payments typed on a phone | [VISA] | `wallet_online.ipynb` |
| One-click first payment: 45% vs 31% retained (+4 pp same category) | [VISA] | `wallet_online.ipynb` |
| New cards: 70% of first online payments typed | [VISA] | `target_audiences.ipynb` |
| Audience A: 190k cards, 80% of typing, 86% on phone | [VISA] | `target_audiences.ipynb` |
| Model: AUC 0.74-0.76, lift 3.5x, calibrated | [VISA] ML | `readiness_model.ipynb` |
| GUS online share vs card online share by category | [VISA + EXT] | GUS monthly retail release; mapping in `ml_readiness` exploration |
| 7.7M adopters, ROI 365%, break-even month 16 | [ASSUMPTION] | `models.py` scenario simulation |

---

## Claims to reword or drop

| Current wording | Issue | Suggestion |
|---|---|---|
| "6 predictive models" | they are scenario simulations with hand-set parameters | "Business case simulation (3 scenarios)", and present the ML model as the predictive part |
| "Cards are displaced by BLIK" as a finding | Visa data cannot see BLIK | keep as market context [EXT]; the finding from Visa data is friction |
| P2P use cases as a data finding | no P2P payments in the Visa data | keep P2P as a product vision, not as evidence |
| Cities / municipalities as end users | we compete in the Business track | focus on banks, merchants, Visa |
| "Faster than BLIK" | not measured | "no typing, 2-3 steps" |
| Any table with fewer than 30 cards or fewer than 3 merchants | breaks the challenge rules (e.g. a postal-prefix row with 2 cards in `geo_results.json`) | filter before showing |

Also confirm with the Visa mentor that storing the data in the BigQuery project used by the team is acceptable.

---

## Likely jury questions

- **"How do you know typing is the problem and not something else?"** 45% of online card payments are typed; a typed
  first payment is followed by less online usage (+4 to +14 pp retention for one-click). It is a strong correlation,
  and the pilot with a control group turns it into proof.
- **"Is this really AI?"** Yes: a gradient-boosting model trained on Visa data, validated on three later periods it
  never saw (AUC 0.74-0.76), calibrated and explained with SHAP. The ROI part is a simulation and we label it as such.
- **"Does the model tell you whom a campaign will convince?"** No, it tells who is about to start paying online. For QR
  that is exactly the moment to intercept; the extra effect of QR is measured with control groups.
- **"Why not only new cards? It is cheaper."** New cards are the cheapest per card and build the habit, so they are
  part of the plan. But typers already make ~7x more typed payments in year one, in-app QR needs no re-issue and the
  pilot effect is visible within weeks.
- **"The data are synthetic, so what is the value?"** A working, validated pipeline: on real Visa data the same code
  produces real audiences, scores and pilot regions.
- **"Privacy?"** Everything shown is aggregated to groups of at least 30 cards (regions: 3,000), merchants only at
  category level; the model scores cards internally and outputs segments.
