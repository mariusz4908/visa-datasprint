# CardFlow

**Transaction data as a roadmap for card adoption in e-commerce and P2P payments**
Visa DataSprint Hackathon 2026

| | |
|---|---|
| **Live demo** | [CardFlow on Streamlit](https://visa-datasprint-bpszhjrxqjrkpcdhsdm2pe.streamlit.app/) |
| **Project documentation (PDF)** | [CardFlow documentation](LINK_TO_PROJECT_PDF) |
| **Presentation** | [CardFlow_Presentation.pdf](./CardFlow_Presentation.pdf) |

## About

In Polish shops people pay by card, but online and between friends they switch to BLIK, transfers or cash. CardFlow
uses Visa transaction data (305M synthetic transactions, Jan 2025 - Jun 2026) together with GUS, NBP and Gemius
statistics to show where and why the card stops being the first choice, and what to do about it:

- **Dashboard** (Streamlit): card-free spending categories, e-commerce gaps, cash-heavy sectors, subscriptions.
- **Visa QR Pay**: a product concept for P2P and online payments without typing the card number.
- **ML targeting**: a LightGBM model that predicts which cards will start paying online, used to pick the first
  audiences for QR Pay (details in [ml_readiness/README.md](./ml_readiness/README.md)).

End users: online merchants, banks and Visa, cities. All results are aggregates of at least 30 cards, and merchant
categories follow the 3/75 rule. The Visa data is synthetic, so the figures illustrate the method.

## How to run

Requires Python 3.10+.

```bash
git clone https://github.com/mariusz4908/visa-datasprint.git
cd visa-datasprint
pip install -r requirements.txt
streamlit run cardflow_app.py
```

The app opens at http://localhost:8501. It reads only the precomputed JSON files in this repository; the raw Visa
data is not needed. To rebuild the ML results from the raw data, see [ml_readiness/README.md](./ml_readiness/README.md).

## Repository structure

```
cardflow_app.py          Streamlit entry point (sidebar, language switch, page routing)
app_pages/               one module per dashboard page; common.py loads the data
ml_readiness/            ML readiness model, personas, QR Pay audiences (notebooks + results/)
models.py                QR Pay adoption and ROI simulations (Bass diffusion, scenarios)
*.json                   precomputed results read by the app
run_analysis.py,
query_*.py               BigQuery queries that produced the Visa JSON files
fetch_*.py,
build_gus_report.py      GUS / NBP / Gemius data and the GUS x Visa cross-analysis
load_to_bq.py            loads the raw parquet into BigQuery
generate_presentation.py builds CardFlow_Presentation.pdf
raport_*.html            static analysis reports
METHODOLOGY.md           methodology and model details
STORYLINE.md             the project narrative
```
