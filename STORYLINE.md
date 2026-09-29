# CardFlow: storyline and evidence map

**[VISA]** = measured in the Visa data (notebooks in `ml_readiness/`) · **[EXT]** = GUS / NBP / Gemius ·
**[ASSUMPTION]** = scenario input. Visa data are synthetic (305.5M transactions, Jan 2025 - Jun 2026): they show the method.

## Pitch

> Almost half of online card payments still require typing a 16-digit card number, and that friction decides whether
> a new online customer stays with the card. Visa QR Pay removes the typing; our ML targeting tells banks who gets it first.

## Slides

| # | Message | Key evidence |
|---|---|---|
| 1 | Title | - |
| 2 | **Cards win in stores, lose online** | [EXT] BLIK 67% vs cards 16% of e-commerce · [VISA] 36% of active cards never pay online |
| 3 | **Why: typing the card number** | [VISA] 45% of online card payments are typed, growing (42% -> 45%) · phone-first users type on a phone in 49% of online payments · Polish merchants type more than foreign (travel 97% vs 68%) |
| 4 | **The first online payment decides** | [VISA] one-click first payment: 45% keep paying online vs 31% after typing (+4 pp within the same category) · 70% of new cards' first online payments are typed |
| 5 | **Solution: Visa QR Pay** | concept · [VISA] 86% of typing happens on phones, so QR must work from the banking app, not only from the card |
| 6 | **Who first** | [VISA] A: 190k cards (22%) make 80% of typed payments, heaviest 20% make 63% of that · new cards: ~27k/month · C: 58k model-selected cards, ~14% start online within 3 months |
| 7 | **The ML model** | [VISA] see below |
| 8 | **Rollout and business case** | in-app QR for A now, QR on every new card, C at first online payment; random 10% control group per audience · ROI = simulation [ASSUMPTION] fed with `results/target_audiences.json` |
| 9 | **Recommendations** | banks: in-app QR + onboarding of new cards · merchants: marketplaces, transport tickets, food delivery first · Visa: KPI = share of first online payments without typing (today 30%) |
| 10 | **Prototype vs next steps** | working: pipeline, friction analysis, model, audiences, dashboard · next: real pilot, real data, merchant integration |

## The ML model (slide 7)

- **What:** for cards that never paid online, the chance of a first online card payment in the next 3 months, from in-store behaviour only.
- **How well:** tested on 3 later periods it never saw: AUC 0.74-0.76; top 10% start **3.5x** more often; top 20% hold **55%** of future starters; calibrated (4.9% predicted = 4.9% actual).
- **Drivers:** new card (first 90 days), any phone payment in store, evening activity, fast food, transport, payments abroad; not how much people spend.
- **Role:** the targeting engine, not the heart of the pitch. It is the only part that is ML trained and validated on Visa data.

## Wording to change

- "6 predictive models" -> **"business case simulation"**; the ML model is the predictive part.
- BLIK, P2P: market context [EXT], not findings from Visa data.
- Cities as end users -> drop (Business track). "Faster than BLIK" -> "no typing, 2-3 steps".
- Filter out any table with < 30 cards or < 3 merchants (e.g. a 2-card row in `geo_results.json`).

## Jury questions

- **Is typing really the cause?** Strong correlation in the data; the pilot with control groups proves it.
- **Is this AI?** Yes: gradient boosting on Visa data, out-of-time validated, calibrated, explained with SHAP.
- **Why not only new cards?** They are cheapest per card and build the habit, but typers give ~7x more payments to replace in year one and in-app QR needs no re-issue.
- **Synthetic data?** The pipeline is ready: on real Visa data it produces real audiences and scores.
