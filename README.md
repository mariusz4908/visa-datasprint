# CardFlow

**Transaction Data as a Roadmap for Card Adoption in E-Commerce & P2P Payments**
**Dane transakcyjne jako mapa drogowa popularyzacji kart w e-commerce i platno&#347;ciach P2P**

**Visa DataSprint Hackathon 2026**

---

> **[EN]** Sections are bilingual — English first, Polish below.
> **[PL]** Sekcje sa dwujezyczne — angielski najpierw, polski ponizej.

---

## Project Title / Tytul Projektu

**CardFlow** — *"From Cash & Transfer to Card"* / *"Od gotowki i przelewu do karty"*

---

## Problem Statement / Opis Problemu

**[EN]** Payment cards dominate at physical points of sale (58% share in Poland, NBP 2024), but in **e-commerce** and **peer-to-peer payments** (splitting a dinner bill, marketplace purchases, group collections) they are being displaced by other methods. In Poland, **BLIK captures 67% of e-commerce** and **55% of P2P transactions**, while cards hold just 16% online and ~2% in P2P.

The same person taps their Visa card at a grocery store but switches to BLIK when shopping online — because BLIK is faster, doesn't require typing a 16-digit card number, and feels more secure. This "escape point" represents billions of PLN in transaction volume that flows outside the card ecosystem.

**Key question:** *When, where, and why does the card stop being the first choice — and what can be done about it?*

**[PL]** Karty platnicze dominuja w sklepach stacjonarnych (58% udzialu w Polsce, NBP 2024), ale w **e-commerce** i **platnosciach miedzy osobami** (zwrot za wspolny obiad, zakup z portalu ogloszen, zrzutka) wypieraja je inne metody. W Polsce **BLIK ma 67% e-commerce** i **55% transakcji P2P**, podczas gdy karty to zaledwie 16% online i ~2% w P2P.

Ta sama osoba placi karta w sklepie osiedlowym, a online lub znajomemu placi juz inaczej — bo BLIK jest szybszy, nie wymaga wpisywania numeru karty i wydaje sie bezpieczniejszy. Te "punkty ucieczki" to miliardy zlotych przeplywajace poza ekosystemem kart.

**Kluczowe pytanie:** *Kiedy, gdzie i dlaczego karta przestaje byc pierwszym wyborem — i co mozna z tym zrobic?*

---

## Proposed Solution / Proponowane Rozwiazanie

### 1. Analytical Dashboard (CardFlow Streamlit App)

An interactive analytical tool that cross-references **Visa transaction data** (305.5M transactions sample) with **GUS household spending data**, **NBP payment statistics**, and **Gemius e-commerce reports** to identify:

- **Card-free zones** — spending categories where cards are virtually absent (housing 20.6% of budget = 0.3% of card value; healthcare, education, telecom)
- **E-commerce escape points** — where and why customers abandon cards for BLIK
- **Cash deserts** — sectors with lowest terminal coverage (tutoring 5%, home repair 10%, markets 15%)
- **Online vs offline gaps** — categories with near-zero e-commerce presence (grocery 0.12% online, pharmacy 0.18%)
- **Subscription economy** — Visa's strongest moat (Apple, Netflix, Spotify locked on card rails)

### 2. Visa QR Pay — Product Concept

A new payment paradigm where **every Visa card gets a unique QR code**:

- **P2P Mode:** Someone scans your card's QR code, enters an amount and description, and you receive a payment request on your phone. You approve or decline with biometrics. Powered by Visa Direct.
- **E-Commerce Mode:** Instead of typing your card number at checkout, scan your own card's QR with your phone camera or laptop webcam. A push notification appears — approve and you're done. Faster than BLIK, more secure than typing card details.

### 3. Predictive Models

Six models projecting QR Pay adoption, revenue, and market impact:
- Bass Diffusion adoption S-curve (3 scenarios)
- Transaction volume projection (P2P + e-commerce + services)
- BLIK cannibalization analysis
- Revenue & ROI model (break-even at month 16 in base scenario)
- E-commerce market share simulation
- Sensitivity analysis with tornado charts

---

## End Users

| User Group | What They Get |
|---|---|
| **Online merchants** | Insights on where to implement Click to Pay, tokenized payments; data on checkout abandonment patterns |
| **Banks & Visa** | Segment-level analysis of where to activate card payments (P2P, recurring bills, micro-transactions); Visa QR Pay concept with ROI projections |
| **Cities & municipalities** | Maps of cashless payment gaps in local services (markets, parking, transport, public fees); recommendations for Tap-to-Phone programs |

---

## Data Sources

| Source | Description | Usage |
|---|---|---|
| **Visa synthetic transaction data** | 305,525,104 anonymized transactions, Jan 2025 – Jun 2026 | Primary dataset — transaction patterns, categories, channels, geography |
| **GUS Household Budget Survey 2024** | COICOP household expenditure breakdown (12 categories, 1,690 PLN/month per capita) | Cross-reference to identify spending categories invisible to cards |
| **NBP Payment Statistics 2024** | Card transactions (9.2B), terminals (1.25M), BLIK (4.2B tx), cash vs card share | Macro payment landscape context |
| **Gemius E-Commerce Report 2024** | E-commerce payment method shares (BLIK 67%, card 16%) | Online payment competitive analysis |
| **GUS BDL API** | Population by voivodeship and powiat (2024) | Geographic penetration analysis |
| **BLIK S.A. Annual Report** | BLIK transaction volumes and growth rates | Competitive threat quantification |

### Data Processing

All Visa data was loaded into **Google BigQuery** (`restaurantclub-prod.rozne.datasprint_sample_data`) and queried using SQL for aggregated analysis. No individual transactions or cardholders are identifiable — all analysis operates on groups of 30+ cards per the compliance requirements (3/75 rule observed).

---

## Repository Structure

```
visa-datasprint/
|
|-- cardflow_app.py              # Streamlit entry point: config, sidebar, page routing
|-- app_pages/                   # One module per dashboard page (render()), common.py = shared data & colours
|-- ml_readiness/                # ML readiness model, QR Pay audiences (see ml_readiness/README.md)
|-- models.py                    # Predictive models (Bass diffusion, ROI, etc.)
|-- requirements.txt             # Python dependencies
|-- README.md                    # This file
|-- METHODOLOGY.md               # Detailed methodology & model documentation
|
|-- # Data files (pre-computed from BigQuery)
|-- analysis_results.json        # Core transaction analysis (monthly, hourly, categories)
|-- ecommerce_analysis.json      # E-commerce deep dive (online categories, merchants, trends)
|-- category_analysis.json       # All 619 MCC categories with online/offline split
|-- precise_gaps.json            # Micro-payments, recurring patterns, channel gaps
|-- geo_results.json             # Geographic analysis (postal codes, LAU, FUA)
|-- model_results.json           # Predictive model outputs (3 scenarios, 36 months)
|
|-- # External data
|-- gus_data.json                # GUS population data (voivodeships + powiaty)
|-- gus_spending.json            # GUS COICOP household expenditure structure
|-- gus_cross_analysis.json      # Visa × GUS cross-analysis results
|-- payment_methods_data.json    # NBP/Gemius payment method statistics
|
|-- # Data collection scripts
|-- load_to_bq.py                # Script to load parquet into BigQuery
|-- run_analysis.py              # Core BigQuery analysis queries
|-- query_categories.py          # Category & channel analysis queries
|-- query_ecommerce.py           # E-commerce specific queries
|-- query_geo.py                 # Geographic queries
|-- query_precise_gaps.py        # Precise gap identification queries
|-- fetch_gus.py                 # GUS BDL API data fetcher
|-- fetch_gus_spending.py        # GUS household spending data
|-- fetch_payment_data.py        # NBP/Gemius payment statistics
|-- build_gus_report.py          # GUS × Visa cross-analysis builder
|
|-- # Static reports (HTML)
|-- raport_analiza.html          # Transaction overview report
|-- raport_gus_vs_visa.html      # GUS vs Visa gap analysis
|-- raport_ecommerce_gaps.html   # E-commerce & payment gap report
|
|-- CHALLENGE_DATASPRINT.pdf     # Original hackathon challenge brief
```

---

## How to Run

### Prerequisites
- Python 3.10+
- ~500MB disk space for data files

### Installation
```bash
git clone https://github.com/mariusz4908/visa-datasprint.git
cd visa-datasprint
pip install -r requirements.txt
```

### Run the Dashboard
```bash
streamlit run cardflow_app.py
```
The app will open at `http://localhost:8501`

### Live Demo
> [Streamlit Cloud link — to be added after deployment]

---

## Dashboard Pages

| Page | Content |
|---|---|
| **Executive Summary** | KPIs, payment landscape trends, key findings |
| **Transaction Overview** | Monthly/hourly/daily patterns, top categories & merchants, payment channels |
| **E-Commerce Deep Dive** | Online vs physical analysis, top online merchants, e-commerce growth trend, category gaps |
| **BLIK vs Visa** | Head-to-head comparison, market share trends 2022-2024, strengths & weaknesses |
| **Card-Free Zones** | GUS × Visa gap analysis, COICOP → MCC mapping, Gap Index visualization |
| **Subscription Economy** | Recurring vs one-time value, top subscription services, card-on-file analysis |
| **Cash Deserts & Infrastructure** | Terminal coverage gaps, cash by transaction size, ATM analysis, micro-payments |
| **Visa QR Pay — Our Solution** | Product concept, P2P & e-commerce modes, technical architecture, competitive analysis |
| **Predictive Models** | 6 models with interactive scenario selector, adoption curves, ROI, sensitivity analysis |
| **Recommendations** | Actionable strategies for merchants, banks/Visa, and cities |

---

## Key Findings

1. **BLIK dominates Polish e-commerce** (67%, growing +5pp/year) while cards decline (16%, -2pp/year)
2. **~25% of household spending is invisible to cards** (housing, telecom, education — paid by transfer)
3. **Visa's moat = international subscriptions** (Apple, Netflix, Spotify = ~8M tx locked on card rails)
4. **E-grocery is 0.12% online** — in mature markets it's 10-15%; online grocery avg is 3.1× higher than in-store
5. **4.1% of recurring card-merchant relationships generate 42.8% of all transactions**
6. **ATM avg withdrawal = 1,521** (8.3× avg card tx) — indicating deliberate cash-for-purpose behavior

---

## Predictive Model Results (Base Scenario)

| Metric | Year 1 | Year 2 | Year 3 |
|---|---|---|---|
| QR Pay Adopters | 2.3M | 6.1M | 7.7M |
| Monthly Transactions | 3.8M | 13.4M | 18.2M |
| Monthly Volume (PLN) | 549M | 1.9B | 2.6B |
| Cumulative Revenue | 12M PLN | 72M PLN | 149M PLN |
| **Break-even** | — | **Month 16** | — |
| **3-Year ROI** | — | — | **365%** |

---

## Technology Stack

- **Data warehouse:** Google BigQuery
- **Backend/Analysis:** Python, SQL
- **Dashboard:** Streamlit + Plotly
- **Predictive Models:** NumPy (Bass diffusion, Monte Carlo)
- **External data:** GUS BDL API, NBP, Gemius reports

---

## Links / Linki

| Resource | Link |
|---|---|
| **Repository / Repozytorium** | [github.com/mariusz4908/visa-datasprint](https://github.com/mariusz4908/visa-datasprint) |
| **Live Demo** | *Streamlit Cloud — link to be added / do dodania* |
| **Presentation PDF / Prezentacja** | [CardFlow_Presentation.pdf](./CardFlow_Presentation.pdf) (10 slides / slajdow) |
| **Methodology / Metodologia** | [METHODOLOGY.md](./METHODOLOGY.md) |
| **HTML Reports / Raporty HTML** | [Transaction Analysis](./raport_analiza.html) &#124; [GUS vs Visa](./raport_gus_vs_visa.html) &#124; [E-Commerce Gaps](./raport_ecommerce_gaps.html) |

---

## Team / Zespol

Visa DataSprint Hackathon 2026

---

## Compliance / Zgodnosc

All analyses comply with Visa data usage rules:
- No individual card identification — minimum 30 cards per group
- No merchant dominance disclosure — minimum 3 players per comparison group, none exceeding 75%
- Synthetic data used exclusively for hackathon purposes
