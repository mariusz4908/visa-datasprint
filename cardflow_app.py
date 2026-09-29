import streamlit as st

# ── CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CardFlow – Visa DataSprint 2026",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Page modules are imported after set_page_config: loading their data calls Streamlit
from app_pages import (  # noqa: E402
    executive_summary,
    transaction_overview,
    e_commerce_deep_dive,
    blik_vs_visa,
    card_free_zones,
    subscription_economy,
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
    "summary": ("🏠 Executive Summary", "🏠 Podsumowanie", executive_summary.render),
    "overview": ("📊 Transaction Overview", "📊 Przeglad Transakcji", transaction_overview.render),
    "ecom": ("🛒 E-Commerce Deep Dive", "🛒 Analiza E-Commerce", e_commerce_deep_dive.render),
    "blik": ("⚔️ BLIK vs Visa", "⚔️ BLIK vs Visa", blik_vs_visa.render),
    "cardfree": ("🔴 Card-Free Zones", "🔴 Strefy bez Kart", card_free_zones.render),
    "subs": ("🔄 Subscription Economy", "🔄 Ekonomia Subskrypcji", subscription_economy.render),
    "cash": ("💵 Cash Deserts & Infrastructure", "💵 Pustynie Gotówkowe", cash_deserts_infrastructure.render),
    "qrpay": ("💡 Visa QR Pay — Our Solution", "💡 Visa QR Pay — Nasze Rozwiązanie", visa_qr_pay.render),
    "innov": ("🚀 Innovation Portfolio", "🚀 Portfolio Innowacji", innovation_portfolio.render),
    "ml": ("🤖 Who First — ML Targeting", "🤖 Kto Pierwszy — Targetowanie ML", who_first_ml_targeting.render),
    "models": ("📈 Predictive Models & Simulations", "📈 Modele Predykcyjne", predictive_models_simulations.render),
    "recs": ("🎯 Recommendations", "🎯 Rekomendacje", recommendations.render),
}

# ── SIDEBAR ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/5e/Visa_Inc._logo.svg", width=120)
    st.markdown("# CardFlow")
    st.caption("Visa DataSprint Hackathon 2026")
    lang = st.radio("🌐 Language / Jezyk", ["EN", "PL"], horizontal=True)
    st.session_state["lang"] = lang
    st.divider()
    page = st.radio(t("Navigate", "Nawigacja"), list(PAGES), format_func=lambda k: t(*PAGES[k][:2]),
                    label_visibility="collapsed")
    st.divider()
    st.markdown(t("**Data sources:**", "**Źródła danych:**"))
    st.caption(t("• Visa synthetic tx (305.5M)", "• Syntetyczne tx Visa (305.5M)"))
    st.caption(t("• GUS Household Budget 2024", "• GUS Budżety Domowe 2024"))
    st.caption(t("• NBP Payment Statistics 2024", "• NBP Statystyki Płatnicze 2024"))
    st.caption(t("• Gemius E-commerce Report 2024", "• Gemius Raport E-commerce 2024"))
    st.caption(t("• ML readiness model (ml_readiness/)", "• Model ML gotowości (ml_readiness/)"))

# ── PAGE (one module per page in app_pages/) ────────────────────────────
PAGES[page][2]()

# Footer
st.divider()
st.caption(t("CardFlow — Visa DataSprint Hackathon 2026 | Data: Visa synthetic transactions (305.5M), GUS (2024), NBP (2024), Gemius (2024)",
              "CardFlow — Visa DataSprint Hackathon 2026 | Dane: Syntetyczne transakcje Visa (305.5M), GUS (2024), NBP (2024), Gemius (2024)"))
