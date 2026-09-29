import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import json
import os

# ── CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CardFlow – Visa DataSprint 2026",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

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

# ── SIDEBAR ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/5e/Visa_Inc._logo.svg", width=120)
    st.markdown("# CardFlow")
    st.caption("Visa DataSprint Hackathon 2026")
    lang = st.radio("🌐 Language / Jezyk", ["EN", "PL"], horizontal=True)
    st.session_state["lang"] = lang
    st.divider()
    page = st.radio(t("Navigate", "Nawigacja"), [
        t("🏠 Executive Summary", "🏠 Podsumowanie"),
        t("📊 Transaction Overview", "📊 Przeglad Transakcji"),
        t("🛒 E-Commerce Deep Dive", "🛒 Analiza E-Commerce"),
        t("⚔️ BLIK vs Visa", "⚔️ BLIK vs Visa"),
        t("🔴 Card-Free Zones", "🔴 Strefy bez Kart"),
        t("🔄 Subscription Economy", "🔄 Ekonomia Subskrypcji"),
        t("💵 Cash Deserts & Infrastructure", "💵 Pustynie Gotówkowe"),
        t("💡 Visa QR Pay — Our Solution", "💡 Visa QR Pay — Nasze Rozwiązanie"),
        t("🚀 Innovation Portfolio", "🚀 Portfolio Innowacji"),
        t("📈 Predictive Models & Simulations", "📈 Modele Predykcyjne"),
        t("🎯 Recommendations", "🎯 Rekomendacje"),
    ], label_visibility="collapsed")
    st.divider()
    st.markdown(t("**Data sources:**", "**Źródła danych:**"))
    st.caption(t("• Visa synthetic tx (305.5M)", "• Syntetyczne tx Visa (305.5M)"))
    st.caption(t("• GUS Household Budget 2024", "• GUS Budżety Domowe 2024"))
    st.caption(t("• NBP Payment Statistics 2024", "• NBP Statystyki Płatnicze 2024"))
    st.caption(t("• Gemius E-commerce Report 2024", "• Gemius Raport E-commerce 2024"))

# Map page names to internal keys for bilingual routing
PAGE_KEYS = {
    "🏠 Executive Summary": "summary", "🏠 Podsumowanie": "summary",
    "📊 Transaction Overview": "overview", "📊 Przeglad Transakcji": "overview",
    "🛒 E-Commerce Deep Dive": "ecom", "🛒 Analiza E-Commerce": "ecom",
    "⚔️ BLIK vs Visa": "blik",
    "🔴 Card-Free Zones": "cardfree", "🔴 Strefy bez Kart": "cardfree",
    "🔄 Subscription Economy": "subs", "🔄 Ekonomia Subskrypcji": "subs",
    "💵 Cash Deserts & Infrastructure": "cash", "💵 Pustynie Gotówkowe": "cash",
    "💡 Visa QR Pay — Our Solution": "qrpay", "💡 Visa QR Pay — Nasze Rozwiązanie": "qrpay",
    "🚀 Innovation Portfolio": "innov", "🚀 Portfolio Innowacji": "innov",
    "📈 Predictive Models & Simulations": "models", "📈 Modele Predykcyjne": "models",
    "🎯 Recommendations": "recs", "🎯 Rekomendacje": "recs",
}
current_page = PAGE_KEYS.get(page, "summary")

# ══════════════════════════════════════════════════════════════════════════
# PAGE: EXECUTIVE SUMMARY
# ══════════════════════════════════════════════════════════════════════════
if current_page == "summary":
    if lang == "EN":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0D1137, #1A1F71, #2A3090); padding: 40px 32px; border-radius: 16px; color: white; margin-bottom: 24px;">
            <h1 style="margin:0; font-size:2.2em;">CardFlow</h1>
            <p style="opacity:0.9; font-size:1.1em; margin-top:4px;">Transaction data as a roadmap for card adoption in e-commerce & P2P payments</p>
            <span style="background:#F7B600; color:#0D1137; padding:4px 16px; border-radius:16px; font-weight:700; font-size:0.85em;">VISA DATASPRINT HACKATHON 2026</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0D1137, #1A1F71, #2A3090); padding: 40px 32px; border-radius: 16px; color: white; margin-bottom: 24px;">
            <h1 style="margin:0; font-size:2.2em;">CardFlow</h1>
            <p style="opacity:0.9; font-size:1.1em; margin-top:4px;">Dane transakcyjne jako mapa drogowa adopcji kart w e-commerce i płatności P2P</p>
            <span style="background:#F7B600; color:#0D1137; padding:4px 16px; border-radius:16px; font-weight:700; font-size:0.85em;">VISA DATASPRINT HACKATHON 2026</span>
        </div>
        """, unsafe_allow_html=True)

    if lang == "EN":
        st.markdown("""
        > **Payment cards dominate in physical stores, but in e-commerce and peer-to-peer transactions they are being displaced
        > by other methods.** In Poland, BLIK, fast transfers, and cash are the main alternatives. Users choose them because
        > they're faster, don't require typing a card number, and feel more secure. The same person pays by card at a local
        > shop but uses a different method online or when paying a friend.
        >
        > **CardFlow** uses anonymized, aggregated transaction data to understand *when, where, and why* the card stops being
        > the first choice. We analyze behavioral patterns by merchant category, time of day, basket value, and location.
        > We identify **"escape points"** — moments where customers switch payment methods.
        """)
    else:
        st.markdown("""
        > **Karty płatnicze dominują w sklepach stacjonarnych, ale w e-commerce i płatności peer-to-peer są wypierane
        > przez inne metody.** W Polsce BLIK, szybkie przelewy i gotówka to główne alternatywy. Użytkownicy wybierają je,
        > bo są szybsze, nie wymagają wpisywania numeru karty i wydają się bezpieczniejsze. Ta sama osoba płaci kartą
        > w sklepie osiedlowym, ale online lub płacąc znajomemu — wybiera inną metodę.
        >
        > **CardFlow** wykorzystuje zanonimizowane, zagregowane dane transakcyjne, by zrozumiec *kiedy, gdzie i dlaczego*
        > karta przestaje być pierwszym wyborem. Analizujemy wzorce zachowan wedlug kategorii merchantow, pory dnia,
        > wartości koszyka i lokalizacji. Identyfikujemy **"punkty ucieczki"** — momenty, w których klienci zmieniają metodę płatności.
        """)

    st.divider()

    # KPIs
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric(t("Transactions", "Transakcje"), "305.5M", help=t("Total in sample dataset", "Próbka danych"))
    c2.metric(t("Unique Cards", "Unikalne Karty"), "1.95M", help=t("Unique card identifiers", "Unikalne identyfikatory kart"))
    c3.metric(t("Total Value", "Łączna Wartość"), "55.7B", help=t("Fictional currency units", "Fikcyjne jednostki walutowe"))
    c4.metric(t("Avg Transaction", "Średnia Transakcja"), "182.30", help=t("Average transaction value", "Średnia wartość transakcji"))
    c5.metric(t("Online Share (TX)", "Udział Online (TX)"), "11.2%", delta="+1.4pp YoY")
    c6.metric(t("Online Share (Value)", "Udział Online (Wartosc)"), "19.6%", help=t("Online = higher avg value", "Online = wyższa średnia wartość"))

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(t("The Polish Payment Landscape", "Polski Krajobraz Platniczy"))
        fig = go.Figure()
        years = ["2019", "2020", "2021", "2022", "2023", "2024"]
        fig.add_trace(go.Scatter(x=years, y=[44,50,53,55,57,58], name=t("Card at POS (%)", "Karta w POS (%)"), line=dict(color=VISA_BLUE, width=3)))
        fig.add_trace(go.Scatter(x=years, y=[54,47,43,40,37,35], name=t("Cash at POS (%)", "Gotówka w POS (%)"), line=dict(color=ACCENT[1], width=3, dash="dash")))
        fig.add_trace(go.Scatter(x=years, y=[5,10,15,22,30,42], name=t("BLIK tx (×100M)", "BLIK tx (×100M)"), line=dict(color=BLIK_PINK, width=3)))
        fig.update_layout(height=350, margin=dict(t=10,b=30), legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("E-Commerce Payment Methods 2024", "Metody Płatności E-Commerce 2024"))
        fig = px.pie(
            names=[t("BLIK (67%)", "BLIK (67%)"), t("Card (16%)", "Karta (16%)"), t("Bank Transfer (10%)", "Przelew (10%)"), t("Cash on Delivery (5%)", "Za pobraniem (5%)"), t("Other (2%)", "Inne (2%)")],
            values=[67, 16, 10, 5, 2],
            color_discrete_sequence=[BLIK_PINK, VISA_BLUE, ACCENT[0], ACCENT[3], "#ccc"],
            hole=0.4,
        )
        fig.update_layout(height=350, margin=dict(t=10,b=30))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader(t("Key Findings at a Glance", "Kluczowe Odkrycia"))
    f1, f2, f3 = st.columns(3)
    with f1:
        st.error(t("**BLIK Threat:** 67% of e-commerce and growing +5pp/year. Cards fell from 20% to 16% in 2 years.",
                    "**Zagrożenie BLIK:** 67% e-commerce i rośnie +5pp/rok. Karty spadly z 20% do 16% w 2 lata."))
    with f2:
        st.warning(t("**Card-Free Zones:** Housing (20.6% of spending), telecom (4.0%), education (1.1%) have <1% card penetration.",
                      "**Strefy bez Kart:** Mieszkanie (20.6% wydatkow), telekom (4.0%), edukacja (1.1%) maja <1% penetracji kart."))
    with f3:
        st.success(t("**Visa's Moat:** Subscriptions (Apple, Netflix, Spotify) + international e-commerce = ~8M tx locked on card rails.",
                      "**Fosa Visa:** Subskrypcje (Apple, Netflix, Spotify) + międzynarodowy e-commerce = ~8M tx na szynach kart."))

    f4, f5, f6 = st.columns(3)
    with f4:
        st.info(t("**E-Grocery Gap:** 26% of card tx are grocery but only 0.12% online. Online avg = 3.1x higher value.",
                   "**Luka E-Grocery:** 26% tx kartowych to spożywcze, ale tylko 0.12% online. Średnia online = 3.1x wyższa wartość."))
    with f5:
        st.error(t("**Cash Services:** Doctors (255K tx), dentists (76K), home repair (31K) — cash dominates services.",
                    "**Uslugi Gotowkowe:** Lekarze (255K tx), dentysci (76K), naprawy domowe (31K) — gotówka dominuje w usługach."))
    with f6:
        st.success(t("**Recurring Power:** 4.1% of card-merchant pairs generate 42.8% of transactions and 36.5% of value.",
                      "**Sila Cyklicznosci:** 4.1% par karta-merchant generuje 42.8% transakcji i 36.5% wartości."))

    st.divider()

    if lang == "EN":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0D1137, #1A1F71); padding: 24px 28px; border-radius: 14px; color: white;">
            <h3 style="color:#F7B600; margin:0 0 8px 0;">💡 Our Proposed Solution: Visa QR Pay</h3>
            <p style="margin:0; font-size:1em; color:#D0D8F0;">
            A QR code on every Visa card that enables <strong style="color:white;">two new payment flows</strong>:
            (1) <strong style="color:white;">P2P payments</strong> — scan someone's card to send them money, competing directly with BLIK P2P;
            (2) <strong style="color:white;">E-commerce checkout</strong> — scan your own card instead of typing the number, faster and safer than any existing method.
            No card number shared, biometric approval, powered by Visa Direct.
            </p>
            <p style="margin:8px 0 0 0; font-size:0.9em; color:#A0AAC0;">👈 Navigate to <strong style="color:#F7B600;">"Visa QR Pay — Our Solution"</strong> in the sidebar for the full concept.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0D1137, #1A1F71); padding: 24px 28px; border-radius: 14px; color: white;">
            <h3 style="color:#F7B600; margin:0 0 8px 0;">💡 Nasze Rozwiązanie: Visa QR Pay</h3>
            <p style="margin:0; font-size:1em; color:#D0D8F0;">
            Kod QR na każdej karcie Visa umożliwia <strong style="color:white;">dwa nowe sposoby płatności</strong>:
            (1) <strong style="color:white;">Płatności P2P</strong> — zeskanuj kartę znajomego, by wysłać mu pieniądze, konkurując bezpośrednio z BLIK P2P;
            (2) <strong style="color:white;">Płatności e-commerce</strong> — zeskanuj własną kartę zamiast wpisywać numer, szybciej i bezpieczniej niż jakakolwiek istniejąca metoda.
            Bez udostępniania numeru karty, zatwierdzenie biometryczne, napędzane przez Visa Direct.
            </p>
            <p style="margin:8px 0 0 0; font-size:0.9em; color:#A0AAC0;">👈 Przejdź do <strong style="color:#F7B600;">"Visa QR Pay — Nasze Rozwiązanie"</strong> w menu bocznym, by poznać pełną koncepcję.</p>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# PAGE: TRANSACTION OVERVIEW
# ══════════════════════════════════════════════════════════════════════════
elif current_page == "overview":
    st.header(t("Transaction Overview", "Przegląd Transakcji"))
    st.caption(t("Sample dataset: 305.5M transactions, January 2025 – June 2026",
                  "Próbka danych: 305.5M transakcji, styczeń 2025 – czerwiec 2026"))

    # Monthly trends
    monthly = analysis["monthly_trends"]
    df_m = pd.DataFrame(monthly)
    df_m["month"] = df_m["prch_mnth_id"].astype(str).apply(lambda x: x[:4]+"-"+x[4:])

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Monthly Transaction Volume & Value", "Miesięczny Wolumen i Wartość Transakcji"))
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=df_m["month"], y=df_m["tx_count"]/1e6, name=t("Transactions (M)", "Transakcje (M)"), marker_color=VISA_BLUE, opacity=0.7), secondary_y=False)
        fig.add_trace(go.Scatter(x=df_m["month"], y=df_m["total_amount"]/1e9, name=t("Value (B)", "Wartość (mld)"), line=dict(color=VISA_GOLD, width=3)), secondary_y=True)
        fig.update_yaxes(title_text=t("Transactions (M)", "Transakcje (M)"), secondary_y=False)
        fig.update_yaxes(title_text=t("Value (B)", "Wartość (mld)"), secondary_y=True)
        fig.update_layout(height=400, margin=dict(t=10,b=30), legend=dict(orientation="h",y=-0.2))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("Average Transaction Value Over Time", "Średnia Wartość Transakcji w Czasie"))
        fig = px.line(df_m, x="month", y="avg_amount", markers=True)
        fig.update_traces(line_color=ACCENT[0], line_width=3)
        fig.update_layout(height=400, margin=dict(t=10,b=30), yaxis_title=t("Avg amount", "Średnia kwota"), yaxis_range=[170,200])
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Hourly & Daily
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Hourly Pattern (GMT → Poland = +1/+2h)", "Rozkład Godzinowy (GMT → Polska = +1/+2h)"))
        hourly = analysis["hourly_pattern"]
        df_h = pd.DataFrame(hourly)
        df_h["hour_label"] = df_h["hour_gmt"].apply(lambda h: f"{(h+1)%24}:00")
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=df_h["hour_label"], y=df_h["tx_count"]/1e6, name=t("TX (M)", "TX (M)"), marker_color=VISA_BLUE, opacity=0.6), secondary_y=False)
        fig.add_trace(go.Scatter(x=df_h["hour_label"], y=df_h["avg_amount"], name=t("Avg amount", "Średnia kwota"), line=dict(color=VISA_GOLD, width=2)), secondary_y=True)
        fig.update_layout(height=350, margin=dict(t=10,b=30), legend=dict(orientation="h",y=-0.2))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("Day of Week Pattern", "Rozkład Dzienny"))
        daily = analysis["day_of_week"]
        df_d = pd.DataFrame(daily)
        colors = [VISA_BLUE]*7
        colors[df_d["tx_count"].idxmax()] = VISA_GOLD
        colors[df_d["tx_count"].idxmin()] = ACCENT[1]
        fig = go.Figure(go.Bar(x=df_d["day_name"], y=df_d["tx_count"]/1e6, marker_color=colors))
        fig.update_layout(height=350, margin=dict(t=10,b=30), yaxis_title=t("TX (millions)", "TX (mln)"))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Top categories & merchants
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Top 15 Merchant Categories", "Top 15 Kategorii Merchantow"))
        cats = analysis["top_categories"][:15]
        df_c = pd.DataFrame(cats)
        fig = px.bar(df_c, y="mrch_catg_nm", x="tx_count", orientation="h", color_discrete_sequence=[VISA_BLUE])
        fig.update_layout(height=500, margin=dict(t=10,b=10,l=10), yaxis=dict(autorange="reversed"), xaxis_title=t("Transactions", "Transakcje"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("Top 15 Merchants", "Top 15 Merchantow"))
        merch = analysis["top_merchants"][:15]
        df_me = pd.DataFrame(merch)
        fig = px.bar(df_me, y="mrch_nm_raw", x="tx_count", orientation="h", color_discrete_sequence=[ACCENT[3]])
        fig.update_layout(height=500, margin=dict(t=10,b=10,l=10), yaxis=dict(autorange="reversed"), xaxis_title=t("Transactions", "Transakcje"))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Payment channels
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader(t("Payment Channels", "Kanały Płatności"))
        ch = analysis["channel"]
        df_ch = pd.DataFrame(ch)
        fig = px.pie(df_ch, names="channel_flg", values="tx_count", color_discrete_sequence=ACCENT, hole=0.35)
        fig.update_layout(height=350, margin=dict(t=10,b=30))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("Physical vs Online", "Fizyczne vs Online"))
        cp = analysis["cp_flag"]
        labels = [t("Physical (88.8%)", "Fizyczne (88.8%)"), t("Online (11.2%)", "Online (11.2%)")]
        fig = px.pie(names=labels, values=[cp[0]["tx_count"], cp[1]["tx_count"]], color_discrete_sequence=[VISA_BLUE, ACCENT[1]], hole=0.35)
        fig.update_layout(height=350, margin=dict(t=10,b=30))
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.subheader(t("Card Types", "Typy Kart"))
        ct = analysis["card_types"][:6]
        df_ct = pd.DataFrame(ct)
        fig = px.pie(df_ct, names="crd_typ_nm", values="tx_count", color_discrete_sequence=ACCENT, hole=0.35)
        fig.update_layout(height=350, margin=dict(t=10,b=30))
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════
# PAGE: E-COMMERCE DEEP DIVE
# ══════════════════════════════════════════════════════════════════════════
elif current_page == "ecom":
    st.header(t("E-Commerce Deep Dive", "Analiza E-Commerce"))

    overall = ecommerce["ecommerce_overall"]
    phys = [r for r in overall if r["cp_flag"] == 1][0]
    onl = [r for r in overall if r["cp_flag"] == 0][0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("Online Transactions", "Transakcje Online"), f"{onl['tx_count']/1e6:.1f}M", f"{onl['tx_count']/sum(r['tx_count'] for r in overall)*100:.1f}% {t('of total', 'z całkowitych')}")
    c2.metric(t("Online Value", "Wartość Online"), f"{onl['total_amount']/1e9:.1f}B", f"{onl['total_amount']/sum(r['total_amount'] for r in overall)*100:.1f}% {t('of total', 'z całkowitych')}")
    c3.metric(t("Online Avg TX", "Średnia TX Online"), f"{onl['avg_amount']:.0f}", f"+{onl['avg_amount']-phys['avg_amount']:.0f} vs {t('physical', 'fizyczne')}")
    c4.metric(t("Online Cards", "Karty Online"), f"{onl['unique_cards']/1e6:.2f}M", f"{onl['unique_cards']/phys['unique_cards']*100:.0f}% {t('of physical cards', 'kart fizycznych')}")

    st.divider()

    # Monthly trend
    st.subheader(t("E-Commerce Growth Trend", "Trend Wzrostu E-Commerce"))
    trend = ecommerce["ecommerce_monthly_trend"]
    df_t = pd.DataFrame(trend)
    df_t["month"] = df_t["prch_mnth_id"].astype(str).apply(lambda x: x[:4]+"-"+x[4:])

    col1, col2 = st.columns(2)
    with col1:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=df_t["month"], y=df_t["online_tx"]/1e6, name=t("Online TX (M)", "Online TX (M)"), marker_color=VISA_BLUE, opacity=0.7), secondary_y=False)
        fig.add_trace(go.Scatter(x=df_t["month"], y=df_t["online_tx_pct"], name=t("Online % of TX", "Online % TX"), line=dict(color=VISA_GOLD, width=3)), secondary_y=True)
        fig.update_yaxes(title_text=t("Online TX (M)", "Online TX (M)"), secondary_y=False)
        fig.update_yaxes(title_text=t("Online share (%)", "Udział online (%)"), secondary_y=True)
        fig.update_layout(height=380, margin=dict(t=10,b=30), legend=dict(orientation="h",y=-0.2), title_text=t("Online transaction volume & share", "Wolumen i udział transakcji online"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_t["month"], y=df_t["online_tx_pct"], name=t("% of TX", "% TX"), line=dict(color=VISA_BLUE, width=2), mode="lines+markers"))
        fig.add_trace(go.Scatter(x=df_t["month"], y=df_t["online_val_pct"], name=t("% of Value", "% wartości"), line=dict(color=ACCENT[1], width=2), mode="lines+markers"))
        fig.update_layout(height=380, margin=dict(t=10,b=30), yaxis_title=t("Online share (%)", "Udział online (%)"), title_text=t("Online share: transactions vs value", "Udział online: transakcje vs wartość"), legend=dict(orientation="h",y=-0.2))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Top online categories
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Top Online Categories (by TX count)", "Top Kategorie Online (wg liczby TX)"))
        top_ecom = ecommerce["ecommerce_top_categories"][:15]
        df_ec = pd.DataFrame(top_ecom)
        fig = px.bar(df_ec, y="mrch_catg_nm", x="tx_count", orientation="h", color_discrete_sequence=[VISA_BLUE])
        fig.update_layout(height=500, margin=dict(t=10,b=10,l=10), yaxis=dict(autorange="reversed"), xaxis_title=t("Transactions", "Transakcje"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("Top Online Merchants", "Top Merchanci Online"))
        top_merch = ecommerce["ecommerce_top_merchants"][:20]
        df_em = pd.DataFrame(top_merch)
        fig = px.bar(df_em, y="mrch_nm_raw", x="tx_count", orientation="h", color_discrete_sequence=[ACCENT[3]],
                     hover_data=["mrch_catg_nm", "avg_amount", "unique_cards"])
        fig.update_layout(height=500, margin=dict(t=10,b=10,l=10), yaxis=dict(autorange="reversed"), xaxis_title=t("Transactions", "Transakcje"))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Online channel breakdown
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Online Payment Channels", "Kanały Płatności Online"))
        ch = ecommerce["ecommerce_by_channel"]
        df_ech = pd.DataFrame(ch)
        fig = px.pie(df_ech, names="channel_flg", values="tx_count", color_discrete_sequence=ACCENT, hole=0.35)
        fig.update_layout(height=350, margin=dict(t=10,b=30))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("Online vs Physical: Avg Transaction Value", "Online vs Fizyczne: Średnia Wartosc Transakcji"))
        if lang == "EN":
            cats_compare = [
                {"cat": "Family Clothing", "physical": 179, "online": 646},
                {"cat": "Grocery", "physical": 131, "online": 402},
                {"cat": "Cosmetics", "physical": 117, "online": 394},
                {"cat": "Pharmacy", "physical": 143, "online": 479},
                {"cat": "Misc Food", "physical": 59, "online": 259},
                {"cat": "Service Stations", "physical": 216, "online": 344},
                {"cat": "Fast Food", "physical": 64, "online": 133},
                {"cat": "Restaurants", "physical": 121, "online": 152},
            ]
        else:
            cats_compare = [
                {"cat": "Odzież rodzinna", "physical": 179, "online": 646},
                {"cat": "Spożywcze", "physical": 131, "online": 402},
                {"cat": "Kosmetyki", "physical": 117, "online": 394},
                {"cat": "Apteka", "physical": 143, "online": 479},
                {"cat": "Różna żywność", "physical": 59, "online": 259},
                {"cat": "Stacje paliw", "physical": 216, "online": 344},
                {"cat": "Fast food", "physical": 64, "online": 133},
                {"cat": "Restauracje", "physical": 121, "online": 152},
            ]
        df_cmp = pd.DataFrame(cats_compare)
        fig = go.Figure()
        fig.add_trace(go.Bar(name=t("Physical", "Fizyczne"), y=df_cmp["cat"], x=df_cmp["physical"], orientation="h", marker_color=VISA_BLUE, opacity=0.7))
        fig.add_trace(go.Bar(name=t("Online", "Online"), y=df_cmp["cat"], x=df_cmp["online"], orientation="h", marker_color=ACCENT[1]))
        fig.update_layout(height=350, margin=dict(t=10,b=30), barmode="group", xaxis_title=t("Avg transaction value", "Średnia wartość transakcji"), legend=dict(orientation="h",y=-0.15))
        st.plotly_chart(fig, use_container_width=True)

    st.info(t("💡 **Key Insight:** Online transactions average **318** (1.9× physical at 165). In clothing the multiplier is **3.6×** (646 online vs 179 in-store). Every physical transaction converted to online generates ~2× the card revenue.",
               "💡 **Kluczowy Wniosek:** Transakcje online średnio **318** (1.9× fizyczne przy 165). W odzieży mnożnik to **3.6×** (646 online vs 179 w sklepie). Każda fizyczna transakcja przekonwertowana na online generuje ~2× przychód kartowy."))

    st.divider()

    # Categories with lowest online penetration
    st.subheader(t("Categories With Lowest Online Penetration (E-Commerce Desert)", "Kategorie z Najniższą Penetracją Online (Pustynia E-Commerce)"))
    online_det = precise["online_detailed"][:15]
    df_od = pd.DataFrame(online_det)
    fig = px.bar(df_od, y="mrch_catg_nm", x="online_tx_pct", orientation="h",
                 color="online_tx_pct", color_continuous_scale=["#E85D75", "#F7B600", "#2ECC71"],
                 hover_data=["total_tx", "online_tx"])
    fig.update_layout(height=500, margin=dict(t=10,b=10), yaxis=dict(autorange="reversed"),
                      xaxis_title=t("% of transactions that are online", "% transakcji online"), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    st.error(t("🛒 **E-Grocery Gap:** Groceries = 26.3% of all card TX but only **0.12%** are online. E-pharmacy = **0.18%**. In mature markets, e-grocery is 10-15% of food retail. At just 5% penetration this would mean millions of new high-value online card transactions.",
                "🛒 **Luka E-Grocery:** Spozywcze = 26.3% wszystkich TX kartowych, ale tylko **0.12%** online. E-apteka = **0.18%**. Na dojrzalych rynkach e-grocery to 10-15% handlu spożywczego. Przy zaledwie 5% penetracji to miliony nowych wysokowartościowych transakcji kartowych online."))


# ══════════════════════════════════════════════════════════════════════════
# PAGE: BLIK vs VISA
# ══════════════════════════════════════════════════════════════════════════
elif current_page == "blik":
    st.header(t("BLIK vs Visa: The Battle for Polish E-Commerce", "BLIK vs Visa: Bitwa o Polski E-Commerce"))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("BLIK e-com share", "Udział BLIK e-com"), "67%", "+5pp vs 2023", delta_color="inverse")
    c2.metric(t("Card e-com share", "Udział kart e-com"), "16%", "-2pp vs 2023", delta_color="inverse")
    c3.metric(t("BLIK tx/year", "BLIK tx/rok"), "4.2B", "+45% YoY", delta_color="inverse")
    c4.metric(t("Card tx/year (total)", "Tx kartowe/rok (lacznie)"), "9.2B", "+8% YoY")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("E-Commerce Payment Trends 2022–2024", "Trendy Płatności E-Commerce 2022–2024"))
        years = ["2022", "2023", "2024"]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=years, y=[55, 62, 67], name="BLIK", marker_color=BLIK_PINK))
        fig.add_trace(go.Bar(x=years, y=[20, 18, 16], name=t("Card (Visa/MC)", "Karta (Visa/MC)"), marker_color=VISA_BLUE))
        fig.add_trace(go.Bar(x=years, y=[15, 12, 10], name=t("Bank Transfer", "Przelew"), marker_color=ACCENT[0], opacity=0.6))
        fig.add_trace(go.Bar(x=years, y=[8, 6, 5], name=t("Cash on Delivery", "Za pobraniem"), marker_color=ACCENT[3], opacity=0.6))
        fig.update_layout(barmode="stack", height=400, yaxis_title=t("% of e-commerce payments", "% płatności e-commerce"),
                          legend=dict(orientation="h", y=-0.15), margin=dict(t=10,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("BLIK Growth vs Card Decline", "Wzrost BLIK vs Spadek Kart"))
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        yrs = ["2019","2020","2021","2022","2023","2024"]
        fig.add_trace(go.Scatter(x=yrs, y=[0.5,0.9,1.5,2.1,2.9,4.2], name=t("BLIK tx (billions)", "BLIK tx (mld)"),
                                 line=dict(color=BLIK_PINK, width=4), fill="tozeroy", fillcolor="rgba(212,14,106,0.1)"), secondary_y=False)
        fig.add_trace(go.Scatter(x=yrs, y=[25,23,22,20,18,16], name=t("Card e-com share (%)", "Udział kart e-com (%)"),
                                 line=dict(color=VISA_BLUE, width=3, dash="dash")), secondary_y=True)
        fig.update_yaxes(title_text=t("BLIK transactions (B)", "Transakcje BLIK (mld)"), secondary_y=False)
        fig.update_yaxes(title_text=t("Card e-com share (%)", "Udział kart e-com (%)"), secondary_y=True)
        fig.update_layout(height=400, margin=dict(t=10,b=40), legend=dict(orientation="h",y=-0.15))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader(t("BLIK vs Visa — Strategic Comparison", "BLIK vs Visa — Porownanie Strategiczne"))

    if lang == "EN":
        comparison = pd.DataFrame([
            {"Dimension": "E-commerce share 2024", "BLIK": "67%", "Visa Card": "~9%", "Advantage": "🟣 BLIK"},
            {"Dimension": "One-click checkout", "BLIK": "BLIK OneClick", "Visa Card": "Card-on-file / tokenized", "Advantage": "⚪ Tie"},
            {"Dimension": "Recurring / subscriptions", "BLIK": "BLIK Recurring (new)", "Visa Card": "Well established (COF)", "Advantage": "🔵 Visa"},
            {"Dimension": "International e-commerce", "BLIK": "Poland only", "Visa Card": "Global acceptance", "Advantage": "🔵 Visa"},
            {"Dimension": "In-app purchases (Apple/Google)", "BLIK": "Limited support", "Visa Card": "Native integration", "Advantage": "🔵 Visa"},
            {"Dimension": "P2P transfers", "BLIK": "55% share", "Visa Card": "~2% share", "Advantage": "🟣 BLIK"},
            {"Dimension": "Physical POS", "BLIK": "5% (BLIK tap, new)", "Visa Card": "58% (contactless)", "Advantage": "🔵 Visa"},
            {"Dimension": "Cross-border travel", "BLIK": "Not available abroad", "Visa Card": "Universal", "Advantage": "🔵 Visa"},
            {"Dimension": "Chargeback / buyer protection", "BLIK": "Limited", "Visa Card": "Full Visa protection", "Advantage": "🔵 Visa"},
            {"Dimension": "User trust in Poland", "BLIK": "Very high (bank app native)", "Visa Card": "High", "Advantage": "🟣 BLIK"},
        ])
    else:
        comparison = pd.DataFrame([
            {"Wymiar": "Udział w e-commerce 2024", "BLIK": "67%", "Karta Visa": "~9%", "Przewaga": "🟣 BLIK"},
            {"Wymiar": "Płatność jednym kliknięciem", "BLIK": "BLIK OneClick", "Karta Visa": "Card-on-file / tokenizacja", "Przewaga": "⚪ Remis"},
            {"Wymiar": "Cykliczne / subskrypcje", "BLIK": "BLIK Recurring (nowość)", "Karta Visa": "Ugruntowane (COF)", "Przewaga": "🔵 Visa"},
            {"Wymiar": "Międzynarodowy e-commerce", "BLIK": "Tylko Polska", "Karta Visa": "Akceptacja globalna", "Przewaga": "🔵 Visa"},
            {"Wymiar": "Zakupy w aplikacjach (Apple/Google)", "BLIK": "Ograniczone wsparcie", "Karta Visa": "Natywna integracja", "Przewaga": "🔵 Visa"},
            {"Wymiar": "Przelewy P2P", "BLIK": "55% udziału", "Karta Visa": "~2% udziału", "Przewaga": "🟣 BLIK"},
            {"Wymiar": "Fizyczny POS", "BLIK": "5% (BLIK tap, nowość)", "Karta Visa": "58% (zbliżeniowo)", "Przewaga": "🔵 Visa"},
            {"Wymiar": "Podróże zagraniczne", "BLIK": "Niedostępne za granicą", "Karta Visa": "Uniwersalne", "Przewaga": "🔵 Visa"},
            {"Wymiar": "Chargeback / ochrona kupującego", "BLIK": "Ograniczone", "Karta Visa": "Pełna ochrona Visa", "Przewaga": "🔵 Visa"},
            {"Wymiar": "Zaufanie użytkowników w Polsce", "BLIK": "Bardzo wysokie (natywne w banku)", "Karta Visa": "Wysokie", "Przewaga": "🟣 BLIK"},
        ])
    st.dataframe(comparison, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader(t("Where Visa Wins Despite BLIK Dominance", "Gdzie Visa Wygrywa Pomimo Dominacji BLIK"))
    col1, col2 = st.columns(2)
    with col1:
        if lang == "EN":
            st.success("""
            **🔵 Visa Strongholds (BLIK can't easily displace):**
            - **International subscriptions:** Apple (240K cards), Netflix (282K), Spotify (36K), Disney+ (42K), ChatGPT (26K)
            - **Cross-border shopping:** AliExpress, Temu, Shein, Amazon — BLIK doesn't work
            - **In-app purchases:** Google Play, App Store — card-on-file by default
            - **Travel:** Hotels, airlines, car rental — global card acceptance
            - **B2B / Corporate:** Business cards for SaaS, advertising, cloud services
            """)
        else:
            st.success("""
            **🔵 Bastiony Visa (BLIK nie może łatwo wyprzeć):**
            - **Międzynarodowe subskrypcje:** Apple (240K kart), Netflix (282K), Spotify (36K), Disney+ (42K), ChatGPT (26K)
            - **Zakupy transgraniczne:** AliExpress, Temu, Shein, Amazon — BLIK nie działa
            - **Zakupy w aplikacjach:** Google Play, App Store — karta domyślnie zapisana
            - **Podróże:** Hotele, linie lotnicze, wynajem aut — globalna akceptacja kart
            - **B2B / Korporacyjne:** Karty firmowe na SaaS, reklamę, usługi chmurowe
            """)
    with col2:
        if lang == "EN":
            st.error("""
            **🟣 BLIK Strongholds (hard for Visa to compete):**
            - **Domestic e-commerce:** Allegro, OLX, local shops — one-click BLIK
            - **P2P payments:** Splitting bills, marketplace transactions
            - **Quick mobile payments:** 6-digit code, no card number needed
            - **Bill payments:** Telecom top-ups, utility payments
            - **Trust factor:** Integrated in banking apps, feels "safer" than card number entry
            """)
        else:
            st.error("""
            **🟣 Bastiony BLIK (trudne dla Visa do konkurowania):**
            - **Krajowy e-commerce:** Allegro, OLX, lokalne sklepy — BLIK jednym kliknięciem
            - **Płatności P2P:** Dzielenie rachunków, transakcje marketplace
            - **Szybkie płatności mobilne:** 6-cyfrowy kod, bez numeru karty
            - **Opłaty rachunków:** Doładowania telekomów, opłaty za media
            - **Czynnik zaufania:** Zintegrowane w aplikacjach bankowych, czuje się "bezpieczniej" niż wpisywanie numeru karty
            """)

    st.warning(t("⚠️ **Projection:** At current trajectory (-2pp/year for cards), card share in Polish e-commerce could fall **below 10% by 2027**. Visa's strategy must focus on defending subscriptions, winning international shopping, and making card payment as frictionless as BLIK (Click to Pay, tokenization).",
                  "⚠️ **Prognoza:** Przy obecnej trajektorii (-2pp/rok dla kart), udział kart w polskim e-commerce może spaść **poniżej 10% do 2027**. Strategia Visa musi skupić się na obronie subskrypcji, wygrywaniu zakupów międzynarodowych i uczynieniu płatności kartą tak bezproblemową jak BLIK (Click to Pay, tokenizacja)."))


# ══════════════════════════════════════════════════════════════════════════
# PAGE: CARD-FREE ZONES
# ══════════════════════════════════════════════════════════════════════════
elif current_page == "cardfree":
    st.header(t("Card-Free Zones: Where Cards Are Not Used", "Strefy bez Kart: Gdzie Karty Nie Są Używane"))
    st.caption(t("Cross-referencing GUS household spending structure with Visa transaction data",
                  "Analiza krzyzowa struktury wydatkow gospodarstw domowych GUS z danymi transakcyjnymi Visa"))

    if lang == "EN":
        gap_data = [
            {"Category": "Housing & Utilities", "GUS %": 20.6, "Visa Value %": 0.3, "Gap Index": 2, "Status": "🔴 Card-Free Zone", "Barrier": "Bank transfers, direct debit"},
            {"Category": "Communications", "GUS %": 4.0, "Visa Value %": 0.01, "Gap Index": 1, "Status": "🔴 Card-Free Zone", "Barrier": "Direct debit, BLIK"},
            {"Category": "Education", "GUS %": 1.1, "Visa Value %": 0.03, "Gap Index": 3, "Status": "🔴 Card-Free Zone", "Barrier": "Bank transfers, cash tutoring"},
            {"Category": "Alcohol & Tobacco", "GUS %": 2.5, "Visa Value %": 0.8, "Gap Index": 32, "Status": "🟠 Very Underused", "Barrier": "Cash-only kiosks"},
            {"Category": "Healthcare", "GUS %": 5.5, "Visa Value %": 2.5, "Gap Index": 46, "Status": "🟠 Underused", "Barrier": "Cash at doctors, dentists"},
            {"Category": "Home Furnishings", "GUS %": 4.4, "Visa Value %": 2.6, "Gap Index": 59, "Status": "🟠 Underused", "Barrier": "Cash for services/repairs"},
            {"Category": "Recreation & Culture", "GUS %": 6.9, "Visa Value %": 5.1, "Gap Index": 74, "Status": "🟡 Slightly Under", "Barrier": "Cash at events, cinemas"},
            {"Category": "Transport", "GUS %": 9.1, "Visa Value %": 7.6, "Gap Index": 84, "Status": "🟢 Well Covered", "Barrier": "Insurance by transfer"},
            {"Category": "Food & Groceries", "GUS %": 27.1, "Visa Value %": 25.3, "Gap Index": 93, "Status": "🟢 Well Covered", "Barrier": "Small shops, markets"},
            {"Category": "Other Goods", "GUS %": 8.7, "Visa Value %": 9.5, "Gap Index": 109, "Status": "🟢 Well Covered", "Barrier": "—"},
            {"Category": "Clothing", "GUS %": 4.4, "Visa Value %": 5.6, "Gap Index": 127, "Status": "🟢 Overrepresented", "Barrier": "—"},
            {"Category": "Restaurants & Hotels", "GUS %": 5.7, "Visa Value %": 9.6, "Gap Index": 168, "Status": "🟢 Overrepresented", "Barrier": "—"},
        ]
    else:
        gap_data = [
            {"Kategoria": "Mieszkanie i Media", "GUS %": 20.6, "Visa Wartość %": 0.3, "Indeks Luki": 2, "Status": "🔴 Strefa bez Kart", "Bariera": "Przelewy bankowe, polecenia zapłaty"},
            {"Kategoria": "Komunikacja", "GUS %": 4.0, "Visa Wartość %": 0.01, "Indeks Luki": 1, "Status": "🔴 Strefa bez Kart", "Bariera": "Polecenia zapłaty, BLIK"},
            {"Kategoria": "Edukacja", "GUS %": 1.1, "Visa Wartość %": 0.03, "Indeks Luki": 3, "Status": "🔴 Strefa bez Kart", "Bariera": "Przelewy bankowe, korepetycje za gotówkę"},
            {"Kategoria": "Alkohol i Tytoń", "GUS %": 2.5, "Visa Wartość %": 0.8, "Indeks Luki": 32, "Status": "🟠 Bardzo Niedoużywane", "Bariera": "Kioski tylko gotówkowe"},
            {"Kategoria": "Opieka Zdrowotna", "GUS %": 5.5, "Visa Wartość %": 2.5, "Indeks Luki": 46, "Status": "🟠 Niedoużywane", "Bariera": "Gotówka u lekarzy, dentystów"},
            {"Kategoria": "Wyposażenie Domu", "GUS %": 4.4, "Visa Wartość %": 2.6, "Indeks Luki": 59, "Status": "🟠 Niedoużywane", "Bariera": "Gotówka za usługi/naprawy"},
            {"Kategoria": "Rekreacja i Kultura", "GUS %": 6.9, "Visa Wartość %": 5.1, "Indeks Luki": 74, "Status": "🟡 Lekko Poniżej", "Bariera": "Gotówka na imprezach, w kinach"},
            {"Kategoria": "Transport", "GUS %": 9.1, "Visa Wartość %": 7.6, "Indeks Luki": 84, "Status": "🟢 Dobrze Pokryte", "Bariera": "Ubezpieczenie przelewem"},
            {"Kategoria": "Żywność i Sklepy Spożywcze", "GUS %": 27.1, "Visa Wartość %": 25.3, "Indeks Luki": 93, "Status": "🟢 Dobrze Pokryte", "Bariera": "Małe sklepy, targowiska"},
            {"Kategoria": "Pozostałe Towary", "GUS %": 8.7, "Visa Wartość %": 9.5, "Indeks Luki": 109, "Status": "🟢 Dobrze Pokryte", "Bariera": "—"},
            {"Kategoria": "Odzież", "GUS %": 4.4, "Visa Wartość %": 5.6, "Indeks Luki": 127, "Status": "🟢 Nadreprezentowane", "Bariera": "—"},
            {"Kategoria": "Restauracje i Hotele", "GUS %": 5.7, "Visa Wartość %": 9.6, "Indeks Luki": 168, "Status": "🟢 Nadreprezentowane", "Bariera": "—"},
        ]
    df_gap = pd.DataFrame(gap_data)
    st.dataframe(df_gap, use_container_width=True, hide_index=True)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Gap Index by Category", "Indeks Luki wg Kategorii"))
        _cat_col = "Category" if lang == "EN" else "Kategoria"
        _gap_col = "Gap Index" if lang == "EN" else "Indeks Luki"
        df_gap_sorted = df_gap.sort_values(_gap_col)
        colors = df_gap_sorted[_gap_col].apply(lambda x: "#E85D75" if x <= 10 else ("#F39C12" if x < 70 else ("#4A90D9" if x <= 100 else "#2ECC71")))
        fig = go.Figure(go.Bar(y=df_gap_sorted[_cat_col], x=df_gap_sorted[_gap_col], orientation="h",
                                marker_color=colors.tolist()))
        fig.add_vline(x=100, line_dash="dash", line_color=VISA_GOLD, annotation_text=t("100 = proportional", "100 = proporcjonalne"))
        fig.update_layout(height=500, margin=dict(t=10,b=10), xaxis_title=t("Gap Index (100 = expected share)", "Indeks Luki (100 = oczekiwany udział)"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("GUS Spending vs Visa Card Value", "Wydatki GUS vs Wartość Kart Visa"))
        _cat_col2 = "Category" if lang == "EN" else "Kategoria"
        _visa_val_col = "Visa Value %" if lang == "EN" else "Visa Wartość %"
        fig = go.Figure()
        fig.add_trace(go.Bar(name=t("GUS Spending %", "Wydatki GUS %"), y=df_gap[_cat_col2], x=df_gap["GUS %"], orientation="h", marker_color=VISA_BLUE, opacity=0.6))
        fig.add_trace(go.Bar(name=t("Visa Value %", "Visa Wartość %"), y=df_gap[_cat_col2], x=df_gap[_visa_val_col], orientation="h", marker_color=ACCENT[1]))
        fig.update_layout(height=500, margin=dict(t=10,b=10), barmode="group", xaxis_title=t("% share", "% udziału"),
                          legend=dict(orientation="h",y=-0.1))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader(t("The 3 Biggest Card-Free Zones Explained", "3 Najwieksze Strefy bez Kart"))

    tab1, tab2, tab3 = st.tabs([t("🏠 Housing & Utilities (20.6%)", "🏠 Mieszkanie i Media (20.6%)"),
                                 t("📱 Communications (4.0%)", "📱 Komunikacja (4.0%)"),
                                 t("🏥 Healthcare (5.5%)", "🏥 Opieka Zdrowotna (5.5%)")])

    with tab1:
        if lang == "EN":
            st.markdown("""
            **20.6% of all household spending is virtually invisible to cards (Gap Index: 2)**

            | Spending Item | Typical Payment | Card Alternative |
            |---|---|---|
            | Rent / mortgage | Bank transfer / standing order | Card-linked rent platforms |
            | Electricity | Direct debit | Card autopay |
            | Gas / heating | Direct debit | Card autopay |
            | Water / sewage | Transfer | Card autopay |
            | Home insurance | Annual transfer | Card-on-file |

            **Why it matters:** ~14.5M households × ~416 PLN/month = **~6B PLN/month** flowing through non-card channels.
            At even 5% card penetration, this = 300M PLN/month in new card volume.
            """)
        else:
            st.markdown("""
            **20.6% wszystkich wydatków gospodarstw domowych jest praktycznie niewidoczne dla kart (Indeks Luki: 2)**

            | Pozycja wydatku | Typowa płatność | Alternatywa kartowa |
            |---|---|---|
            | Czynsz / kredyt hipoteczny | Przelew / zlecenie stałe | Platformy czynszowe z kartą |
            | Prąd | Polecenie zapłaty | Autopłatność kartą |
            | Gaz / ogrzewanie | Polecenie zapłaty | Autopłatność kartą |
            | Woda / kanalizacja | Przelew | Autopłatność kartą |
            | Ubezpieczenie domu | Roczny przelew | Karta zapisana (COF) |

            **Dlaczego to ważne:** ~14.5M gospodarstw × ~416 PLN/mies. = **~6 mld PLN/mies.** przepływające przez kanały pozakartowe.
            Przy zaledwie 5% penetracji kart to 300M PLN/mies. nowego wolumenu kartowego.
            """)

    with tab2:
        if lang == "EN":
            st.markdown("""
            **4.0% of spending, ~0% on cards (Gap Index: ~1)**

            | Item | Payment Method | Card Opportunity |
            |---|---|---|
            | Mobile phone bill | Direct debit / BLIK | Card-on-file subscription |
            | Home internet | Direct debit | Card-on-file subscription |
            | Prepaid top-up | BLIK / transfer | In-app card payment |

            **Structural barrier:** Telcos set up direct debit at contract signing. Card-on-file requires active user choice.
            """)
        else:
            st.markdown("""
            **4.0% wydatków, ~0% na kartach (Indeks Luki: ~1)**

            | Pozycja | Metoda płatności | Szansa kartowa |
            |---|---|---|
            | Rachunek za telefon | Polecenie zapłaty / BLIK | Subskrypcja karta-na-pliku |
            | Internet domowy | Polecenie zapłaty | Subskrypcja karta-na-pliku |
            | Doładowanie prepaid | BLIK / przelew | Płatność kartą w aplikacji |

            **Bariera strukturalna:** Telekomy ustawiają polecenie zapłaty przy podpisaniu umowy. Karta-na-pliku wymaga aktywnego wyboru użytkownika.
            """)

    with tab3:
        if lang == "EN":
            st.markdown("""
            **5.5% of spending, but only 2.5% of card value (Gap Index: 46)**

            | Service | Visa TX Count | Card Issue |
            |---|---|---|
            | Pharmacies | 8.8M | ✅ Well covered |
            | Doctors & physicians | 255K | ❌ Cash dominant |
            | Hospitals | 99K | ❌ Limited terminals |
            | Dentists | 76K | ❌ Cash dominant |
            | Opticians | 157K | 🟡 Moderate |

            **The split:** Product sales (pharmacy) = good card adoption. **Service delivery** (doctor visits, dental) = cash economy.
            Private healthcare in Poland is ~40% of total health spending — and most of it is cash.
            """)
        else:
            st.markdown("""
            **5.5% wydatków, ale tylko 2.5% wartości kartowej (Indeks Luki: 46)**

            | Usługa | Liczba TX Visa | Problem kartowy |
            |---|---|---|
            | Apteki | 8.8M | ✅ Dobrze pokryte |
            | Lekarze | 255K | ❌ Dominacja gotówki |
            | Szpitale | 99K | ❌ Ograniczone terminale |
            | Dentyści | 76K | ❌ Dominacja gotówki |
            | Optycy | 157K | 🟡 Umiarkowane |

            **Podział:** Sprzedaż produktów (apteka) = dobra adopcja kart. **Świadczenie usług** (wizyty lekarskie, stomatologia) = gospodarka gotówkowa.
            Prywatna opieka zdrowotna w Polsce to ~40% wszystkich wydatków na zdrowie — i większość to gotówka.
            """)


# ══════════════════════════════════════════════════════════════════════════
# PAGE: SUBSCRIPTION ECONOMY
# ══════════════════════════════════════════════════════════════════════════
elif current_page == "subs":
    st.header(t("The Subscription Economy: Visa's Competitive Moat", "Ekonomia Subskrypcji: Fosa Konkurencyjna Visa"))

    subs = ecommerce["subscription_merchants"]
    df_s = pd.DataFrame(subs)

    c1, c2, c3 = st.columns(3)
    c1.metric(t("Subscription merchants", "Merchanci subskrypcyjni"), f"{len(df_s)}", t("with >1K cards & 3+ TX/card", "z >1K kart i 3+ TX/karte"))
    c2.metric("Top: Apple.com", "240K cards", "10.3 TX/card avg")
    c3.metric(t("Recurring pairs (12+/period)", "Pary cykliczne (12+/okres)"), "4.1M", "= 42.8% TX")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Top Subscription Services (by unique cardholders)", "Top Usługi Subskrypcyjne (wg unikalnych posiadaczy kart)"))
        fig = go.Figure()
        fig.add_trace(go.Bar(y=df_s["mrch_nm_raw"][:20], x=df_s["unique_cards"][:20]/1e3, orientation="h",
                             name=t("Unique cards (K)", "Unikalne karty (tys.)"), marker_color=VISA_BLUE))
        fig.update_layout(height=600, margin=dict(t=10,b=10,l=10), yaxis=dict(autorange="reversed"),
                          xaxis_title=t("Unique cards (thousands)", "Unikalne karty (tysiące)"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("Transaction Frequency (TX per card)", "Czestotliwosc Transakcji (TX na karte)"))
        fig = go.Figure()
        fig.add_trace(go.Bar(y=df_s["mrch_nm_raw"][:20], x=df_s["tx_per_card"][:20], orientation="h",
                             name=t("TX per card", "TX na kartę"), marker_color=VISA_GOLD))
        fig.update_layout(height=600, margin=dict(t=10,b=10,l=10), yaxis=dict(autorange="reversed"),
                          xaxis_title=t("Transactions per card (18-month period)", "Transakcje na kartę (okres 18 miesięcy)"))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader(t("Recurring vs One-Time: Value Distribution", "Cykliczne vs Jednorazowe: Rozkład Wartosci"))
    recur = precise["recurring_vs_onetime"]
    df_r = pd.DataFrame(recur)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(df_r, names="frequency", values="total_transactions",
                     color_discrete_sequence=ACCENT, hole=0.35, title=t("Share of total transactions", "Udział w łącznych transakcjach"))
        fig.update_layout(height=350, margin=dict(t=40,b=30))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(df_r, names="frequency", values="total_amount",
                     color_discrete_sequence=ACCENT, hole=0.35, title=t("Share of total value", "Udział w łącznej wartości"))
        fig.update_layout(height=350, margin=dict(t=40,b=30))
        st.plotly_chart(fig, use_container_width=True)

    st.success(t("""
    **Key Insight:** Just **4.1% of card-merchant relationships** (those with 12+ transactions in 18 months) generate:
    - **42.8%** of all transactions (130.9M)
    - **36.5%** of all value (20.3B)

    These are the grocery regulars, subscription services, and habitual merchants.
    **Protecting and growing these recurring relationships is Visa's #1 strategic priority.**
    """, """
    **Kluczowy Wniosek:** Zaledwie **4.1% relacji karta-merchant** (z 12+ transakcjami w 18 miesiecy) generuje:
    - **42.8%** wszystkich transakcji (130.9M)
    - **36.5%** calej wartości (20.3B)

    To stali klienci spożywczy, usługi subskrypcyjne i ulubieni merchanci.
    **Ochrona i rozwijanie tych cyklicznych relacji to priorytet strategiczny nr 1 Visa.**
    """))

    st.divider()
    st.subheader(t("Subscription Categories Breakdown", "Podzial Kategorii Subskrypcyjnych"))

    if lang == "EN":
        sub_cats = {
            "Streaming & Media": ["APPLE.COM/BILL", "NETFLIX.COM", "Netflix.com", "Disney Plus", "SPOTIFY",
                                  "Sklep Prime Video", "PlayStation Network"],
            "E-Commerce Platforms": ["Allegro", "Temu.com", "aliexpress", "shein.com", "VINTED, UAB", "Vinted"],
            "Ride-Hailing & Delivery": ["UBER   *TRIP", "UBR* PENDING.UBER.COM", "UBER   * EATS PENDING",
                                         "UBER   *EATS", "Wolt"],
            "Transport & Mobility": ["jakdojade.pl", "KOLEO bilety kolejowe", "www.bilet.intercity.pl", "Autopay Mobility"],
            "Finance & Transfers": ["Revolut*VISA MONEY TRANSF", "AllegroPay", "PAYSEND"],
            "Telecom": ["doladowania.play.pl", "T-MOBILE POLSKA"],
            "AI & Tech": ["OPENAI *CHATGPT SUBSCR"],
        }
    else:
        sub_cats = {
            "Streaming i Media": ["APPLE.COM/BILL", "NETFLIX.COM", "Netflix.com", "Disney Plus", "SPOTIFY",
                                  "Sklep Prime Video", "PlayStation Network"],
            "Platformy E-Commerce": ["Allegro", "Temu.com", "aliexpress", "shein.com", "VINTED, UAB", "Vinted"],
            "Przewozy i Dostawy": ["UBER   *TRIP", "UBR* PENDING.UBER.COM", "UBER   * EATS PENDING",
                                     "UBER   *EATS", "Wolt"],
            "Transport i Mobilność": ["jakdojade.pl", "KOLEO bilety kolejowe", "www.bilet.intercity.pl", "Autopay Mobility"],
            "Finanse i Przelewy": ["Revolut*VISA MONEY TRANSF", "AllegroPay", "PAYSEND"],
            "Telekomunikacja": ["doladowania.play.pl", "T-MOBILE POLSKA"],
            "AI i Technologia": ["OPENAI *CHATGPT SUBSCR"],
        }

    for cat_name, merchants in sub_cats.items():
        cat_df = df_s[df_s["mrch_nm_raw"].isin(merchants)]
        if not cat_df.empty:
            total_cards = cat_df["unique_cards"].sum()
            st.markdown(f"**{cat_name}** — {total_cards/1e3:.0f}K unique cards")


# ══════════════════════════════════════════════════════════════════════════
# PAGE: CASH DESERTS
# ══════════════════════════════════════════════════════════════════════════
elif current_page == "cash":
    st.header(t("Cash Deserts & Payment Infrastructure Gaps", "Pustynie Gotówkowe i Luki Infrastruktury Płatniczej"))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("POS Terminals", "Terminale POS"), "1.25M", "+8% YoY")
    c2.metric(t("Terminals/1000 pop", "Terminale/1000 mieszk."), "33.3", t("EU avg ~35", "Średnia UE ~35"))
    c3.metric(t("Cash at POS", "Gotówka w POS"), "35%", "-2pp YoY")
    c4.metric(t("ATM avg withdrawal", "Średnia wypłata ATM"), "1,521", t("8.3× avg card TX", "8.3× średnia TX kartowa"))

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Sectors with Lowest Terminal Coverage", "Sektory z Najniższym Pokryciem Terminali"))
        if lang == "EN":
            sectors = [
                {"Sector": "Tutoring / education services", "Terminal %": 5},
                {"Sector": "Home repair / tradesmen", "Terminal %": 10},
                {"Sector": "Open-air markets / bazaars", "Terminal %": 15},
                {"Sector": "Childcare / nurseries", "Terminal %": 30},
                {"Sector": "Traditional taxis", "Terminal %": 40},
                {"Sector": "Vending machines", "Terminal %": 45},
                {"Sector": "Food trucks / street food", "Terminal %": 50},
                {"Sector": "Private medical clinics", "Terminal %": 55},
                {"Sector": "Beauty / hairdressers", "Terminal %": 60},
                {"Sector": "Public institutions (fees)", "Terminal %": 60},
                {"Sector": "Small kiosks / newsstands", "Terminal %": 65},
                {"Sector": "Street parking", "Terminal %": 70},
            ]
        else:
            sectors = [
                {"Sector": "Korepetycje / usługi edukacyjne", "Terminal %": 5},
                {"Sector": "Naprawy domowe / fachowcy", "Terminal %": 10},
                {"Sector": "Targowiska / bazary", "Terminal %": 15},
                {"Sector": "Opieka nad dziećmi / żłobki", "Terminal %": 30},
                {"Sector": "Tradycyjne taksówki", "Terminal %": 40},
                {"Sector": "Automaty vendingowe", "Terminal %": 45},
                {"Sector": "Food trucki / street food", "Terminal %": 50},
                {"Sector": "Prywatne kliniki", "Terminal %": 55},
                {"Sector": "Salony urody / fryzjerzy", "Terminal %": 60},
                {"Sector": "Instytucje publiczne (opłaty)", "Terminal %": 60},
                {"Sector": "Małe kioski / saloniki prasowe", "Terminal %": 65},
                {"Sector": "Parkowanie uliczne", "Terminal %": 70},
            ]
        df_sec = pd.DataFrame(sectors)
        colors = df_sec["Terminal %"].apply(lambda x: "#E85D75" if x < 30 else ("#F39C12" if x < 50 else "#4A90D9"))
        fig = go.Figure(go.Bar(y=df_sec["Sector"], x=df_sec["Terminal %"], orientation="h",
                                marker_color=colors.tolist()))
        fig.update_layout(height=500, margin=dict(t=10,b=10), xaxis_title=t("% with POS terminal", "% z terminalem POS"), xaxis_range=[0,100])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("Cash Usage by Transaction Size", "Użycie Gotówki wg Wielkości Transakcji"))
        sizes = [t("Under 10 PLN", "Poniżej 10 PLN"), "10-50 PLN", "50-100 PLN", "100-500 PLN", t("Over 500 PLN", "Powyżej 500 PLN")]
        fig = go.Figure()
        fig.add_trace(go.Bar(name=t("Cash", "Gotówka"), x=sizes, y=[65,40,30,25,20], marker_color=ACCENT[1]))
        fig.add_trace(go.Bar(name=t("Card", "Karta"), x=sizes, y=[30,50,55,55,50], marker_color=VISA_BLUE))
        fig.add_trace(go.Bar(name="BLIK", x=sizes, y=[5,10,15,20,15], marker_color=BLIK_PINK))
        fig.add_trace(go.Bar(name=t("Transfer", "Przelew"), x=sizes, y=[0,0,0,0,15], marker_color=ACCENT[4], opacity=0.5))
        fig.update_layout(barmode="stack", height=500, yaxis_title=t("% of payments", "% płatności"), yaxis_range=[0,100],
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=10,b=40))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader(t("Transaction Size Distribution in Visa Data", "Rozkład Wielkości Transakcji w Danych Visa"))
    small = precise["small_transactions"]
    df_sm = pd.DataFrame(small)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=df_sm["bucket"], y=df_sm["tx_count"]/1e6, name=t("Transactions (M)", "Transakcje (M)"), marker_color=VISA_BLUE, opacity=0.7), secondary_y=False)
    fig.add_trace(go.Scatter(x=df_sm["bucket"], y=df_sm["total_amount"]/1e9, name=t("Value (B)", "Wartość (mld)"), line=dict(color=VISA_GOLD, width=3)), secondary_y=True)
    fig.update_yaxes(title_text=t("Transactions (M)", "Transakcje (M)"), secondary_y=False)
    fig.update_yaxes(title_text=t("Value (B)", "Wartość (mld)"), secondary_y=True)
    fig.update_layout(height=400, margin=dict(t=10,b=30), legend=dict(orientation="h",y=-0.15))
    st.plotly_chart(fig, use_container_width=True)

    st.info(t("""
    💡 **Micro-payments:** 19.3M transactions are under 5 units (avg 2.86). These exist because contactless payments
    removed the friction of small amounts. But per NBP data, 65% of sub-10 PLN transactions in Poland are still cash.
    **Opportunity:** "Tap for everything" campaigns + zero-fee micro-transactions for merchants.
    """, """
    💡 **Mikropłatności:** 19.3M transakcji jest poniżej 5 jednostek (średnia 2.86). Istnieją, bo płatności zbliżeniowe
    usunęły tarcie małych kwot. Ale wg danych NBP, 65% transakcji poniżej 10 PLN w Polsce to nadal gotówka.
    **Szansa:** Kampanie "Przykładaj za wszystko" + zerowe opłaty za mikropłatności dla merchantów.
    """))

    st.divider()
    st.subheader(t("The ATM Cash Flow", "Przepływ Gotówki ATM"))
    if lang == "EN":
        st.markdown("""
        | Metric | Value |
        |---|---|
        | ATM transactions in Visa sample | 5.4M |
        | Average ATM withdrawal | **1,521** (8.3× avg card TX of 182) |
        | Total ATM value | 8.2B (14.7% of all value in dataset) |
        | Estimated destination of cash | Rent, private doctors, markets, services, informal economy |

        **The high average withdrawal (1,521) suggests deliberate, purpose-driven cash usage** — people withdraw large
        amounts specifically to pay for things that don't accept cards (or where they prefer cash).
        """)
    else:
        st.markdown("""
        | Metryka | Wartość |
        |---|---|
        | Transakcje ATM w próbce Visa | 5.4M |
        | Średnia wypłata ATM | **1 521** (8.3× średnia TX kartowa 182) |
        | Łączna wartość ATM | 8.2 mld (14.7% całej wartości w zbiorze) |
        | Szacowane przeznaczenie gotówki | Czynsz, prywatni lekarze, targowiska, usługi, szara strefa |

        **Wysoka średnia wypłata (1 521) sugeruje celowe, ukierunkowane użycie gotówki** — ludzie wypłacają duże
        kwoty specjalnie, by płacić za rzeczy, które nie akceptują kart (lub gdzie preferują gotówkę).
        """)


# ══════════════════════════════════════════════════════════════════════════
# PAGE: VISA QR PAY — OUR SOLUTION
# ══════════════════════════════════════════════════════════════════════════
elif current_page == "qrpay":
    if lang == "EN":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8EDF8, #D0D9F0); padding: 44px 36px; border-radius: 18px; color: #1A1F71; margin-bottom: 28px; border: 2px solid #B0BDE0;">
            <h1 style="margin:0; font-size:2.4em; color:#0D1137;">Visa QR Pay</h1>
            <p style="color:#333; font-size:1.15em; margin-top:8px;">Your card is your identity. One scan — and the payment comes to you.</p>
            <p style="color:#555; font-size:0.95em; margin-top:4px;">A new payment paradigm: instead of entering card details, you scan a QR code on your physical card. The payment request comes to your phone. You approve or decline — that's it.</p>
            <span style="background:#F7B600; color:#0D1137; padding:5px 20px; border-radius:16px; font-weight:700; font-size:0.85em;">OUR PROPOSED SOLUTION</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8EDF8, #D0D9F0); padding: 44px 36px; border-radius: 18px; color: #1A1F71; margin-bottom: 28px; border: 2px solid #B0BDE0;">
            <h1 style="margin:0; font-size:2.4em; color:#0D1137;">Visa QR Pay</h1>
            <p style="color:#333; font-size:1.15em; margin-top:8px;">Twoja karta to Twoja tożsamość. Jedno skanowanie — i płatność przychodzi do Ciebie.</p>
            <p style="color:#555; font-size:0.95em; margin-top:4px;">Nowy paradygmat płatności: zamiast wpisywać dane karty, skanujesz kod QR na fizycznej karcie. Żądanie płatności pojawia sie na Twoim telefonie. Zatwierdzasz lub odrzucasz — to wszystko.</p>
            <span style="background:#F7B600; color:#0D1137; padding:5px 20px; border-radius:16px; font-weight:700; font-size:0.85em;">NASZE ROZWIĄZANIE</span>
        </div>
        """, unsafe_allow_html=True)

    # ── THE PROBLEM ──
    st.header(t("The Problem We're Solving", "Problem Który Rozwiązujemy"))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.error(t("""
        **🛒 Online Checkout Friction**

        Typing a 16-digit card number, expiry date, and CVV is the #1 reason people abandon cards online.
        In Poland, **67% choose BLIK** instead — because it's one code, one tap.

        *Cards lose not on trust, but on convenience.*
        """, """
        **🛒 Tarcie przy Platnosci Online**

        Wpisywanie 16-cyfrowego numeru karty, daty waznosci i CVV to powod nr 1, dla ktorego ludzie rezygnuja z kart online.
        W Polsce **67% wybiera BLIK** — bo to jeden kod, jedno klikniecie.

        *Karty przegrywaja nie na zaufaniu, lecz na wygodzie.*
        """))
    with col2:
        st.error(t("""
        **🤝 P2P Payments: Cards Don't Exist**

        Splitting a dinner bill, paying for a marketplace item, collecting for a group gift —
        cards are invisible here. **BLIK P2P owns 55%**, bank transfers 40%, cards ~2%.

        *There's no card-native way to request money from someone.*
        """, """
        **🤝 Płatności P2P: Karty Nie Istnieja**

        Dzielenie rachunku za kolację, płatność za przedmiot z marketplace, zbiórka na prezent —
        karty sa tu niewidoczne. **BLIK P2P ma 55%**, przelewy 40%, karty ~2%.

        *Nie ma natywnego sposobu, by karta poprosic kogos o pieniadze.*
        """))
    with col3:
        st.error(t("""
        **🔢 The Number Problem**

        Your card number is sensitive data. Every time you type it, there's a risk.
        Every time you share it, you worry. Every new website = another place your card data lives.

        *What if you never had to type your card number again?*
        """, """
        **🔢 Problem Numeru Karty**

        Numer Twojej karty to wrazliwe dane. Za kazdym razem, gdy go wpisujesz, ryzykujesz.
        Za kazdym razem, gdy go udostepniasz, martwisz sie. Kazda nowa strona = kolejne miejsce z danymi Twojej karty.

        *A gdybys nigdy więcej nie musiał wpisywać numeru karty?*
        """))

    st.divider()

    # ── THE SOLUTION ──
    st.header(t("The Solution: Visa QR Pay", "Rozwiązanie: Visa QR Pay"))
    st.markdown(t("""
    > **Every Visa card gets a unique QR code** — printed on the card, available in the banking app, or on a sticker.
    > Scanning this QR code doesn't reveal the card number. It creates a **secure payment request channel**
    > between the payer and the cardholder.
    """, """
    > **Kazda karta Visa otrzymuje unikalny kod QR** — wydrukowany na karcie, dostepny w aplikacji bankowej lub jako naklejka.
    > Skanowanie tego kodu QR nie ujawnia numeru karty. Tworzy **bezpieczny kanał żądania płatności**
    > między płacącym a posiadaczem karty.
    """))

    st.divider()

    # ── TWO MODES ──
    tab1, tab2 = st.tabs([t("💰 Mode 1: P2P — Request Payment", "💰 Tryb 1: P2P — Zadanie Platnosci"),
                           t("🛒 Mode 2: E-Commerce — Scan to Pay", "🛒 Tryb 2: E-Commerce — Skanuj i Plac")])

    with tab1:
        if lang == "EN":
            st.markdown("""
            <div style="background: linear-gradient(135deg, #E8F0FE, #D0E0FF); padding: 28px; border-radius: 16px; margin-bottom: 20px;">
                <h2 style="color: #1A1F71; margin:0;">Mode 1: P2P Payment Request</h2>
                <p style="color: #333; margin-top:8px; font-size:1.05em;">Someone owes you money? They scan your card's QR code and send you a payment — instantly, by card.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #E8F0FE, #D0E0FF); padding: 28px; border-radius: 16px; margin-bottom: 20px;">
                <h2 style="color: #1A1F71; margin:0;">Tryb 1: Zadanie Płatności P2P</h2>
                <p style="color: #333; margin-top:8px; font-size:1.05em;">Ktos jest Ci winien pieniadze? Skanuje kod QR Twojej karty i wysyla Ci platnosc — natychmiast, karta.</p>
            </div>
            """, unsafe_allow_html=True)

        st.subheader(t("How It Works", "Jak To Działa"))

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">📱</div>
                <h4 style="color:#1A1F71;">{t("Step 1: Scan", "Krok 1: Skanuj")}</h4>
                <p style="font-size:0.9em; color:#666;">{t("Your friend scans the QR code on your Visa card using their phone camera", "Twój znajomy skanuje kod QR na Twojej karcie Visa aparatem telefonu")}</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">💲</div>
                <h4 style="color:#1A1F71;">{t("Step 2: Enter Amount", "Krok 2: Wpisz kwotę")}</h4>
                <p style="font-size:0.9em; color:#666;">{t('They type the amount, add a short description (e.g. "dinner split"), and confirm', 'Wpisuje kwotę, dodaje krótki opis (np. "podział kolacji") i potwierdza')}</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">🔔</div>
                <h4 style="color:#1A1F71;">{t("Step 3: You Get a Request", "Krok 3: Otrzymujesz żądanie")}</h4>
                <p style="font-size:0.9em; color:#666;">{t('A push notification appears on your phone: "Adam wants to pay you 45 PLN — dinner split"', 'Na Twoim telefonie pojawia się powiadomienie push: "Adam chce Ci zapłacić 45 PLN — podział kolacji"')}</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">✅</div>
                <h4 style="color:#1A1F71;">{t("Step 4: Approve or Decline", "Krok 4: Zatwierdź lub odrzuć")}</h4>
                <p style="font-size:0.9em; color:#666;">{t("You review the request and tap Approve. The money moves via Visa Direct — instantly to your card.", "Przeglądasz żądanie i klikasz Zatwierdź. Pieniądze przechodzą przez Visa Direct — natychmiast na Twoją kartę.")}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        st.subheader(t("Use Cases", "Przypadki Użycia"))
        uc1, uc2, uc3, uc4 = st.columns(4)
        with uc1:
            st.info(t("**🍕 Split the bill**\n\nScan the card of whoever paid, enter your share. No IBAN, no phone number needed.",
                       "**🍕 Podziel rachunek**\n\nZeskanuj kartę osoby, która płaciła, wpisz swoją część. Bez IBAN, bez numeru telefonu."))
        with uc2:
            st.info(t("**🏪 Marketplace sale**\n\nSelling on OLX? Buyer scans your card QR at meetup. Instant card-to-card payment.",
                       "**🏪 Sprzedaż na marketplace**\n\nSprzedajesz na OLX? Kupujący skanuje Twój QR przy spotkaniu. Natychmiastowa płatność kartą-do-karty."))
        with uc3:
            st.info(t("**🎁 Group collection**\n\nOrganizing a gift? Share your card QR in the group chat. Everyone scans & pays.",
                       "**🎁 Zbiórka grupowa**\n\nOrganizujesz prezent? Udostępnij QR karty na czacie grupowym. Każdy skanuje i płaci."))
        with uc4:
            st.info(t("**🔧 Pay the plumber**\n\nNo terminal needed. The tradesman shows their card, you scan and pay. Done.",
                       "**🔧 Zapłać hydraulikowi**\n\nBez terminala. Fachowiec pokazuje swoją kartę, skanujesz i płacisz. Gotowe."))

        st.success(t("""
        **Why this changes the game:**
        - **No card number shared** — the QR contains a tokenized identifier, not the actual card number
        - **Works offline** — the QR is printed on the physical card, no internet needed to initiate
        - **Pull → Push model** — the *receiver* doesn't pull money; the *sender* pushes a request that must be approved
        - **Powered by Visa Direct** — instant settlement, 24/7, to any Visa card globally
        - **Directly competes with BLIK P2P** — but works across borders and doesn't require the same bank
        """, """
        **Dlaczego to zmienia gre:**
        - **Brak udostepniania numeru karty** — QR zawiera tokenizowany identyfikator, nie rzeczywisty numer karty
        - **Dziala offline** — QR jest wydrukowany na fizycznej karcie, nie potrzeba internetu do rozpoczecia
        - **Model Pull → Push** — *odbiorca* nie ściąga pieniędzy; *nadawca* wysyla zadanie, które musi być zatwierdzone
        - **Napedzane przez Visa Direct** — natychmiastowe rozliczenie, 24/7, na dowolna karte Visa na swiecie
        - **Bezposrednia konkurencja z BLIK P2P** — ale dziala transgranicznie i nie wymaga tego samego banku
        """))

    with tab2:
        if lang == "EN":
            st.markdown("""
            <div style="background: linear-gradient(135deg, #FFF3E0, #FFE0B2); padding: 28px; border-radius: 16px; margin-bottom: 20px;">
                <h2 style="color: #1A1F71; margin:0;">Mode 2: E-Commerce — Scan Your Card to Pay</h2>
                <p style="color: #333; margin-top:8px; font-size:1.05em;">Instead of typing your card number at checkout, scan your own card's QR with your phone or laptop webcam. The payment request appears on your phone — approve it and you're done.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #FFF3E0, #FFE0B2); padding: 28px; border-radius: 16px; margin-bottom: 20px;">
                <h2 style="color: #1A1F71; margin:0;">Tryb 2: E-Commerce — Zeskanuj Karte i Zaplac</h2>
                <p style="color: #333; margin-top:8px; font-size:1.05em;">Zamiast wpisywac numer karty przy kasie, zeskanuj QR swojej karty telefonem lub kamerka laptopa. Żądanie płatności pojawia sie na telefonie — zatwierdz i gotowe.</p>
            </div>
            """, unsafe_allow_html=True)

        st.subheader(t("How It Works", "Jak To Działa"))

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">🛒</div>
                <h4 style="color:#1A1F71;">{t("Step 1: Checkout", "Krok 1: Kasa")}</h4>
                <p style="font-size:0.9em; color:#666;">{t('At any online store, choose "Visa QR Pay" as your payment method', 'W dowolnym sklepie online wybierz "Visa QR Pay" jako metodę płatności')}</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">📷</div>
                <h4 style="color:#1A1F71;">{t("Step 2: Scan Your Card", "Krok 2: Zeskanuj kartę")}</h4>
                <p style="font-size:0.9em; color:#666;">{t("Hold your Visa card's QR code up to your phone camera or laptop webcam", "Przyłóż kod QR karty Visa do aparatu telefonu lub kamerki laptopa")}</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">🔔</div>
                <h4 style="color:#1A1F71;">{t("Step 3: Approve on Phone", "Krok 3: Zatwierdź na telefonie")}</h4>
                <p style="font-size:0.9em; color:#666;">{t('A push notification: "Allegro — 289 PLN — headphones". You verify and approve with biometrics.', 'Powiadomienie push: "Allegro — 289 PLN — słuchawki". Weryfikujesz i zatwierdzasz biometrycznie.')}</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">🎉</div>
                <h4 style="color:#1A1F71;">{t("Step 4: Done", "Krok 4: Gotowe")}</h4>
                <p style="font-size:0.9em; color:#666;">{t("Payment confirmed. No card number typed. No 3DS redirect. Faster than BLIK.", "Płatność potwierdzona. Bez wpisywania numeru karty. Bez przekierowania 3DS. Szybciej niż BLIK.")}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        st.subheader(t("Why This Beats Current Methods", "Dlaczego To Bije Obecne Metody"))

        if lang == "EN":
            comp = pd.DataFrame([
                {"Step": "Select payment method", "Traditional Card": "Choose 'card'", "BLIK": "Choose 'BLIK'", "Visa QR Pay": "Choose 'Visa QR Pay'"},
                {"Step": "Identify yourself", "Traditional Card": "Type 16-digit card number + expiry + CVV", "BLIK": "Open bank app, copy 6-digit code", "Visa QR Pay": "Scan QR on your card (1 second)"},
                {"Step": "Authenticate", "Traditional Card": "3D Secure redirect → bank app → confirm", "BLIK": "Confirm in bank app", "Visa QR Pay": "Approve push notification (biometric)"},
                {"Step": "Total steps", "Traditional Card": "5-7 steps, 30-60 seconds", "BLIK": "3-4 steps, 15-20 seconds", "Visa QR Pay": "2-3 steps, 5-10 seconds"},
                {"Step": "Card number exposed?", "Traditional Card": "Yes — typed into website", "BLIK": "No (different system)", "Visa QR Pay": "No — only tokenized ID transmitted"},
                {"Step": "Works internationally?", "Traditional Card": "Yes", "BLIK": "No (Poland only)", "Visa QR Pay": "Yes (any Visa-accepting merchant)"},
                {"Step": "Works on laptop without phone?", "Traditional Card": "Yes (but must type number)", "BLIK": "No (requires phone app)", "Visa QR Pay": "Yes (laptop webcam scans QR)"},
            ])
        else:
            comp = pd.DataFrame([
                {"Krok": "Wybierz metodę płatności", "Tradycyjna Karta": "Wybierz 'kartę'", "BLIK": "Wybierz 'BLIK'", "Visa QR Pay": "Wybierz 'Visa QR Pay'"},
                {"Krok": "Zidentyfikuj się", "Tradycyjna Karta": "Wpisz 16-cyfrowy numer karty + datę + CVV", "BLIK": "Otwórz aplikację banku, skopiuj 6-cyfrowy kod", "Visa QR Pay": "Zeskanuj QR na karcie (1 sekunda)"},
                {"Krok": "Uwierzytelnienie", "Tradycyjna Karta": "Przekierowanie 3D Secure → aplikacja banku → potwierdź", "BLIK": "Potwierdź w aplikacji banku", "Visa QR Pay": "Zatwierdź powiadomienie push (biometria)"},
                {"Krok": "Łączna liczba kroków", "Tradycyjna Karta": "5-7 kroków, 30-60 sekund", "BLIK": "3-4 kroki, 15-20 sekund", "Visa QR Pay": "2-3 kroki, 5-10 sekund"},
                {"Krok": "Numer karty ujawniony?", "Tradycyjna Karta": "Tak — wpisany na stronie", "BLIK": "Nie (inny system)", "Visa QR Pay": "Nie — przesyłane tylko tokenizowane ID"},
                {"Krok": "Działa międzynarodowo?", "Tradycyjna Karta": "Tak", "BLIK": "Nie (tylko Polska)", "Visa QR Pay": "Tak (każdy merchant akceptujący Visa)"},
                {"Krok": "Działa na laptopie bez telefonu?", "Tradycyjna Karta": "Tak (ale trzeba wpisać numer)", "BLIK": "Nie (wymaga aplikacji na telefon)", "Visa QR Pay": "Tak (kamera laptopa skanuje QR)"},
            ])
        st.dataframe(comp, use_container_width=True, hide_index=True)

        st.success(t("""
        **The key advantage over BLIK:** Visa QR Pay is **faster** (scan vs. type 6-digit code), **more secure**
        (no card data shared, tokenized), **global** (works on any Visa-accepting website worldwide), and uses
        **biometric approval** (Face ID / fingerprint) instead of manually confirming in the bank app.
        """, """
        **Kluczowa przewaga nad BLIK:** Visa QR Pay jest **szybszy** (skan vs. wpisywanie 6-cyfrowego kodu), **bezpieczniejszy**
        (brak udostepniania danych karty, tokenizacja), **globalny** (dziala na kazdej stronie akceptujacej Visa na swiecie) i korzysta z
        **zatwierdzenia biometrycznego** (Face ID / odcisk palca) zamiast ręcznego potwierdzania w aplikacji bankowej.
        """))

    st.divider()

    # ── DATA-BACKED OPPORTUNITY ──
    st.header(t("Data-Backed: Why This Solution Addresses Real Gaps", "Dane Potwierdzaja: Dlaczego To Rozwiazanie Adresuje Realne Luki"))

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Gaps Addressed by Visa QR Pay", "Luki Adresowane przez Visa QR Pay"))
        if lang == "EN":
            gaps = pd.DataFrame([
                {"Gap": "P2P payments (cards = 2%)", "Current Winner": "BLIK (55%)", "QR Pay Impact": "Direct competitor — scan card to send money", "TAM": "~280B PLN/year"},
                {"Gap": "E-commerce checkout friction", "Current Winner": "BLIK (67%)", "QR Pay Impact": "Faster than BLIK: scan vs type code", "TAM": "~65B PLN/year"},
                {"Gap": "Cash services (plumber, tutor)", "Current Winner": "Cash (90%+)", "QR Pay Impact": "No terminal needed — just show your card", "TAM": "~50B PLN/year"},
                {"Gap": "Marketplace payments (OLX)", "Current Winner": "BLIK/Transfer", "QR Pay Impact": "Instant card-to-card at meetup", "TAM": "~15B PLN/year"},
                {"Gap": "Group collections", "Current Winner": "BLIK/Transfer", "QR Pay Impact": "Share QR in chat, everyone scans & pays", "TAM": "~5B PLN/year"},
                {"Gap": "International online shopping", "Current Winner": "Card (but friction)", "QR Pay Impact": "Scan & approve — no number entry on foreign sites", "TAM": "~20B PLN/year"},
            ])
        else:
            gaps = pd.DataFrame([
                {"Luka": "Płatności P2P (karty = 2%)", "Obecny Lider": "BLIK (55%)", "Wpływ QR Pay": "Bezpośredni konkurent — zeskanuj kartę, wyślij pieniądze", "TAM": "~280 mld PLN/rok"},
                {"Luka": "Tarcie przy kasie e-commerce", "Obecny Lider": "BLIK (67%)", "Wpływ QR Pay": "Szybszy niż BLIK: skan vs wpisywanie kodu", "TAM": "~65 mld PLN/rok"},
                {"Luka": "Usługi gotówkowe (hydraulik, korepetytor)", "Obecny Lider": "Gotówka (90%+)", "Wpływ QR Pay": "Bez terminala — pokaż kartę", "TAM": "~50 mld PLN/rok"},
                {"Luka": "Płatności marketplace (OLX)", "Obecny Lider": "BLIK/Przelew", "Wpływ QR Pay": "Natychmiastowa karta-do-karty przy spotkaniu", "TAM": "~15 mld PLN/rok"},
                {"Luka": "Zbiórki grupowe", "Obecny Lider": "BLIK/Przelew", "Wpływ QR Pay": "Udostępnij QR na czacie, każdy skanuje i płaci", "TAM": "~5 mld PLN/rok"},
                {"Luka": "Międzynarodowe zakupy online", "Obecny Lider": "Karta (ale z tarciem)", "Wpływ QR Pay": "Skanuj i zatwierdź — bez numeru na zagranicznych stronach", "TAM": "~20 mld PLN/rok"},
            ])
        st.dataframe(gaps, use_container_width=True, hide_index=True)

    with col2:
        st.subheader(t("Total Addressable Market", "Calkowity Rynek Docelowy"))
        fig = go.Figure(go.Funnel(
            y=[t("P2P Payments", "Płatności P2P"), t("Domestic E-Commerce", "Krajowy E-Commerce"), t("Cash Services", "Usługi Gotówkowe"), t("International E-Com", "Międzynarodowy E-Com"), t("Marketplace P2P", "Marketplace P2P"), t("Group Collections", "Zbiórki Grupowe")],
            x=[280, 65, 50, 20, 15, 5],
            textinfo="value+text",
            text=[t("280B PLN", "280 mld PLN"), t("65B PLN", "65 mld PLN"), t("50B PLN", "50 mld PLN"), t("20B PLN", "20 mld PLN"), t("15B PLN", "15 mld PLN"), t("5B PLN", "5 mld PLN")],
            marker=dict(color=[VISA_BLUE, ACCENT[0], ACCENT[1], ACCENT[3], ACCENT[4], ACCENT[5]]),
        ))
        fig.update_layout(height=400, margin=dict(t=10,b=10), title_text=t("Estimated Annual Volume (PLN)", "Szacowany Roczny Wolumen (PLN)"))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── TECHNICAL ARCHITECTURE ──
    st.header(t("Technical Concept", "Koncepcja Techniczna"))

    col1, col2 = st.columns(2)
    with col1:
        if lang == "EN":
            st.markdown("""
            ### QR Code Structure
            ```
            visa://pay?token=VQR_8f3a...c7d2&ver=1
            ```

            The QR code on the card contains:
            - **Tokenized card identifier** (not the actual card number)
            - **Version flag** for future extensibility
            - **No sensitive data** — the token is meaningless without Visa's backend

            ### Security Model
            | Layer | Protection |
            |---|---|
            | QR Content | Tokenized ID only — no PAN, no CVV |
            | Request creation | Requires payer's authenticated session |
            | Approval | Push notification + biometric (Face ID / fingerprint) |
            | Transaction | Processed via Visa Direct — full Visa security & fraud detection |
            | Disputes | Full Visa chargeback protection applies |
            | Token revocation | Card owner can revoke/regenerate QR token anytime in bank app |
            """)
        else:
            st.markdown("""
            ### Struktura Kodu QR
            ```
            visa://pay?token=VQR_8f3a...c7d2&ver=1
            ```

            Kod QR na karcie zawiera:
            - **Tokenizowany identyfikator karty** (nie rzeczywisty numer karty)
            - **Flagę wersji** dla przyszłej rozszerzalności
            - **Brak wrażliwych danych** — token jest bezużyteczny bez backendu Visa

            ### Model Bezpieczeństwa
            | Warstwa | Ochrona |
            |---|---|
            | Zawartość QR | Tylko tokenizowane ID — bez PAN, bez CVV |
            | Tworzenie żądania | Wymaga uwierzytelnionej sesji płacącego |
            | Zatwierdzenie | Powiadomienie push + biometria (Face ID / odcisk palca) |
            | Transakcja | Przetwarzana przez Visa Direct — pełne bezpieczeństwo i wykrywanie oszustw Visa |
            | Spory | Pełna ochrona chargeback Visa |
            | Unieważnienie tokenu | Właściciel karty może unieważnić/wygenerować nowy token QR w aplikacji banku |
            """)

    with col2:
        if lang == "EN":
            st.markdown("""
            ### Flow Diagram

            **P2P Mode:**
            ```
            [Payer's Phone]          [Visa Cloud]          [Recipient's Phone]
                 |                        |                        |
                 |--- Scan QR code ------>|                        |
                 |--- Enter amount ------>|                        |
                 |                        |--- Push notification ->|
                 |                        |    "Adam: 45 PLN       |
                 |                        |     dinner split"      |
                 |                        |                        |
                 |                        |<--- APPROVE (biometric)|
                 |                        |                        |
                 |<-- Confirmation -------|------- Funds moved --->|
                 |    "Payment sent"      |    via Visa Direct     |
            ```

            **E-Commerce Mode:**
            ```
            [Merchant Website]       [Visa Cloud]          [Your Phone]
                 |                        |                        |
                 |--- Initiate payment -->|                        |
                 |                        |                        |
            [You scan your card QR with phone/webcam]              |
                 |--- Token sent -------->|                        |
                 |                        |--- Push notification ->|
                 |                        |    "Allegro: 289 PLN   |
                 |                        |     headphones"        |
                 |                        |<--- APPROVE (biometric)|
                 |<-- Payment confirmed --|                        |
                 |    "Order placed!"     |                        |
            ```
            """)
        else:
            st.markdown("""
            ### Diagram Przepływu

            **Tryb P2P:**
            ```
            [Telefon Płacącego]      [Visa Cloud]          [Telefon Odbiorcy]
                 |                        |                        |
                 |--- Skanuj kod QR ----->|                        |
                 |--- Wpisz kwotę ------->|                        |
                 |                        |--- Powiadomienie push->|
                 |                        |    "Adam: 45 PLN       |
                 |                        |     podział kolacji"   |
                 |                        |                        |
                 |                        |<--- ZATWIERDŹ (biomet.)|
                 |                        |                        |
                 |<-- Potwierdzenie ------|--- Środki przelane --->|
                 |    "Płatność wysłana"  |    przez Visa Direct   |
            ```

            **Tryb E-Commerce:**
            ```
            [Strona Merchanta]       [Visa Cloud]          [Twój Telefon]
                 |                        |                        |
                 |--- Zainicjuj płatność->|                        |
                 |                        |                        |
            [Skanujesz QR karty telefonem/kamerką]                 |
                 |--- Token wysłany ----->|                        |
                 |                        |--- Powiadomienie push->|
                 |                        |    "Allegro: 289 PLN   |
                 |                        |     słuchawki"         |
                 |                        |<--- ZATWIERDŹ (biomet.)|
                 |<-- Płatność potwierdz.-|                        |
                 |    "Zamówienie złożone!"|                        |
            ```
            """)

    st.divider()

    # ── COMPETITIVE ADVANTAGE ──
    st.header(t("Competitive Advantage vs BLIK", "Przewaga Konkurencyjna vs BLIK"))

    col1, col2 = st.columns(2)
    with col1:
        if lang == "EN":
            st.markdown("""
            <div style="background:linear-gradient(135deg, #E8F0FE, #D4E2F9); padding:24px; border-radius:14px; border:2px solid #A8C4E8; color:#1F2937;">
                <h3 style="color:#1A1F71;">Why Visa QR Pay wins over BLIK:</h3>
                <ul style="font-size:0.95em; color:#1F2937;">
                    <li><strong style="color:#0D1137;">No app needed to initiate</strong> — anyone with a camera can scan a QR code. BLIK requires the bank app open.</li>
                    <li><strong style="color:#0D1137;">Physical card = always available</strong> — dead phone? Low battery? Your card QR still works for P2P.</li>
                    <li><strong style="color:#0D1137;">Global reach</strong> — works on any Visa merchant worldwide. BLIK = Poland only.</li>
                    <li><strong style="color:#0D1137;">One identity across all channels</strong> — same QR for P2P, e-commerce, in-person services.</li>
                    <li><strong style="color:#0D1137;">No 6-digit code to mistype</strong> — scan is instant and error-free.</li>
                    <li><strong style="color:#0D1137;">Biometric approval</strong> — Face ID / fingerprint vs. manually opening the app and confirming.</li>
                    <li><strong style="color:#0D1137;">Works on laptop</strong> — webcam scans the QR for desktop e-commerce. BLIK always needs a phone.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:linear-gradient(135deg, #E8F0FE, #D4E2F9); padding:24px; border-radius:14px; border:2px solid #A8C4E8; color:#1F2937;">
                <h3 style="color:#1A1F71;">Dlaczego Visa QR Pay wygrywa z BLIK:</h3>
                <ul style="font-size:0.95em; color:#1F2937;">
                    <li><strong style="color:#0D1137;">Nie potrzeba aplikacji do rozpoczęcia</strong> — każdy z aparatem może zeskanować kod QR. BLIK wymaga otwartej aplikacji banku.</li>
                    <li><strong style="color:#0D1137;">Fizyczna karta = zawsze dostępna</strong> — rozładowany telefon? Słaba bateria? QR na karcie nadal działa dla P2P.</li>
                    <li><strong style="color:#0D1137;">Globalny zasięg</strong> — działa u każdego merchanta Visa na świecie. BLIK = tylko Polska.</li>
                    <li><strong style="color:#0D1137;">Jedna tożsamość we wszystkich kanałach</strong> — ten sam QR dla P2P, e-commerce, usług osobistych.</li>
                    <li><strong style="color:#0D1137;">Brak 6-cyfrowego kodu do pomylenia</strong> — skan jest natychmiastowy i bezbłędny.</li>
                    <li><strong style="color:#0D1137;">Zatwierdzenie biometryczne</strong> — Face ID / odcisk palca vs. ręczne otwieranie aplikacji i potwierdzanie.</li>
                    <li><strong style="color:#0D1137;">Działa na laptopie</strong> — kamera skanuje QR dla desktopowego e-commerce. BLIK zawsze wymaga telefonu.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        if lang == "EN":
            st.markdown("""
            <div style="background:linear-gradient(135deg, #FFF3E0, #FFE8CC); padding:24px; border-radius:14px; border:2px solid #FFCC80; color:#3E2723;">
                <h3 style="color:#E65100;">What BLIK still does well:</h3>
                <ul style="font-size:0.95em; color:#3E2723;">
                    <li><strong style="color:#4E342E;">Deeply integrated in Polish banks</strong> — 95% of mobile banking users have BLIK.</li>
                    <li><strong style="color:#4E342E;">No physical card needed at all</strong> — pure digital, works with phone only.</li>
                    <li><strong style="color:#4E342E;">ATM withdrawals</strong> — BLIK can withdraw cash without a card.</li>
                    <li><strong style="color:#4E342E;">Brand trust in Poland</strong> — "BLIK" is almost a verb ("I'll BLIK you").</li>
                </ul>
                <br/>
                <h3 style="color:#E65100;">Visa QR Pay response:</h3>
                <ul style="font-size:0.95em; color:#3E2723;">
                    <li>QR also available <strong style="color:#4E342E;">in banking app</strong> (digital card) — not just physical</li>
                    <li>Partner with Polish banks to add <strong style="color:#4E342E;">"Visa QR Pay" button</strong> next to BLIK</li>
                    <li>Leverage existing <strong style="color:#4E342E;">1.95M Visa cards</strong> in Poland — zero new issuance needed</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:linear-gradient(135deg, #FFF3E0, #FFE8CC); padding:24px; border-radius:14px; border:2px solid #FFCC80; color:#3E2723;">
                <h3 style="color:#E65100;">W czym BLIK nadal jest dobry:</h3>
                <ul style="font-size:0.95em; color:#3E2723;">
                    <li><strong style="color:#4E342E;">Głęboko zintegrowany w polskich bankach</strong> — 95% użytkowników bankowości mobilnej ma BLIK.</li>
                    <li><strong style="color:#4E342E;">Nie potrzeba fizycznej karty</strong> — czysto cyfrowy, działa tylko z telefonem.</li>
                    <li><strong style="color:#4E342E;">Wypłaty z bankomatów</strong> — BLIK może wypłacić gotówkę bez karty.</li>
                    <li><strong style="color:#4E342E;">Zaufanie do marki w Polsce</strong> — "BLIK" to prawie czasownik ("Zblikuję Ci").</li>
                </ul>
                <br/>
                <h3 style="color:#E65100;">Odpowiedź Visa QR Pay:</h3>
                <ul style="font-size:0.95em; color:#3E2723;">
                    <li>QR dostępny również <strong style="color:#4E342E;">w aplikacji bankowej</strong> (karta cyfrowa) — nie tylko fizyczna</li>
                    <li>Partnerstwo z polskimi bankami, by dodać <strong style="color:#4E342E;">przycisk "Visa QR Pay"</strong> obok BLIK</li>
                    <li>Wykorzystanie istniejących <strong style="color:#4E342E;">1.95M kart Visa</strong> w Polsce — zero nowych emisji</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ── ROLLOUT PLAN ──
    st.header(t("Proposed Rollout", "Proponowany Plan Wdrozenia"))

    if lang == "EN":
        phases = pd.DataFrame([
            {"Phase": "Phase 1 (0-3 months)", "Action": "Pilot with 2-3 Polish banks — QR in mobile banking app", "Target": "P2P payments between bank customers", "KPI": "10K active QR payers"},
            {"Phase": "Phase 2 (3-6 months)", "Action": "QR stickers sent to all Visa cardholders by mail", "Target": "P2P + marketplace (OLX, Vinted)", "KPI": "100K active QR payers"},
            {"Phase": "Phase 3 (6-12 months)", "Action": "Merchant SDK — 'Visa QR Pay' button at checkout", "Target": "Top 50 Polish e-commerce sites", "KPI": "1M online QR transactions/month"},
            {"Phase": "Phase 4 (12-18 months)", "Action": "QR printed on all new Visa cards in Poland", "Target": "Full market — P2P, e-com, services", "KPI": "5% of e-commerce share (from ~9%)"},
            {"Phase": "Phase 5 (18-24 months)", "Action": "International rollout — EU, then global", "Target": "Cross-border P2P & e-commerce", "KPI": "Pan-European Visa QR standard"},
        ])
    else:
        phases = pd.DataFrame([
            {"Faza": "Faza 1 (0-3 miesiące)", "Działanie": "Pilot z 2-3 polskimi bankami — QR w aplikacji mobilnej", "Cel": "Płatności P2P między klientami banków", "KPI": "10K aktywnych płatników QR"},
            {"Faza": "Faza 2 (3-6 miesięcy)", "Działanie": "Naklejki QR wysłane do wszystkich posiadaczy kart Visa", "Cel": "P2P + marketplace (OLX, Vinted)", "KPI": "100K aktywnych płatników QR"},
            {"Faza": "Faza 3 (6-12 miesięcy)", "Działanie": "SDK dla merchantów — przycisk 'Visa QR Pay' przy kasie", "Cel": "Top 50 polskich sklepów e-commerce", "KPI": "1M transakcji QR online/mies."},
            {"Faza": "Faza 4 (12-18 miesięcy)", "Działanie": "QR drukowany na wszystkich nowych kartach Visa w Polsce", "Cel": "Pełny rynek — P2P, e-com, usługi", "KPI": "5% udziału w e-commerce (z ~9%)"},
            {"Faza": "Faza 5 (18-24 miesiące)", "Działanie": "Międzynarodowe wdrożenie — UE, potem globalnie", "Cel": "Transgraniczne P2P i e-commerce", "KPI": "Paneuropejski standard Visa QR"},
        ])
    st.dataframe(phases, use_container_width=True, hide_index=True)

    st.divider()

    # ── IMPACT ESTIMATION ──
    st.header(t("Projected Impact", "Prognozowany Wplyw"))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(t("P2P market capture target", "Cel przejecia rynku P2P"), "10%", help=t("Of BLIK's 55% P2P share → ~28B PLN/year", "Z 55% udzialu BLIK P2P → ~28B PLN/rok"))
        st.metric(t("New annual card P2P volume", "Nowy roczny wolumen P2P kart"), "~28B PLN")
    with col2:
        st.metric(t("E-commerce share gain", "Wzrost udzialu e-commerce"), "+3-5pp", help=t("From ~9% to 12-14% of e-commerce", "Z ~9% do 12-14% e-commerce"))
        st.metric(t("New annual e-com volume", "Nowy roczny wolumen e-com"), "~3-4B PLN")
    with col3:
        st.metric(t("Cash services converted", "Konwersja usług gotówkowych"), "5-10%", help=t("Of ~50B PLN cash service economy", "Z ~50B PLN gospodarki usług gotówkowych"))
        st.metric(t("New annual service volume", "Nowy roczny wolumen uslug"), "~3-5B PLN")

    if lang == "EN":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8F8F0, #D5F5E3); padding: 20px 24px; border-radius: 14px; border-left: 4px solid #2ECC71; margin-top: 20px; color: #1A3C2A;">
            <h3 style="color:#1B7A3D; margin:0 0 8px 0;">Combined Potential: ~35B PLN in new annual card transaction volume</h3>
            <p style="margin:0; color:#1A3C2A;">By turning every Visa card into a payment acceptance point (via QR), we transform cards from a "spending tool"
            into a <strong style="color:#145A24;">universal payment platform</strong> — competing with BLIK on convenience while leveraging Visa's global infrastructure,
            security, and buyer protection that BLIK cannot match.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8F8F0, #D5F5E3); padding: 20px 24px; border-radius: 14px; border-left: 4px solid #2ECC71; margin-top: 20px; color: #1A3C2A;">
            <h3 style="color:#1B7A3D; margin:0 0 8px 0;">Laczny Potencjal: ~35B PLN nowego rocznego wolumenu transakcji kartowych</h3>
            <p style="margin:0; color:#1A3C2A;">Zamieniajac kazda karte Visa w punkt akceptacji platnosci (przez QR), transformujemy karty z "narzedzia wydatkow"
            w <strong style="color:#145A24;">uniwersalna platforme platnicza</strong> — konkurujac z BLIK na wygodzie, jednoczesnie wykorzystujac globalna infrastrukture Visa,
            bezpieczenstwo i ochronę kupującego, których BLIK nie może zapewnić.</p>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# PAGE: INNOVATION PORTFOLIO
# ══════════════════════════════════════════════════════════════════════════
elif current_page == "innov":
    st.header(t("Visa Marketplace Shield — Escrow for P2P Commerce", "Visa Marketplace Shield — Escrow dla Handlu P2P"))
    st.caption(t("Card-powered escrow for marketplace transactions — backed by data gaps in our analysis",
                  "Escrow napedzany kartami dla transakcji marketplace — poparty lukami w naszej analizie"))
    st.subheader(t("3. Visa Marketplace Shield — Escrow for P2P Commerce", "3. Visa Marketplace Shield — Escrow dla Handlu P2P"))

    col1, col2 = st.columns([2, 1])
    with col1:
        if lang == "EN":
            st.markdown("""
            **The Gap:** Marketplace transactions (OLX, Vinted, Facebook Marketplace) = ~15B PLN/year. Currently paid by
            BLIK P2P or bank transfer — **with zero buyer protection**. Scams are common. Cards are not used because
            there's no card-native mechanism for person-to-person commerce.

            **The Solution:** Card-powered escrow for marketplace transactions:

            **For Buyers:**
            1. At meetup or online, scan seller's Visa QR code
            2. Enter amount + item description + take a photo
            3. Money is **held in Visa escrow** (charged to buyer's card)
            4. Buyer confirms receipt within 48h → money released to seller
            5. Dispute? **Full Visa chargeback protection** kicks in

            **For Sellers:**
            - Guaranteed payment (no bounced transfers, no fake BLIK)
            - Money arrives to Visa card within 24h of buyer confirmation
            - Seller reputation score builds over time

            **Key advantage over BLIK P2P:** BLIK transfer is instant and irreversible — if you get scammed, the money is gone.
            Visa Marketplace Shield holds funds until both parties are satisfied. **Trust = the differentiator.**
            """)
        else:
            st.markdown("""
            **Luka:** Transakcje marketplace (OLX, Vinted, Facebook Marketplace) = ~15 mld PLN/rok. Obecnie płacone przez
            BLIK P2P lub przelew — **bez żadnej ochrony kupującego**. Oszustwa są powszechne. Karty nie są używane, bo
            nie ma natywnego kartowego mechanizmu dla handlu osoby-z-osobą.

            **Rozwiązanie:** Escrow napędzany kartami dla transakcji marketplace:

            **Dla Kupujących:**
            1. Przy spotkaniu lub online zeskanuj kod QR Visa sprzedającego
            2. Wpisz kwotę + opis przedmiotu + zrób zdjęcie
            3. Pieniądze są **przechowywane w escrow Visa** (pobrane z karty kupującego)
            4. Kupujący potwierdza odbiór w ciągu 48h → pieniądze zwolnione do sprzedającego
            5. Spór? Uruchamia się **pełna ochrona chargeback Visa**

            **Dla Sprzedających:**
            - Gwarantowana płatność (bez zwróconych przelewów, bez fałszywych BLIK)
            - Pieniądze na karcie Visa w ciągu 24h od potwierdzenia kupującego
            - Reputacja sprzedającego buduje się z czasem

            **Kluczowa przewaga nad BLIK P2P:** Przelew BLIK jest natychmiastowy i nieodwracalny — jeśli zostaniesz oszukany, pieniądze przepadły.
            Visa Marketplace Shield przechowuje środki, aż obie strony będą zadowolone. **Zaufanie = wyróżnik.**
            """)

    with col2:
        if lang == "EN":
            st.markdown("""
            <div style="background:#E8F5E9; padding:20px; border-radius:12px; border:2px solid #A5D6A7; color:#1A3C2A;">
                <h4 style="color:#2E7D32; margin:0 0 12px 0;">Impact Estimate</h4>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">TAM:</strong> ~15B PLN/year</p>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">OLX users:</strong> ~14M in Poland</p>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Vinted users:</strong> ~5M in Poland</p>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Avg marketplace tx:</strong> 120 PLN</p>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Target capture:</strong> 10-15%</p>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">New card volume:</strong> 1.5-2.3B PLN/yr</p>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Escrow fee:</strong> 1-2% (paid by buyer for protection)</p>
                <hr style="border-color:#A5D6A7;"/>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Data source:</strong></p>
                <p style="margin:2px 0; font-size:0.85em; color:#2E5A3A;">Visa data: Vinted 352K tx, Allegro 1.8M tx already on cards. Massive untapped OLX/FB Marketplace volume.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:#E8F5E9; padding:20px; border-radius:12px; border:2px solid #A5D6A7; color:#1A3C2A;">
                <h4 style="color:#2E7D32; margin:0 0 12px 0;">Szacowany Wpływ</h4>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">TAM:</strong> ~15 mld PLN/rok</p>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Użytkownicy OLX:</strong> ~14M w Polsce</p>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Użytkownicy Vinted:</strong> ~5M w Polsce</p>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Średnia tx marketplace:</strong> 120 PLN</p>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Docelowe przejęcie:</strong> 10-15%</p>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Nowy wolumen kartowy:</strong> 1.5-2.3 mld PLN/rok</p>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Opłata escrow:</strong> 1-2% (płacona przez kupującego za ochronę)</p>
                <hr style="border-color:#A5D6A7;"/>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Źródło danych:</strong></p>
                <p style="margin:2px 0; font-size:0.85em; color:#2E5A3A;">Dane Visa: Vinted 352K tx, Allegro 1.8M tx już na kartach. Ogromny niewykorzystany wolumen OLX/FB Marketplace.</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    st.subheader(t("Synergy: QR Pay + Marketplace Shield", "Synergia: QR Pay + Marketplace Shield"))

    if lang == "EN":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8F5E9, #C8E6C9); padding: 20px 24px; border-radius: 14px; border-left: 4px solid #43A047; color:#1A3C2A;">
            <h4 style="color:#1B5E20; margin:0 0 8px 0;">Two solutions, one ecosystem</h4>
            <p style="color:#1A3C2A; margin:0;"><strong style="color:#145A24;">Visa QR Pay</strong> provides the identity layer (scan a card to initiate payment).
            <strong style="color:#145A24;">Marketplace Shield</strong> adds the trust layer (escrow + buyer protection).
            Together they create a complete P2P commerce solution that BLIK cannot match:
            instant identification via QR + guaranteed safe transaction via escrow + full Visa chargeback protection.
            This transforms every Visa card into both a <strong style="color:#145A24;">payment tool</strong> and a <strong style="color:#145A24;">trust badge</strong>.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8F5E9, #C8E6C9); padding: 20px 24px; border-radius: 14px; border-left: 4px solid #43A047; color:#1A3C2A;">
            <h4 style="color:#1B5E20; margin:0 0 8px 0;">Dwa rozwiązania, jeden ekosystem</h4>
            <p style="color:#1A3C2A; margin:0;"><strong style="color:#145A24;">Visa QR Pay</strong> zapewnia warstwę tożsamości (zeskanuj kartę, by zainicjować płatność).
            <strong style="color:#145A24;">Marketplace Shield</strong> dodaje warstwę zaufania (escrow + ochrona kupującego).
            Razem tworzą kompletne rozwiązanie handlu P2P, którego BLIK nie może dorównać:
            natychmiastowa identyfikacja przez QR + gwarantowana bezpieczna transakcja przez escrow + pełna ochrona chargeback Visa.
            To zamienia każdą kartę Visa zarówno w <strong style="color:#145A24;">narzędzie płatnicze</strong>, jak i <strong style="color:#145A24;">odznakę zaufania</strong>.</p>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# PAGE: PREDICTIVE MODELS & SIMULATIONS
# ══════════════════════════════════════════════════════════════════════════
elif current_page == "models":
    models = load_json("model_results.json")
    st.header(t("Predictive Models & Simulations", "Modele Predykcyjne i Symulacje"))
    st.caption(t("6 models projecting Visa QR Pay adoption, transaction volume, BLIK cannibalization, ROI, and market share impact over 36 months",
                  "6 modeli prognozujacych adopcje Visa QR Pay, wolumen transakcji, kanibalizacje BLIK, ROI i wplyw na udzial rynkowy w ciagu 36 miesiecy"))

    scenario_labels = [t("Conservative", "Konserwatywny"), t("Base", "Bazowy"), t("Optimistic", "Optymistyczny")]
    scenario_map = {t("Conservative", "Konserwatywny"): "Conservative", t("Base", "Bazowy"): "Base", t("Optimistic", "Optymistyczny"): "Optimistic"}
    scenario_label = st.radio(t("Select scenario:", "Wybierz scenariusz:"), scenario_labels, index=1, horizontal=True)
    scenario = scenario_map[scenario_label]

    months_labels = [f"M{i+1}" for i in range(36)]
    year_labels = [""] * 36
    for i in [0, 11, 23, 35]:
        year_labels[i] = f"Y{i//12+1}" if i > 0 else "Start"

    # KPIs for selected scenario
    r = models["revenue"][scenario]
    a = models["adoption"][scenario]
    v = models["volume"][scenario]
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric(t("3Y Adopters", "Uzytkownicy 3L"), f"{a['cumulative'][35]/1e6:.1f}M", f"{a['penetration_pct'][35]:.0f}% {t('penetration', 'penetracji')}")
    c2.metric(t("3Y Total TX", "Lacznie TX 3L"), f"{v['cumulative_tx'][35]/1e6:.0f}M")
    c3.metric(t("3Y Total Value", "Łączna Wartość 3L"), f"{v['cumulative_val'][35]/1e9:.1f}B PLN")
    c4.metric(t("3Y Revenue", "Przychod 3L"), f"{r['total_3yr_revenue']/1e6:.0f}M PLN", f"ROI: {r['roi_pct']:.0f}%")
    be = r["breakeven_month"]
    c5.metric(t("Break-even", "Punkt Rentowności"), f"{t('Month', 'Miesiac')} {be}" if be else t("Not reached", "Nie osiagniety"), t("within 3 years", "w ciągu 3 lat") if be else t("needs more time", "potrzeba więcej czasu"))

    st.divider()

    # ── MODEL 1: ADOPTION S-CURVE ──
    st.subheader(t("Model 1: Adoption S-Curve (Bass Diffusion)", "Model 1: Krzywa Adopcji S (Dyfuzja Bassa)"))
    st.caption(t("Bass diffusion model: p = innovation coefficient (marketing), q = imitation coefficient (word-of-mouth)",
                  "Model dyfuzji Bassa: p = wspolczynnik innowacji (marketing), q = wspolczynnik imitacji (marketing szeptany)"))

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        colors_sc = {"Conservative": ACCENT[1], "Base": VISA_BLUE, "Optimistic": ACCENT[2]}
        for name in ["Conservative", "Base", "Optimistic"]:
            ad = models["adoption"][name]
            fig.add_trace(go.Scatter(x=months_labels, y=np.array(ad["cumulative"])/1e6,
                                     name=name, line=dict(color=colors_sc[name], width=3 if name==scenario else 1.5,
                                                          dash="solid" if name==scenario else "dot")))
        fig.update_layout(height=400, yaxis_title=t("Cumulative adopters (millions)", "Skumulowani użytkownicy (mln)"), title_text=t("QR Pay Adoption Curve", "Krzywa Adopcji QR Pay"),
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        for name in ["Conservative", "Base", "Optimistic"]:
            ad = models["adoption"][name]
            fig.add_trace(go.Bar(x=months_labels, y=np.array(ad["monthly_new"])/1e3,
                                 name=name, marker_color=colors_sc[name],
                                 visible=True if name==scenario else "legendonly"))
        fig.update_layout(height=400, yaxis_title=t("New adopters per month (K)", "Nowi użytkownicy/mies. (tys.)"), title_text=t("Monthly New Adopters", "Nowi Użytkownicy Miesięcznie"),
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with st.expander(t("Model assumptions", "Zalozenia modelu")):
        st.json(models["assumptions"]["adoption_params"])

    st.divider()

    # ── MODEL 2: TRANSACTION VOLUME ──
    st.subheader(t("Model 2: Transaction Volume Projection", "Model 2: Prognoza Wolumenu Transakcji"))

    sv = models["volume"][scenario]
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["p2p_tx_monthly"])/1e6,
                                 name="P2P", fill="tonexty", line=dict(color=ACCENT[0]), stackgroup="one"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["ecom_tx_monthly"])/1e6,
                                 name="E-Commerce", fill="tonexty", line=dict(color=ACCENT[3]), stackgroup="one"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["svc_tx_monthly"])/1e6,
                                 name=t("Services", "Usługi"), fill="tonexty", line=dict(color=ACCENT[2]), stackgroup="one"))
        fig.update_layout(height=400, yaxis_title=t("Monthly TX (millions)", "Miesięczne TX (mln)"), title_text=t(f"Monthly Transactions — {scenario}", f"Miesięczne Transakcje — {scenario}"),
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["p2p_val_monthly"])/1e9,
                                 name="P2P", fill="tonexty", line=dict(color=ACCENT[0]), stackgroup="one"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["ecom_val_monthly"])/1e9,
                                 name="E-Commerce", fill="tonexty", line=dict(color=ACCENT[3]), stackgroup="one"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["svc_val_monthly"])/1e9,
                                 name=t("Services", "Usługi"), fill="tonexty", line=dict(color=ACCENT[2]), stackgroup="one"))
        fig.update_layout(height=400, yaxis_title=t("Monthly value (B PLN)", "Wartość miesięczna (mld PLN)"), title_text=t(f"Monthly Transaction Value — {scenario}", f"Miesięczna Wartość Transakcji — {scenario}"),
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with st.expander(t("Activity assumptions per user/month", "Zalozenia aktywnosci na uzytkownika/miesiac")):
        st.json(models["assumptions"]["activity_params"])

    st.divider()

    # ── MODEL 3: CANNIBALIZATION ──
    st.subheader(t("Model 3: BLIK Cannibalization vs Net New Volume", "Model 3: Kanibalizacja BLIK vs Nowy Wolumen Netto"))
    st.caption(t("How much QR Pay volume is taken from BLIK vs genuinely new card transaction volume?",
                  "Ile wolumenu QR Pay jest przejete od BLIK vs faktycznie nowy wolumen transakcji kartowych?"))

    cn = models["cannibalization"][scenario]
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(cn["net_new_monthly"])/1e6,
                                 name=t("Net new to Visa (from cash/transfer)", "Nowe netto dla Visa (z gotówki/przelewów)"), fill="tozeroy",
                                 line=dict(color=ACCENT[2]), fillcolor="rgba(46,204,113,0.3)"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(cn["from_blik_monthly"])/1e6,
                                 name=t("Cannibalized from BLIK", "Skanibalizowane z BLIK"), fill="tozeroy",
                                 line=dict(color=BLIK_PINK), fillcolor="rgba(212,14,106,0.2)"))
        fig.update_layout(height=400, yaxis_title=t("Monthly value (M PLN)", "Wartość miesięczna (M PLN)"), title_text=t(f"Source of QR Pay Volume — {scenario}", f"Źródło Wolumenu QR Pay — {scenario}"),
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Pie at month 36
        net_new_36 = cn["net_new_monthly"][35]
        blik_36 = cn["from_blik_monthly"][35]
        existing_36 = cn["from_existing_card"][35]
        fig = px.pie(names=[t("Net new (cash/transfer → card)", "Nowe netto (gotówka/przelew → karta)"), t("From BLIK", "Z BLIK"), t("From existing card", "Z istniejącej karty")],
                     values=[net_new_36, blik_36, existing_36],
                     color_discrete_sequence=[ACCENT[2], BLIK_PINK, ACCENT[0]], hole=0.35,
                     title=t(f"Volume Source at Month 36 — {scenario}", f"Źródło Wolumenu w Miesiącu 36 — {scenario}"))
        fig.update_layout(height=400, margin=dict(t=40,b=30))
        st.plotly_chart(fig, use_container_width=True)

    net_new_pct = cn["net_new_pct"][35]
    if lang == "EN":
        st.info(f"**{scenario} scenario at Month 36:** {net_new_pct:.0f}% of QR Pay volume is NET NEW to the card ecosystem (from cash/transfers). {100-net_new_pct:.0f}% is cannibalized from BLIK or existing card channels.")
    else:
        st.info(f"**Scenariusz {scenario} w Miesiącu 36:** {net_new_pct:.0f}% wolumenu QR Pay to NOWE NETTO dla ekosystemu kartowego (z gotówki/przelewów). {100-net_new_pct:.0f}% jest skanibalizowane z BLIK lub istniejących kanałów kartowych.")

    st.divider()

    # ── MODEL 4: REVENUE & ROI ──
    st.subheader(t("Model 4: Revenue & ROI Projection", "Model 4: Prognoza Przychodu i ROI"))

    rv = models["revenue"][scenario]
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["cumulative_revenue"])/1e6,
                                 name=t("Cumulative Revenue", "Skumulowany Przychód"), line=dict(color=ACCENT[2], width=3), fill="tozeroy", fillcolor="rgba(46,204,113,0.15)"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["cumulative_costs"])/1e6,
                                 name=t("Cumulative Costs", "Skumulowane Koszty"), line=dict(color=ACCENT[1], width=3, dash="dash")))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["cumulative_profit"])/1e6,
                                 name=t("Cumulative Profit", "Skumulowany Zysk"), line=dict(color=VISA_BLUE, width=3)))
        if rv["breakeven_month"]:
            fig.add_vline(x=rv["breakeven_month"]-1, line_dash="dot", line_color=VISA_GOLD,
                          annotation_text=t(f"Break-even: M{rv['breakeven_month']}", f"Punkt rentowności: M{rv['breakeven_month']}"))
        fig.update_layout(height=400, yaxis_title=t("PLN (millions)", "PLN (mln)"), title_text=t(f"Cumulative P&L — {scenario}", f"Skumulowany P&L — {scenario}"),
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["p2p_rev"])/1e6,
                                 name=t("P2P revenue", "Przychód P2P"), fill="tonexty", stackgroup="one", line=dict(color=ACCENT[0])))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["ecom_rev"])/1e6,
                                 name=t("E-commerce revenue", "Przychód e-commerce"), fill="tonexty", stackgroup="one", line=dict(color=ACCENT[3])))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["svc_rev"])/1e6,
                                 name=t("Services revenue", "Przychód z usług"), fill="tonexty", stackgroup="one", line=dict(color=ACCENT[2])))
        fig.update_layout(height=400, yaxis_title=t("Monthly revenue (M PLN)", "Przychód miesięczny (M PLN)"), title_text=t(f"Revenue by Channel — {scenario}", f"Przychód wg Kanału — {scenario}"),
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with st.expander(t("Cost breakdown", "Rozkład kosztów")):
        st.json(models["costs"])

    st.divider()

    # ── MODEL 5: E-COMMERCE MARKET SHARE ──
    st.subheader(t("Model 5: E-Commerce Market Share Simulation", "Model 5: Symulacja Udzialu w Rynku E-Commerce"))
    st.caption(t("How QR Pay changes Visa's share of the Polish e-commerce payments market",
                  "Jak QR Pay zmienia udzial Visa w polskim rynku płatności e-commerce"))

    es = models["ecom_share"][scenario]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months_labels, y=es["visa_share_pct"], name=t("Visa total (card + QR Pay)", "Visa łącznie (karta + QR Pay)"),
                             line=dict(color=VISA_BLUE, width=3)))
    fig.add_trace(go.Scatter(x=months_labels, y=es["visa_base_share"], name=t("Visa baseline (without QR Pay)", "Visa bazowo (bez QR Pay)"),
                             line=dict(color=VISA_BLUE, width=1.5, dash="dot")))
    fig.add_trace(go.Scatter(x=months_labels, y=es["blik_share_pct"], name=t("BLIK (adjusted)", "BLIK (skorygowany)"),
                             line=dict(color=BLIK_PINK, width=3)))
    fig.add_hline(y=es["visa_base_share"][0], line_dash="dash", line_color="#ccc",
                  annotation_text=t(f"Current Visa e-com share: {es['visa_base_share'][0]:.1f}%", f"Obecny udział Visa e-com: {es['visa_base_share'][0]:.1f}%"))
    fig.update_layout(height=450, yaxis_title=t("Market share (%)", "Udział rynkowy (%)"), title_text=t(f"E-Commerce Payment Share — {scenario}", f"Udział w Płatnościach E-Commerce — {scenario}"),
                      legend=dict(orientation="h",y=-0.12), margin=dict(t=40,b=40))
    st.plotly_chart(fig, use_container_width=True)

    visa_start = es["visa_share_pct"][0]
    visa_end = es["visa_share_pct"][35]
    blik_start = es["blik_share_pct"][0]
    blik_end = es["blik_share_pct"][35]
    if lang == "EN":
        st.success(f"**{scenario}:** Visa e-commerce share moves from **{visa_start:.1f}%** to **{visa_end:.1f}%** (+{visa_end-visa_start:.1f}pp). BLIK declines from **{blik_start:.1f}%** to **{blik_end:.1f}%** ({blik_end-blik_start:+.1f}pp).")
    else:
        st.success(f"**{scenario}:** Udział Visa w e-commerce rośnie z **{visa_start:.1f}%** do **{visa_end:.1f}%** (+{visa_end-visa_start:.1f}pp). BLIK spada z **{blik_start:.1f}%** do **{blik_end:.1f}%** ({blik_end-blik_start:+.1f}pp).")

    st.divider()

    # ── MODEL 6: SENSITIVITY ──
    st.subheader(t("Model 6: Sensitivity Analysis", "Model 6: Analiza Wrazliwosci"))
    st.caption(t("How 3-year revenue changes when we vary each key parameter ±50% from base",
                  "Jak zmienia sie 3-letni przychod gdy modyfikujemy kazdy kluczowy parametr ±50% od bazy"))

    sens = pd.DataFrame(models["sensitivity"])
    base_rev = sens[(sens["parameter"]==sens["parameter"].iloc[0]) & (sens["multiplier"]==1.0)]["revenue_3yr_mln"].values[0]

    param_choice = st.selectbox(t("Select parameter:", "Wybierz parametr:"), sens["parameter"].unique())
    df_p = sens[sens["parameter"] == param_choice]

    fig = go.Figure()
    colors_bar = df_p["multiplier"].apply(lambda m: VISA_BLUE if m == 1.0 else (ACCENT[2] if m > 1 else ACCENT[1]))
    fig.add_trace(go.Bar(x=df_p["multiplier"].apply(lambda m: f"{m:.0%}"), y=df_p["revenue_3yr_mln"],
                         marker_color=colors_bar.tolist(), text=df_p["revenue_3yr_mln"].apply(lambda v: f"{v:.0f}M"),
                         textposition="outside"))
    fig.add_hline(y=base_rev, line_dash="dash", line_color=VISA_GOLD, annotation_text=t(f"Base: {base_rev:.0f}M PLN", f"Baza: {base_rev:.0f}M PLN"))
    fig.update_layout(height=400, yaxis_title=t("3-year revenue (M PLN)", "Przychód 3-letni (M PLN)"),
                      xaxis_title=t(f"{param_choice} (multiplier vs base)", f"{param_choice} (mnożnik vs baza)"),
                      title_text=t(f"Sensitivity: {param_choice}", f"Wrażliwość: {param_choice}"), margin=dict(t=40,b=40))
    st.plotly_chart(fig, use_container_width=True)

    # Tornado chart
    st.subheader(t("Tornado Chart: Revenue Sensitivity to All Parameters", "Wykres Tornado: Wrazliwosc Przychodu na Wszystkie Parametry"))
    tornado = []
    for param in sens["parameter"].unique():
        df_param = sens[sens["parameter"] == param]
        low = df_param[df_param["multiplier"] == 0.5]["revenue_3yr_mln"].values[0]
        high = df_param[df_param["multiplier"] == 1.5]["revenue_3yr_mln"].values[0]
        base = df_param[df_param["multiplier"] == 1.0]["revenue_3yr_mln"].values[0]
        tornado.append({"Parameter": param, "Low (50%)": low - base, "High (150%)": high - base, "Range": high - low})

    df_torn = pd.DataFrame(tornado).sort_values("Range", ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(y=df_torn["Parameter"], x=df_torn["Low (50%)"], name=t("50% of base", "50% bazy"),
                         orientation="h", marker_color=ACCENT[1]))
    fig.add_trace(go.Bar(y=df_torn["Parameter"], x=df_torn["High (150%)"], name=t("150% of base", "150% bazy"),
                         orientation="h", marker_color=ACCENT[2]))
    fig.update_layout(height=400, xaxis_title=t("Impact on 3Y revenue (M PLN vs base)", "Wpływ na przychód 3L (M PLN vs baza)"),
                      barmode="overlay", title_text=t("Tornado: Which Parameters Matter Most", "Tornado: Które Parametry Mają Największe Znaczenie"),
                      legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── SCENARIO COMPARISON TABLE ──
    st.subheader(t("Scenario Comparison Summary", "Porównanie Scenariuszy"))
    comp_data = []
    for name in ["Conservative", "Base", "Optimistic"]:
        a = models["adoption"][name]
        v = models["volume"][name]
        r = models["revenue"][name]
        cn = models["cannibalization"][name]
        if lang == "EN":
            comp_data.append({
                "Scenario": name,
                "Y3 Adopters": f"{a['cumulative'][35]/1e6:.1f}M",
                "Y3 Penetration": f"{a['penetration_pct'][35]:.0f}%",
                "Y3 Monthly TX": f"{v['total_tx_monthly'][35]/1e6:.1f}M",
                "Y3 Monthly Value": f"{v['total_val_monthly'][35]/1e9:.1f}B PLN",
                "3Y Revenue": f"{r['total_3yr_revenue']/1e6:.0f}M PLN",
                "3Y Profit": f"{r['total_3yr_profit']/1e6:.0f}M PLN",
                "ROI": f"{r['roi_pct']:.0f}%",
                "Break-even": f"Month {r['breakeven_month']}" if r["breakeven_month"] else "Not reached",
                "Net New %": f"{cn['net_new_pct'][35]:.0f}%",
            })
        else:
            comp_data.append({
                "Scenariusz": name,
                "Użytkownicy 3L": f"{a['cumulative'][35]/1e6:.1f}M",
                "Penetracja 3L": f"{a['penetration_pct'][35]:.0f}%",
                "Mies. TX 3L": f"{v['total_tx_monthly'][35]/1e6:.1f}M",
                "Mies. Wartość 3L": f"{v['total_val_monthly'][35]/1e9:.1f} mld PLN",
                "Przychód 3L": f"{r['total_3yr_revenue']/1e6:.0f}M PLN",
                "Zysk 3L": f"{r['total_3yr_profit']/1e6:.0f}M PLN",
                "ROI": f"{r['roi_pct']:.0f}%",
                "Punkt rentowności": f"Miesiąc {r['breakeven_month']}" if r["breakeven_month"] else "Nie osiągnięty",
                "Nowe netto %": f"{cn['net_new_pct'][35]:.0f}%",
            })
    st.dataframe(pd.DataFrame(comp_data), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════
# PAGE: RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════
elif current_page == "recs":
    st.header(t("Strategic Recommendations", "Rekomendacje Strategiczne"))
    if lang == "EN":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8EDF8, #D0D9F0); padding: 24px 28px; border-radius: 14px; color: #0D1137; margin-bottom: 20px; border: 2px solid #B0BDE0;">
            <h3 style="margin:0; color:#1A1F71;">CardFlow — From Cash & Transfer to Card</h3>
            <p style="color:#333; margin-top:6px;">We turn transaction data into concrete decisions. We show not just how people pay,
            but what to do to make the card their most convenient choice — online and in private payments.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8EDF8, #D0D9F0); padding: 24px 28px; border-radius: 14px; color: #0D1137; margin-bottom: 20px; border: 2px solid #B0BDE0;">
            <h3 style="margin:0; color:#1A1F71;">CardFlow — Od Gotówki i Przelewów do Karty</h3>
            <p style="color:#333; margin-top:6px;">Zamieniamy dane transakcyjne w konkretne decyzje. Pokazujemy nie tylko jak ludzie płacą,
            ale co zrobić, by karta była ich najwygodniejszym wyborem — online i w płatności prywatnych.</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader(t("For Three Target Audiences", "Dla Trzech Grup Docelowych"))

    tab1, tab2, tab3 = st.tabs([t("🛍️ Online Merchants", "🛍️ Dla Sklepów Internetowych"),
                                 t("🏦 Banks & Visa", "🏦 Dla Banków i Visa"),
                                 t("🏙️ Cities & Municipalities", "🏙️ Dla Miast i Samorządów")])

    with tab1:
        if lang == "EN":
            st.markdown("""
            ### Online Merchants: Reduce Friction, Increase Card Share

            | Escape Point Identified | Recommendation | Expected Impact |
            |---|---|---|
            | **67% of e-commerce uses BLIK** because it's one-click | Implement **Visa Click to Pay** — tokenized one-click card payment | +3-5pp card share |
            | **E-grocery at 0.12%** online | Launch card-first checkout for grocery delivery (Frisco, Barbora) | Avg online basket 3.1× higher |
            | **Online avg = 318 vs 165 physical** | Promote card for high-value online purchases (electronics, furniture) | Higher revenue per TX |
            | **Clothing online: 5% of TX, 16% of value** | Card-on-file + saved checkout for fashion e-commerce | Lock in repeat buyers |
            | **COD still 5% of e-commerce** | Offer "Pay now with card, get free shipping" incentive | Convert COD → card |
            | **BLIK lacks chargeback protection** | Highlight Visa buyer protection for expensive purchases | Trust advantage for >200 PLN |

            **Quick Win:** Partner with Allegro (1.8M card TX already) to make Visa Click to Pay as prominent as BLIK at checkout.
            """)
        else:
            st.markdown("""
            ### Sklepy internetowe: Zmniejsz tarcie, zwiększ udział kart

            | Zidentyfikowany punkt ucieczki | Rekomendacja | Oczekiwany wpływ |
            |---|---|---|
            | **67% e-commerce używa BLIK** bo jest jednym kliknięciem | Wdrożyć **Visa Click to Pay** — tokenizowana płatność kartą jednym kliknięciem | +3-5pp udziału kart |
            | **E-grocery na 0.12%** online | Uruchomić checkout karta-najpierw dla dostaw spożywczych (Frisco, Barbora) | Średni koszyk online 3.1× wyższy |
            | **Średnia online = 318 vs 165 fizyczna** | Promować kartę dla zakupów online o wysokiej wartości (elektronika, meble) | Wyższy przychód na TX |
            | **Odzież online: 5% TX, 16% wartości** | Card-on-file + zapisany checkout dla mody e-commerce | Zatrzymanie stałych kupujących |
            | **Za pobraniem nadal 5% e-commerce** | Zaoferować "Zapłać kartą, dostawa gratis" | Konwersja pobrania → karta |
            | **BLIK nie ma ochrony chargeback** | Podkreślić ochronę kupującego Visa przy drogich zakupach | Przewaga zaufania >200 PLN |

            **Szybka wygrana:** Partnerstwo z Allegro (już 1.8M TX kartowych), by Visa Click to Pay był tak widoczny jak BLIK przy kasie.
            """)

    with tab2:
        if lang == "EN":
            st.markdown("""
            ### Banks & Visa: Activate Cards in New Channels

            | Segment | Current State | Visa Direct / Card Opportunity |
            |---|---|---|
            | **P2P payments** | BLIK 55%, card ~2% | **Visa Direct** for instant P2P — "split the bill by card" |
            | **Subscriptions** | 282K cards on Netflix, 240K on Apple | Promote card-on-file for ALL subscriptions (telecom, insurance) |
            | **Recurring bills** | 3% card, 90% transfer/direct debit | Card-linked bill payment with **2% cashback** incentive |
            | **Ages 65+** | 72% cash preference | Simplified contactless card for seniors + education |
            | **Ages 45-64** | 40% cash | "Your card works online too" campaign |
            | **Micro-payments <10 PLN** | 65% cash | Zero-fee contactless under 10 PLN for merchants |
            | **ATM heavy users** | Avg 1,521/withdrawal | Identify & target with "why withdraw when you can tap?" |

            **Quick Win:** Launch "Visa Split" — P2P card-to-card transfers integrated in banking apps, competing directly with BLIK P2P.

            **Visa Direct opportunity:** 14.5M households paying 416 PLN/month in rent + 68 PLN telecom = **7B PLN/month** in potential card-linked payments.
            """)
        else:
            st.markdown("""
            ### Banki i Visa: Aktywuj karty w nowych kanałach

            | Segment | Obecny stan | Szansa Visa Direct / Karta |
            |---|---|---|
            | **Płatności P2P** | BLIK 55%, karta ~2% | **Visa Direct** na natychmiastowe P2P — "podziel rachunek kartą" |
            | **Subskrypcje** | 282K kart na Netflix, 240K na Apple | Promować card-on-file dla WSZYSTKICH subskrypcji (telekom, ubezpieczenia) |
            | **Rachunki cykliczne** | 3% karta, 90% przelew/polecenie zapłaty | Płatność rachunków powiązana z kartą z **2% cashback** |
            | **Wiek 65+** | 72% preferencja gotówki | Uproszczona karta zbliżeniowa dla seniorów + edukacja |
            | **Wiek 45-64** | 40% gotówka | Kampania "Twoja karta działa też online" |
            | **Mikropłatności <10 PLN** | 65% gotówka | Zerowa opłata za zbliżeniowe poniżej 10 PLN dla merchantów |
            | **Intensywni użytkownicy ATM** | Średnia 1 521/wypłata | Zidentyfikuj i targetuj "po co wypłacać, skoro możesz przykładać?" |

            **Szybka wygrana:** Uruchomienie "Visa Split" — przelewy karta-do-karty P2P zintegrowane w aplikacjach bankowych, bezpośrednia konkurencja z BLIK P2P.

            **Szansa Visa Direct:** 14.5M gospodarstw płacących 416 PLN/mies. czynszu + 68 PLN telekom = **7 mld PLN/mies.** potencjalnych płatności powiązanych z kartą.
            """)

    with tab3:
        if lang == "EN":
            st.markdown("""
            ### Cities & Municipalities: Cashless Local Economy

            | Urban Challenge | Data Insight | Solution |
            |---|---|---|
            | **Open-air markets** | 15% terminal coverage | **Tap-to-Phone** program for market vendors (zero cost) |
            | **Local transport** | 3.8M tx, but 1M via apps only | Contactless card validators on all buses/trams |
            | **Parking** | 2.8M tx at meters/garages | Universal card-tap parking meters |
            | **Municipal fees** | 60% terminal coverage | Online card payment portal for all city services |
            | **Local events/festivals** | Cash-heavy by tradition | Cashless event wristbands linked to Visa |
            | **Food trucks & street food** | 50% terminal coverage | SumUp/Zettle micro-POS deployment program |
            | **Public institutions** | 60% terminals | Card payment kiosks in offices |

            **Case Study Potential:** Partner with one Polish city (e.g., Kraków — highest card mobility at 17.7%)
            for a **"Cashless City" pilot** — measure impact on local commerce, tax revenue visibility, and tourist spending.
            """)
        else:
            st.markdown("""
            ### Miasta i samorządy: Bezgotówkowa lokalna gospodarka

            | Wyzwanie miejskie | Dane | Rozwiązanie |
            |---|---|---|
            | **Targowiska** | 15% pokrycia terminali | Program **Tap-to-Phone** dla sprzedawców targowych (zero kosztów) |
            | **Transport lokalny** | 3.8M tx, ale 1M tylko przez aplikacje | Walidatory kart zbliżeniowych we wszystkich autobusach/tramwajach |
            | **Parking** | 2.8M tx w parkometrach/garażach | Uniwersalne parkometry z tap kartą |
            | **Opłaty miejskie** | 60% pokrycia terminali | Portal płatności kartą online dla wszystkich usług miejskich |
            | **Lokalne imprezy/festiwale** | Tradycyjnie gotówkowe | Bezgotówkowe opaski eventowe powiązane z Visa |
            | **Food trucki i street food** | 50% pokrycia terminali | Program wdrożenia mikro-POS SumUp/Zettle |
            | **Instytucje publiczne** | 60% terminali | Kioski płatności kartą w urzędach |

            **Potencjał studium przypadku:** Partnerstwo z jednym polskim miastem (np. Kraków — najwyższa mobilność kartowa 17.7%)
            dla pilotażu **"Miasto Bezgotówkowe"** — pomiar wpływu na lokalny handel, widoczność przychodów podatkowych i wydatki turystów.
            """)

    st.divider()
    st.subheader(t("Priority Matrix", "Macierz Priorytetów"))

    if lang == "EN":
        priorities = pd.DataFrame([
            {"Initiative": "Visa Click to Pay at top merchants", "Impact": "High", "Effort": "Medium", "Timeline": "3-6 months", "Target": "Merchants"},
            {"Initiative": "E-grocery card-first checkout", "Impact": "High", "Effort": "Medium", "Timeline": "3-6 months", "Target": "Merchants"},
            {"Initiative": "Tap-to-Phone for service providers", "Impact": "High", "Effort": "Low", "Timeline": "1-3 months", "Target": "Visa/Banks"},
            {"Initiative": "Visa Direct P2P in banking apps", "Impact": "Very High", "Effort": "High", "Timeline": "6-12 months", "Target": "Banks"},
            {"Initiative": "Card-on-file for recurring bills", "Impact": "Very High", "Effort": "High", "Timeline": "6-12 months", "Target": "Banks"},
            {"Initiative": "Zero-fee micro-payments", "Impact": "Medium", "Effort": "Low", "Timeline": "1-3 months", "Target": "Visa"},
            {"Initiative": "Cashless City pilot", "Impact": "High", "Effort": "High", "Timeline": "6-12 months", "Target": "Cities"},
            {"Initiative": "Senior contactless education", "Impact": "Medium", "Effort": "Low", "Timeline": "1-3 months", "Target": "Banks"},
        ])
    else:
        priorities = pd.DataFrame([
            {"Inicjatywa": "Visa Click to Pay u top merchantów", "Wpływ": "Wysoki", "Nakład": "Średni", "Harmonogram": "3-6 miesięcy", "Cel": "Merchanci"},
            {"Inicjatywa": "E-grocery checkout karta-najpierw", "Wpływ": "Wysoki", "Nakład": "Średni", "Harmonogram": "3-6 miesięcy", "Cel": "Merchanci"},
            {"Inicjatywa": "Tap-to-Phone dla usługodawców", "Wpływ": "Wysoki", "Nakład": "Niski", "Harmonogram": "1-3 miesiące", "Cel": "Visa/Banki"},
            {"Inicjatywa": "Visa Direct P2P w aplikacjach bankowych", "Wpływ": "Bardzo Wysoki", "Nakład": "Wysoki", "Harmonogram": "6-12 miesięcy", "Cel": "Banki"},
            {"Inicjatywa": "Card-on-file dla rachunków cyklicznych", "Wpływ": "Bardzo Wysoki", "Nakład": "Wysoki", "Harmonogram": "6-12 miesięcy", "Cel": "Banki"},
            {"Inicjatywa": "Zerowe opłaty za mikropłatności", "Wpływ": "Średni", "Nakład": "Niski", "Harmonogram": "1-3 miesiące", "Cel": "Visa"},
            {"Inicjatywa": "Pilotaż Miasto Bezgotówkowe", "Wpływ": "Wysoki", "Nakład": "Wysoki", "Harmonogram": "6-12 miesięcy", "Cel": "Miasta"},
            {"Inicjatywa": "Edukacja zbliżeniowa dla seniorów", "Wpływ": "Średni", "Nakład": "Niski", "Harmonogram": "1-3 miesiące", "Cel": "Banki"},
        ])
    st.dataframe(priorities, use_container_width=True, hide_index=True)

    st.divider()
    if lang == "EN":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFF9E6, #FFF3CC); padding: 20px 24px; border-radius: 14px; border-left: 4px solid #F7B600; color:#3D2E00;">
            <h3 style="color:#0D1137; margin:0 0 8px 0;">The Bottom Line</h3>
            <p style="margin:0; font-size:1.05em; color:#3D2E00;">
            Cards already dominate physical POS (58% and growing). But <strong style="color:#1A1F71;">~25% of household spending</strong> (housing, telecom, education)
            is invisible to cards, and in e-commerce <strong style="color:#1A1F71;">BLIK has captured 67%</strong>. The opportunity is not to fight BLIK head-on
            in domestic one-click payments, but to <strong style="color:#1A1F71;">own the niches where cards have structural advantages</strong>:
            international commerce, subscriptions, high-value purchases with buyer protection, P2P via Visa Direct,
            and the untapped recurring bills market. Combined, these represent <strong style="color:#1A1F71;">tens of billions of PLN in annual payment volume</strong>
            currently flowing through non-card channels.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFF9E6, #FFF3CC); padding: 20px 24px; border-radius: 14px; border-left: 4px solid #F7B600; color:#3D2E00;">
            <h3 style="color:#0D1137; margin:0 0 8px 0;">Podsumowanie</h3>
            <p style="margin:0; font-size:1.05em; color:#3D2E00;">
            Karty juz dominuja na fizycznych POS (58% i rosnie). Ale <strong style="color:#1A1F71;">~25% wydatkow gospodarstw domowych</strong> (mieszkanie, telekom, edukacja)
            jest niewidoczne dla kart, a w e-commerce <strong style="color:#1A1F71;">BLIK przejal 67%</strong>. Szansa nie polega na walce z BLIK czolowo
            w krajowych platnosci jednym kliknieciem, ale na <strong style="color:#1A1F71;">zajmowaniu nisz, gdzie karty maja strukturalne przewagi</strong>:
            handel międzynarodowy, subskrypcje, zakupy o wysokiej wartości z ochroną kupującego, P2P przez Visa Direct
            i niewykorzystany rynek rachunkow cyklicznych. Lacznie to <strong style="color:#1A1F71;">dziesiatki miliardow PLN rocznego wolumenu platnosci</strong>
            plynacych obecnie przez kanaly nie-kartowe.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.divider()
st.caption(t("CardFlow — Visa DataSprint Hackathon 2026 | Data: Visa synthetic transactions (305.5M), GUS (2024), NBP (2024), Gemius (2024)",
              "CardFlow — Visa DataSprint Hackathon 2026 | Dane: Syntetyczne transakcje Visa (305.5M), GUS (2024), NBP (2024), Gemius (2024)"))
