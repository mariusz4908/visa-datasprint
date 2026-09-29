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
    who_first_ml_targeting,
    predictive_models_simulations,
    recommendations,
)

PAGES = {
    "🏠 Executive Summary": executive_summary.render,
    "📊 Transaction Overview": transaction_overview.render,
    "🛒 E-Commerce Deep Dive": e_commerce_deep_dive.render,
    "⚔️ BLIK vs Visa": blik_vs_visa.render,
    "🔴 Card-Free Zones": card_free_zones.render,
    "🔄 Subscription Economy": subscription_economy.render,
    "💵 Cash Deserts & Infrastructure": cash_deserts_infrastructure.render,
    "💡 Visa QR Pay — Our Solution": visa_qr_pay.render,
    "🤖 Who First — ML Targeting": who_first_ml_targeting.render,
    "📈 Predictive Models & Simulations": predictive_models_simulations.render,
    "🎯 Recommendations": recommendations.render,
}

# ── SIDEBAR ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<img src="https://cdn.visa.com/v2/assets/images/logos/visa/blue/logo.png" width="120" style="margin-bottom:4px">', unsafe_allow_html=True)
    st.markdown("# CardFlow")
    st.caption("Visa DataSprint Hackathon 2026")
    st.divider()
    page = st.radio("Navigate", list(PAGES), label_visibility="collapsed")
    st.divider()
    st.markdown("**Data sources:**")
    st.caption("• Visa synthetic tx (305.5M)")
    st.caption("• GUS Household Budget 2024")
    st.caption("• NBP Payment Statistics 2024")
    st.caption("• Gemius E-commerce Report 2024")
    st.caption("• ML readiness model (ml_readiness/)")

# ── PAGE (one module per page in app_pages/) ────────────────────────────
PAGES[page]()

# Footer
st.divider()
st.caption("CardFlow — Visa DataSprint Hackathon 2026 | Data: Visa synthetic transactions (305.5M), GUS (2024), NBP (2024), Gemius (2024)")
