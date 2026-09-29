# CardFlow — Methodology & Model Documentation
# CardFlow — Metodologia i Dokumentacja Modeli

---

## 1. Data Pipeline / Pipeline Danych

### EN
1. **Data ingestion:** 17GB Parquet file (`datasprint_sample_data.parquet`) loaded into Google BigQuery via Python `google-cloud-bigquery` client
2. **Exploratory analysis:** 20+ SQL queries extracting aggregated metrics by category, time, geography, channel, and card segment
3. **External data enrichment:** GUS population/spending data via BDL API + hardcoded NBP/Gemius statistics
4. **Cross-referencing:** COICOP (GUS) → MCC (Visa) category mapping to identify structural payment gaps
5. **Predictive modeling:** Bass diffusion, activity projections, cannibalization, ROI — computed in Python/NumPy
6. **Visualization:** Streamlit + Plotly interactive dashboard

### PL
1. **Załadowanie danych:** Plik Parquet 17GB załadowany do Google BigQuery przez klienta Python `google-cloud-bigquery`
2. **Analiza eksploracyjna:** 20+ zapytan SQL wyciagajacych zagregowane metryki wg kategorii, czasu, geografii, kanalu i segmentu kart
3. **Wzbogacenie danymi zewnetrznymi:** Dane GUS o populacji/wydatkach z API BDL + statystyki NBP/Gemius
4. **Analiza krzyzowa:** Mapowanie kategorii COICOP (GUS) → MCC (Visa) w celu identyfikacji strukturalnych luk platniczych
5. **Modelowanie predykcyjne:** Dyfuzja Bassa, projekcje aktywnosci, kanibalizacja, ROI — obliczone w Python/NumPy
6. **Wizualizacja:** Interaktywny dashboard Streamlit + Plotly

---

## 2. Gap Analysis Methodology / Metodologia Analizy Luk

### EN
**Gap Index** = (Visa value share % / GUS spending share %) × 100

- Gap Index = 100: Card usage proportional to spending share
- Gap Index < 100: Cards underrepresented (gap = opportunity)
- Gap Index > 100: Cards overrepresented (strong adoption)

**COICOP → MCC Mapping:**

| COICOP Category | Mapped MCC Categories | Gap Index |
|---|---|---|
| Food & Groceries | GROCERY STORES, MISC FOOD, BAKERIES, CANDY STORES | 93 |
| Housing & Utilities | UTILITIES/ELEC/GAS/H2O (only 469K tx found) | 2 |
| Transport | SERVICE STATIONS, TAXIS, LOCAL TRANSPORT, PARKING | 84 |
| Restaurants & Hotels | EATING PLACES, FAST FOOD, HOTELS, BARS | 168 |
| Health | DRUG STORES, DOCTORS, HOSPITALS, DENTISTS, OPTICIANS | 46 |
| Clothing | FAMILY CLOTHING, MENS/WOMENS, COSMETIC STORES | 127 |
| Home Furnishings | HOME SUPPLY, FURNITURE, LUMBER, HARDWARE | 59 |
| Recreation & Culture | DIGITAL GOODS, BOOKS, SPORTS, ENTERTAINMENT | 74 |
| Communications | TELECOM SERVICES (only 792K tx of 305M total) | ~1 |
| Education | COLLEGES, SCHOOLS, CHILDCARE | 3 |
| Alcohol & Tobacco | PKG STORES/LIQUOR, CIGAR STORES | 32 |

### PL
**Indeks Luki** = (Udzial wartosci Visa % / Udzial wydatkow GUS %) × 100

- Indeks = 100: Uzycie kart proporcjonalne do udzialu wydatkow
- Indeks < 100: Karty niedoreprezentowane (luka = szansa)
- Indeks > 100: Karty nadreprezentowane (silna adopcja)

---

## 3. Predictive Models / Modele Predykcyjne

### Model 1: Bass Diffusion (Adoption S-Curve)

**EN:** The Bass model simulates technology adoption as a function of two forces:
- **p (innovation):** External influence — marketing, advertising, media coverage
- **q (imitation):** Internal influence — word of mouth, social proof, network effects

Formula: `F(t) = (1 - e^(-(p+q)t)) / (1 + (q/p)·e^(-(p+q)t))`

**PL:** Model Bassa symuluje adopcje technologii jako funkcje dwoch sil:
- **p (innowacja):** Wplyw zewnetrzny — marketing, reklama, media
- **q (imitacja):** Wplyw wewnetrzny — poczta pantoflowa, dowod spoleczny, efekty sieciowe

| Scenario | p | q | Rationale |
|---|---|---|---|
| Conservative | 0.005 | 0.08 | Limited marketing, slow bank adoption |
| Base | 0.012 | 0.15 | Moderate push, 2-3 bank partnerships |
| Optimistic | 0.025 | 0.25 | Aggressive launch, viral adoption, all major banks |

TAM (Total Addressable Market): 8M active Visa cards in Poland

### Model 2: Transaction Volume

Per active user per month:

| Channel | TX/month | Avg amount (PLN) | Source |
|---|---|---|---|
| P2P | 1.5 – 4.0 | 70 – 90 | Based on BLIK P2P patterns |
| E-commerce | 0.8 – 2.5 | 200 – 280 | From Visa data avg online tx |
| Services | 0.2 – 0.5 | 120 – 180 | Estimated from cash service sector |

Active rate (% of adopters who transact monthly): 40% – 70% depending on scenario.

### Model 3: Cannibalization

Estimates what fraction of QR Pay volume comes from:
- **BLIK** (cannibalization — not net new to card ecosystem)
- **Cash/Transfer** (net new — genuinely new card volume)
- **Existing card** (channel shift within card ecosystem)

| Source | P2P | E-Commerce | Services |
|---|---|---|---|
| From BLIK | 50-70% | 30-40% | 0% |
| From Cash/Transfer | 30-50% | 50-60% | 80-90% |
| From existing card | 0% | 5-10% | 10-20% |

### Model 4: Revenue & ROI

Revenue streams:
- P2P: 0.5% Visa Direct fee
- E-commerce: 0.15% network fee
- Services: 0.5% (P2P-like)

Cost structure (3 years):
- Development: 5M PLN
- Bank integration: 3M PLN
- Marketing: 16M PLN (8+5+3 over 3 years)
- QR stickers: 2M PLN
- Operations: 6M PLN (2M/year)
- **Total: 32M PLN**

### Model 5: E-Commerce Market Share

Simulates how QR Pay shifts Visa's e-commerce share:
- Base e-commerce market: 65B PLN/year, growing 8%/year
- Current Visa share: ~8.8% (55% of 16% card share)
- QR Pay adds new card volume, partially cannibalizing BLIK

### Model 6: Sensitivity Analysis

Tornado analysis varying ±50% on 5 key parameters:
1. P2P transactions per user/month
2. E-commerce transactions per user/month
3. Average P2P amount
4. Active user rate
5. Bass q coefficient (virality)

Most sensitive parameter: **Bass q (virality)** — word-of-mouth adoption is the #1 driver of 3-year revenue.

---

## 4. Compliance / Zgodnosc

### EN
- All analyses use aggregated data only (minimum 30 cards per group)
- No individual cardholders, merchants, or transactions are identifiable
- Visa synthetic data used exclusively for hackathon purposes
- GUS/NBP data is publicly available
- The 3/75 rule is observed (minimum 3 players per group, none >75%)

### PL
- Wszystkie analizy uzywaja wylacznie danych zagregowanych (minimum 30 kart na grupe)
- Zaden pojedynczy posiadacz karty, merchant ani transakcja nie jest identyfikowalny
- Syntetyczne dane Visa uzywane wylacznie na potrzeby hackathonu
- Dane GUS/NBP sa publicznie dostepne
- Zasada 3/75 jest przestrzegana (min. 3 podmioty w grupie, zaden >75%)
