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
