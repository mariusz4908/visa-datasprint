"""Shared data, helpers and colours for all dashboard pages."""
import json
import os

import streamlit as st

# Repository root: the JSON result files live there
DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@st.cache_data
def load_json(name):
    with open(os.path.join(DATA_DIR, name), "r", encoding="utf-8") as f:
        return json.load(f)

# Load all data files
analysis = load_json("analysis_results.json")
gus_spending = load_json("gus_spending.json")
payment_data = load_json("payment_methods_data.json")
ecommerce = load_json("ecommerce_analysis.json")
precise = load_json("precise_gaps.json")
category_data = load_json("category_analysis.json")
geo_data = load_json("geo_results.json")
gus_data = load_json("gus_data.json")

# ── COLORS ──────────────────────────────────────────────────────────────
VISA_BLUE = "#1A1F71"
VISA_GOLD = "#F7B600"
BLIK_PINK = "#D40E6A"
ACCENT = ["#4A90D9", "#E85D75", "#2ECC71", "#F39C12", "#9B59B6", "#1ABC9C",
          "#E74C3C", "#3498DB", "#E67E22", "#8E44AD", "#16A085", "#C0392B"]

# ── TRANSLATION HELPER ──────────────────────────────────────────────────
def t(en, pl):
    """Return text in selected language."""
    return en if st.session_state.get("lang", "EN") == "EN" else pl


# ── SOURCE NOTES ────────────────────────────────────────────────────────
# key -> (badge colour, badge, EN description, PL description)
SOURCES = {
    "visa": ("blue", "VISA", "Visa synthetic transactions (305.5M, Jan 2025–Jun 2026)",
             "syntetyczne transakcje Visa (305,5 mln, I 2025–VI 2026)"),
    "visa_ml": ("blue", "VISA", "Visa synthetic transactions, Polish cards, Jan–Jun 2026 (ml_readiness/)",
                "syntetyczne transakcje Visa, polskie karty, I–VI 2026 (ml_readiness/)"),
    "gus_hbs": ("green", "GUS", "GUS Household Budget Survey 2024 (COICOP)",
                "GUS, Budżety gospodarstw domowych 2024 (COICOP)"),
    "nbp": ("orange", "NBP", "NBP payment statistics 2024", "NBP, statystyki płatnicze 2024"),
    "nbp_survey": ("orange", "NBP", "NBP survey 'Payment habits of Poles' 2024",
                   "NBP, badanie „Zwyczaje płatnicze Polaków” 2024"),
    "gemius": ("violet", "GEMIUS", "Gemius/PBI 'E-commerce in Poland' 2022–2024",
               "Gemius/PBI „E-commerce w Polsce” 2022–2024"),
    "blik": ("violet", "BLIK", "BLIK S.A. annual reports", "raporty roczne BLIK S.A."),
    "estimate": ("gray", "EST", "team estimates based on industry reports",
                 "szacunki zespołu na podstawie raportów branżowych"),
    "sim": ("red", "SIM", "CardFlow simulation (models.py): scenario assumptions, not observed data",
            "symulacja CardFlow (models.py): założenia scenariuszowe, nie dane obserwowane"),
}


def source(*keys, note=None):
    """Caption under a chart saying where its numbers come from; note is an optional (EN, PL) pair."""
    parts = [f":{colour}-background[{badge}] {t(en, pl)}"
             for colour, badge, en, pl in (SOURCES[k] for k in keys)]
    text = f"{t('Source', 'Źródło')}: " + " · ".join(parts)
    if note:
        text += f" — {t(*note)}"
    st.caption(text)
