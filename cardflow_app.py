import streamlit as st

# ── CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CardFlow – Visa DataSprint 2026",
    page_icon=":material/credit_card:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Page modules are imported after set_page_config: loading their data calls Streamlit
from app_pages import (  # noqa: E402
    executive_summary,
    blik_vs_visa,
    card_free_zones,
    cash_deserts_infrastructure,
    visa_qr_pay,
    innovation_portfolio,
    who_first_ml_targeting,
    predictive_models_simulations,
    recommendations,
)
from app_pages.common import t  # noqa: E402

# page key -> (EN label, PL label, render function)
PAGES = {
    "summary": ("Executive Summary", "Podsumowanie", executive_summary.render),
    "blik": ("The Problem: BLIK vs Visa", "Problem: BLIK vs Visa", blik_vs_visa.render),
    "cardfree": ("Card-Free Zones", "Strefy bez kart", card_free_zones.render),
    "cash": ("Cash Deserts & Infrastructure", "Gdzie rządzi gotówka", cash_deserts_infrastructure.render),
    "qrpay": ("Visa QR Pay — Our Solution", "Visa QR Pay — nasze rozwiązanie", visa_qr_pay.render),
    "innov": ("Innovation Portfolio", "Portfolio innowacji", innovation_portfolio.render),
    "ml": ("Who First — ML Targeting", "Kto pierwszy — targetowanie ML", who_first_ml_targeting.render),
    "models": ("Predictive Models & Simulations", "Modele predykcyjne", predictive_models_simulations.render),
    "recs": ("Recommendations", "Rekomendacje", recommendations.render),
}

# Clean nav labels (no emoji) for sidebar display
_NAV = {
    "summary":  ("Executive Summary",            "Podsumowanie"),
    "blik":     ("The Problem: BLIK vs Visa",     "Problem: BLIK vs Visa"),
    "cardfree": ("Card-Free Zones",               "Strefy bez kart"),
    "cash":     ("Cash Deserts",                  "Gdzie rządzi gotówka"),
    "qrpay":    ("Visa QR Pay",                   "Visa QR Pay"),
    "innov":    ("Innovation Portfolio",          "Portfolio innowacji"),
    "ml":       ("ML Targeting",                  "Targetowanie ML"),
    "models":   ("Predictive Models",             "Modele predykcyjne"),
    "recs":     ("Recommendations",               "Rekomendacje"),
}

_SIDEBAR_CSS = """<style>
/* ── Background ──────────────────────────────────────────── */
section[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(165deg, #0D1137 0%, #1A1F71 65%, #1E2480 100%);
    padding-top: 1.25rem;
}

/* ── Text colours ────────────────────────────────────────── */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] small,
section[data-testid="stSidebar"] .stCaption p {
    color: rgba(255,255,255,0.55) !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] strong {
    color: rgba(255,255,255,0.95) !important;
}

/* ── Source links (default blue is unreadable on navy) ───── */
section[data-testid="stSidebar"] a {
    color: rgba(255,255,255,0.75) !important;
    text-decoration: underline dotted rgba(247,182,0,0.6) !important;
}
section[data-testid="stSidebar"] a:hover {
    color: #F7B600 !important;
}

/* ── Dividers ────────────────────────────────────────────── */
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.1) !important;
    margin: 0.6rem 0 !important;
}

/* ── Language segmented control ─────────────────────────── */
section[data-testid="stSidebar"] [data-testid="stSegmentedControl"] {
    gap: 4px !important;
}
section[data-testid="stSidebar"] [data-testid="stSegmentedControl"] button {
    color: rgba(255,255,255,0.55) !important;
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 20px !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    padding: 3px 18px !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.04em !important;
}
section[data-testid="stSidebar"] [data-testid="stSegmentedControl"] button:hover {
    background: rgba(255,255,255,0.12) !important;
    color: white !important;
}
section[data-testid="stSidebar"] [data-testid="stSegmentedControl"] button[aria-pressed="true"] {
    background: #F7B600 !important;
    color: #0D1137 !important;
    border-color: #F7B600 !important;
}

/* ── Nav radio: hide widget label ────────────────────────── */
section[data-testid="stSidebar"] .stRadio > label {
    display: none !important;
}

/* ── Nav radio: items ────────────────────────────────────── */
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 2px;
}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
    padding: 9px 8px 9px 18px !important;
    border-radius: 6px !important;
    border-left: 3px solid transparent !important;
    margin: 0 4px !important;
    cursor: pointer !important;
    font-size: 0.875rem !important;
    font-weight: 400 !important;
    color: rgba(255,255,255,0.6) !important;
    line-height: 1.35 !important;
    transition: background 0.2s ease,
                border-left-color 0.2s ease,
                transform 0.15s ease,
                color 0.2s ease !important;
}

/* Hide the radio circle dot */
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label > div:first-child {
    display: none !important;
}

/* ── Hover ───────────────────────────────────────────────── */
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.07) !important;
    border-left-color: rgba(247,182,0,0.55) !important;
    color: rgba(255,255,255,0.92) !important;
    transform: translateX(4px) !important;
}

/* ── Active / selected ───────────────────────────────────── */
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:has(input:checked) {
    background: rgba(247,182,0,0.12) !important;
    border-left-color: #F7B600 !important;
    color: #F7B600 !important;
    font-weight: 500 !important;
    transform: translateX(4px) !important;
}

/* ── Hide Streamlit chrome ───────────────────────────────── */
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
</style>"""

# ── SIDEBAR ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(_SIDEBAR_CSS, unsafe_allow_html=True)
    st.markdown(
        '<img src="https://cdn.visa.com/v2/assets/images/logos/visa/blue/logo.png"'
        ' width="110" style="margin-bottom:2px">',
        unsafe_allow_html=True,
    )
    st.markdown("## CardFlow")
    st.caption("Visa DataSprint Hackathon 2026")

    lang = st.segmented_control("lang", ["EN", "PL"], default="EN", label_visibility="collapsed")
    if lang is None:
        lang = "EN"
    st.session_state["lang"] = lang

    st.divider()

    page = st.radio(
        "nav",
        list(PAGES),
        format_func=lambda k: t(*_NAV[k]),
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown(t("**Data sources**", "**Źródła danych**"))
    st.caption("[Visa synthetic tx · 305.5M](https://visadatasprint.com)")
    st.caption("[GUS Household Budget 2024](https://stat.gov.pl/obszary-tematyczne/warunki-zycia/"
               "dochody-wydatki-i-warunki-zycia-ludnosci/budzety-gospodarstw-domowych-w-2024-r-,9,23.html)")
    st.caption("[NBP Payment Statistics 2024](https://nbp.pl/wp-content/uploads/2025/05/Ocena-II-polrocze-2024-r.pdf)")
    st.caption("[Gemius E-commerce 2024](https://gemius.com/documents/66/RAPORT_E-COMMERCE_2024.pdf)")

# ── PAGE (one module per page in app_pages/) ────────────────────────────
PAGES[page][2]()

# Footer
st.divider()
st.caption(t("CardFlow — Visa DataSprint Hackathon 2026 | Data: Visa synthetic transactions (305.5M), GUS (2024), NBP (2024), Gemius (2024)",
              "CardFlow — Visa DataSprint Hackathon 2026 | Dane: syntetyczne transakcje Visa (305,5 mln), GUS (2024), NBP (2024), Gemius (2024)"))
