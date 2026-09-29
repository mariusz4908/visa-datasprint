# ML readiness: who and where to target first with Visa QR Pay

Machine-learning part of CardFlow, built directly on the Visa transaction data (local DuckDB, no BigQuery).
It answers three questions for the QR Pay rollout:

1. **Is typing the card number a real problem?** Friction measured in the Visa data.
2. **Who should get QR Pay first?** A LightGBM model that predicts which cards will start paying online by card.
3. **Where to pilot?** Model scores summed per region, with matched control regions to measure the pilot effect.

## Key results (synthetic data: numbers illustrate the method)

**Friction** (`wallet_online.ipynb`, full data, Polish cards)
- 36% of active cards never paid online by card in 18 months.
- 45% of online card payments are a typed card number, and the share is growing (42% -> 45%).
- Cards that pay mostly by phone in store type the card number on a phone in 49% of their online payments.
- After a first online payment with a saved card, 45% keep paying online (3+ of the next 6 months) vs 31% after
  typing the number; within the same first-purchase category the gap is +4 pp.

**Readiness model** (`readiness_model.ipynb`)
- Predicts a first online card payment within 3 months for cards that have never paid online.
- Rolling backtest, each period predicted only from earlier data: AUC 0.736 / 0.742 / 0.757
  (Oct 2025 / Jan 2026 / Apr 2026); the top 10% of cards start 3.2-3.5x more often than average.
- Beats logistic regression (+0.015 AUC) and a one-line wallet rule (+0.12 AUC) in every period; calibrated
  (predicted 4.9% = actual 4.9% on the calibration period).
- Drivers: evening activity, fast food, restaurants, fuel, any phone payment in store, public transport,
  payments abroad, money transfers; a new card (first 90 days) starts ~4x more often than an old one.
- 6 behavioural personas (KMeans on in-store behaviour only); the model finds ready cards even inside
  low-adoption personas (top picks start at 15-16% vs a 3% persona average).

**QR Pay audiences** (last 6 months)
- 190k active cards pay online and mostly type the number (80% of all typed payments): QR replaces this directly.
- Among never-online cards the model's top picks are the second wave: QR should be their first online payment.

**Pilot regions** (`pilot_regions.ipynb`, `results/pilot_regions.json`)

| Track | Pilot | Control |
|---|---|---|
| Replace typing | Warszawa | Gdansk |
| Replace typing | Wroclaw | Poznan |
| First online payment | Katowice | Rzeszow |
| First online payment | Lodz | Lublin |

Only regions large enough to detect a +1 pp effect are eligible; controls are nearest neighbours on behaviour
with parallel pre-trends (correlation 0.98-0.99).

`ai_experiments.ipynb` documents the approaches that were compared (readiness model, clustering, first-purchase
recommender; the recommender did not beat a popularity baseline and was dropped).

## Setup

1. Put `datasprint_sample_data.parquet` in `ml_readiness/data/` (git-ignored), or set the environment variable
   `VISA_DATA_DIR` to the folder that contains it.
2. `pip install -r requirements.txt` (from the repository root).
3. Run the notebooks from this folder in this order. The first two build the cache in `data/cache/`
   (about 15 GB of free disk space and 8 GB RAM are enough; the first run takes 30-40 minutes, later runs minutes):

| Order | Notebook | Builds / shows |
|---|---|---|
| 1 | `explore.ipynb` | first look at the data, aggregated cache |
| 2 | `wallet_online.ipynb` | card-partitioned data (`slim/`), card-month panel, friction analysis |
| 3 | `readiness_model.ipynb` | features per snapshot, tuning, backtest, calibration, SHAP, personas |
| 4 | `pilot_regions.ipynb` | today's scores, region ranking, controls, `results/pilot_regions.json` |
| - | `ai_experiments.ipynb` | comparison of AI approaches (optional) |

`readiness.py` holds the shared feature pipeline; `paths.py` holds the data location.

## Compliance

- Nothing card-level leaves `data/`: notebooks and `results/` contain only aggregates of at least 30 cards
  (regions: at least 3,000), merchants only at category level.
- The model scores single cards internally; campaign outputs are segments, personas and regions.
