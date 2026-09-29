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
            <p style="opacity:0.9; font-size:1.1em; margin-top:4px;">Dane transakcyjne jako mapa drogowa adopcji kart w e-commerce i platnosci P2P</p>
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
        > **Karty płatnicze dominują w sklepach stacjonarnych, ale w e-commerce i platnosci peer-to-peer sa wypierane
        > przez inne metody.** W Polsce BLIK, szybkie przelewy i gotowka to glowne alternatywy. Uzytkownicy wybieraja je,
        > bo są szybsze, nie wymagają wpisywania numeru karty i wydają się bezpieczniejsze. Ta sama osoba płaci kartą
        > w sklepie osiedlowym, ale online lub placac znajomemu — wybiera inna metode.
        >
        > **CardFlow** wykorzystuje zanonimizowane, zagregowane dane transakcyjne, by zrozumiec *kiedy, gdzie i dlaczego*
        > karta przestaje być pierwszym wyborem. Analizujemy wzorce zachowan wedlug kategorii merchantow, pory dnia,
        > wartości koszyka i lokalizacji. Identyfikujemy **"punkty ucieczki"** — momenty, w ktorych klienci zmieniaja metode platnosci.
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
        fig.add_trace(go.Scatter(x=years, y=[44,50,53,55,57,58], name="Card at POS (%)", line=dict(color=VISA_BLUE, width=3)))
        fig.add_trace(go.Scatter(x=years, y=[54,47,43,40,37,35], name="Cash at POS (%)", line=dict(color=ACCENT[1], width=3, dash="dash")))
        fig.add_trace(go.Scatter(x=years, y=[5,10,15,22,30,42], name="BLIK tx (×100M)", line=dict(color=BLIK_PINK, width=3)))
        fig.update_layout(height=350, margin=dict(t=10,b=30), legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("E-Commerce Payment Methods 2024", "Metody Platnosci E-Commerce 2024"))
        fig = px.pie(
            names=["BLIK (67%)", "Card (16%)", "Bank Transfer (10%)", "Cash on Delivery (5%)", "Other (2%)"],
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
                      "**Fosa Visa:** Subskrypcje (Apple, Netflix, Spotify) + miedzynarodowy e-commerce = ~8M tx na szynach kart."))

    f4, f5, f6 = st.columns(3)
    with f4:
        st.info(t("**E-Grocery Gap:** 26% of card tx are grocery but only 0.12% online. Online avg = 3.1x higher value.",
                   "**Luka E-Grocery:** 26% tx kartowych to spozywcze, ale tylko 0.12% online. Srednia online = 3.1x wyzsza wartosc."))
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
            Kod QR na kazdej karcie Visa umozliwia <strong style="color:white;">dwa nowe sposoby platnosci</strong>:
            (1) <strong style="color:white;">Platnosci P2P</strong> — zeskanuj karte znajomego, by wyslac mu pieniadze, konkurujac bezposrednio z BLIK P2P;
            (2) <strong style="color:white;">Platnosci e-commerce</strong> — zeskanuj wlasna karte zamiast wpisywac numer, szybciej i bezpieczniej niz jakakolwiek istniejaca metoda.
            Bez udostepniania numeru karty, zatwierdzenie biometryczne, napedzane przez Visa Direct.
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
        fig.add_trace(go.Bar(x=df_m["month"], y=df_m["tx_count"]/1e6, name="Transactions (M)", marker_color=VISA_BLUE, opacity=0.7), secondary_y=False)
        fig.add_trace(go.Scatter(x=df_m["month"], y=df_m["total_amount"]/1e9, name="Value (B)", line=dict(color=VISA_GOLD, width=3)), secondary_y=True)
        fig.update_yaxes(title_text="Transactions (M)", secondary_y=False)
        fig.update_yaxes(title_text="Value (B)", secondary_y=True)
        fig.update_layout(height=400, margin=dict(t=10,b=30), legend=dict(orientation="h",y=-0.2))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("Average Transaction Value Over Time", "Średnia Wartość Transakcji w Czasie"))
        fig = px.line(df_m, x="month", y="avg_amount", markers=True)
        fig.update_traces(line_color=ACCENT[0], line_width=3)
        fig.update_layout(height=400, margin=dict(t=10,b=30), yaxis_title="Avg amount", yaxis_range=[170,200])
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
        fig.add_trace(go.Bar(x=df_h["hour_label"], y=df_h["tx_count"]/1e6, name="TX (M)", marker_color=VISA_BLUE, opacity=0.6), secondary_y=False)
        fig.add_trace(go.Scatter(x=df_h["hour_label"], y=df_h["avg_amount"], name="Avg amount", line=dict(color=VISA_GOLD, width=2)), secondary_y=True)
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
        fig.update_layout(height=350, margin=dict(t=10,b=30), yaxis_title="TX (millions)")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Top categories & merchants
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Top 15 Merchant Categories", "Top 15 Kategorii Merchantow"))
        cats = analysis["top_categories"][:15]
        df_c = pd.DataFrame(cats)
        fig = px.bar(df_c, y="mrch_catg_nm", x="tx_count", orientation="h", color_discrete_sequence=[VISA_BLUE])
        fig.update_layout(height=500, margin=dict(t=10,b=10,l=10), yaxis=dict(autorange="reversed"), xaxis_title="Transactions")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("Top 15 Merchants", "Top 15 Merchantow"))
        merch = analysis["top_merchants"][:15]
        df_me = pd.DataFrame(merch)
        fig = px.bar(df_me, y="mrch_nm_raw", x="tx_count", orientation="h", color_discrete_sequence=[ACCENT[3]])
        fig.update_layout(height=500, margin=dict(t=10,b=10,l=10), yaxis=dict(autorange="reversed"), xaxis_title="Transactions")
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
        labels = ["Physical (88.8%)", "Online (11.2%)"]
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
        fig.add_trace(go.Bar(x=df_t["month"], y=df_t["online_tx"]/1e6, name="Online TX (M)", marker_color=VISA_BLUE, opacity=0.7), secondary_y=False)
        fig.add_trace(go.Scatter(x=df_t["month"], y=df_t["online_tx_pct"], name="Online % of TX", line=dict(color=VISA_GOLD, width=3)), secondary_y=True)
        fig.update_yaxes(title_text="Online TX (M)", secondary_y=False)
        fig.update_yaxes(title_text="Online share (%)", secondary_y=True)
        fig.update_layout(height=380, margin=dict(t=10,b=30), legend=dict(orientation="h",y=-0.2), title_text="Online transaction volume & share")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_t["month"], y=df_t["online_tx_pct"], name="% of TX", line=dict(color=VISA_BLUE, width=2), mode="lines+markers"))
        fig.add_trace(go.Scatter(x=df_t["month"], y=df_t["online_val_pct"], name="% of Value", line=dict(color=ACCENT[1], width=2), mode="lines+markers"))
        fig.update_layout(height=380, margin=dict(t=10,b=30), yaxis_title="Online share (%)", title_text="Online share: transactions vs value", legend=dict(orientation="h",y=-0.2))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Top online categories
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Top Online Categories (by TX count)", "Top Kategorie Online (wg liczby TX)"))
        top_ecom = ecommerce["ecommerce_top_categories"][:15]
        df_ec = pd.DataFrame(top_ecom)
        fig = px.bar(df_ec, y="mrch_catg_nm", x="tx_count", orientation="h", color_discrete_sequence=[VISA_BLUE])
        fig.update_layout(height=500, margin=dict(t=10,b=10,l=10), yaxis=dict(autorange="reversed"), xaxis_title="Transactions")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("Top Online Merchants", "Top Merchanci Online"))
        top_merch = ecommerce["ecommerce_top_merchants"][:20]
        df_em = pd.DataFrame(top_merch)
        fig = px.bar(df_em, y="mrch_nm_raw", x="tx_count", orientation="h", color_discrete_sequence=[ACCENT[3]],
                     hover_data=["mrch_catg_nm", "avg_amount", "unique_cards"])
        fig.update_layout(height=500, margin=dict(t=10,b=10,l=10), yaxis=dict(autorange="reversed"), xaxis_title="Transactions")
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
        st.subheader(t("Online vs Physical: Avg Transaction Value", "Online vs Fizyczne: Srednia Wartosc Transakcji"))
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
        df_cmp = pd.DataFrame(cats_compare)
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Physical", y=df_cmp["cat"], x=df_cmp["physical"], orientation="h", marker_color=VISA_BLUE, opacity=0.7))
        fig.add_trace(go.Bar(name="Online", y=df_cmp["cat"], x=df_cmp["online"], orientation="h", marker_color=ACCENT[1]))
        fig.update_layout(height=350, margin=dict(t=10,b=30), barmode="group", xaxis_title="Avg transaction value", legend=dict(orientation="h",y=-0.15))
        st.plotly_chart(fig, use_container_width=True)

    st.info(t("💡 **Key Insight:** Online transactions average **318** (1.9× physical at 165). In clothing the multiplier is **3.6×** (646 online vs 179 in-store). Every physical transaction converted to online generates ~2× the card revenue.",
               "💡 **Kluczowy Wniosek:** Transakcje online srednio **318** (1.9× fizyczne przy 165). W odziezi mnoznik to **3.6×** (646 online vs 179 w sklepie). Kazda fizyczna transakcja przekonwertowana na online generuje ~2× przychod kartowy."))

    st.divider()

    # Categories with lowest online penetration
    st.subheader(t("Categories With Lowest Online Penetration (E-Commerce Desert)", "Kategorie z Najniższą Penetracją Online (Pustynia E-Commerce)"))
    online_det = precise["online_detailed"][:15]
    df_od = pd.DataFrame(online_det)
    fig = px.bar(df_od, y="mrch_catg_nm", x="online_tx_pct", orientation="h",
                 color="online_tx_pct", color_continuous_scale=["#E85D75", "#F7B600", "#2ECC71"],
                 hover_data=["total_tx", "online_tx"])
    fig.update_layout(height=500, margin=dict(t=10,b=10), yaxis=dict(autorange="reversed"),
                      xaxis_title="% of transactions that are online", coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    st.error(t("🛒 **E-Grocery Gap:** Groceries = 26.3% of all card TX but only **0.12%** are online. E-pharmacy = **0.18%**. In mature markets, e-grocery is 10-15% of food retail. At just 5% penetration this would mean millions of new high-value online card transactions.",
                "🛒 **Luka E-Grocery:** Spozywcze = 26.3% wszystkich TX kartowych, ale tylko **0.12%** online. E-apteka = **0.18%**. Na dojrzalych rynkach e-grocery to 10-15% handlu spozywczego. Przy zaledwie 5% penetracji to miliony nowych wysokowartościowych transakcji kartowych online."))


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
        st.subheader(t("E-Commerce Payment Trends 2022–2024", "Trendy Platnosci E-Commerce 2022–2024"))
        years = ["2022", "2023", "2024"]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=years, y=[55, 62, 67], name="BLIK", marker_color=BLIK_PINK))
        fig.add_trace(go.Bar(x=years, y=[20, 18, 16], name="Card (Visa/MC)", marker_color=VISA_BLUE))
        fig.add_trace(go.Bar(x=years, y=[15, 12, 10], name="Bank Transfer", marker_color=ACCENT[0], opacity=0.6))
        fig.add_trace(go.Bar(x=years, y=[8, 6, 5], name="Cash on Delivery", marker_color=ACCENT[3], opacity=0.6))
        fig.update_layout(barmode="stack", height=400, yaxis_title="% of e-commerce payments",
                          legend=dict(orientation="h", y=-0.15), margin=dict(t=10,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("BLIK Growth vs Card Decline", "Wzrost BLIK vs Spadek Kart"))
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        yrs = ["2019","2020","2021","2022","2023","2024"]
        fig.add_trace(go.Scatter(x=yrs, y=[0.5,0.9,1.5,2.1,2.9,4.2], name="BLIK tx (billions)",
                                 line=dict(color=BLIK_PINK, width=4), fill="tozeroy", fillcolor="rgba(212,14,106,0.1)"), secondary_y=False)
        fig.add_trace(go.Scatter(x=yrs, y=[25,23,22,20,18,16], name="Card e-com share (%)",
                                 line=dict(color=VISA_BLUE, width=3, dash="dash")), secondary_y=True)
        fig.update_yaxes(title_text="BLIK transactions (B)", secondary_y=False)
        fig.update_yaxes(title_text="Card e-com share (%)", secondary_y=True)
        fig.update_layout(height=400, margin=dict(t=10,b=40), legend=dict(orientation="h",y=-0.15))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader(t("BLIK vs Visa — Strategic Comparison", "BLIK vs Visa — Porownanie Strategiczne"))

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
    st.dataframe(comparison, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader(t("Where Visa Wins Despite BLIK Dominance", "Gdzie Visa Wygrywa Pomimo Dominacji BLIK"))
    col1, col2 = st.columns(2)
    with col1:
        st.success("""
        **🔵 Visa Strongholds (BLIK can't easily displace):**
        - **International subscriptions:** Apple (240K cards), Netflix (282K), Spotify (36K), Disney+ (42K), ChatGPT (26K)
        - **Cross-border shopping:** AliExpress, Temu, Shein, Amazon — BLIK doesn't work
        - **In-app purchases:** Google Play, App Store — card-on-file by default
        - **Travel:** Hotels, airlines, car rental — global card acceptance
        - **B2B / Corporate:** Business cards for SaaS, advertising, cloud services
        """)
    with col2:
        st.error("""
        **🟣 BLIK Strongholds (hard for Visa to compete):**
        - **Domestic e-commerce:** Allegro, OLX, local shops — one-click BLIK
        - **P2P payments:** Splitting bills, marketplace transactions
        - **Quick mobile payments:** 6-digit code, no card number needed
        - **Bill payments:** Telecom top-ups, utility payments
        - **Trust factor:** Integrated in banking apps, feels "safer" than card number entry
        """)

    st.warning(t("⚠️ **Projection:** At current trajectory (-2pp/year for cards), card share in Polish e-commerce could fall **below 10% by 2027**. Visa's strategy must focus on defending subscriptions, winning international shopping, and making card payment as frictionless as BLIK (Click to Pay, tokenization).",
                  "⚠️ **Prognoza:** Przy obecnej trajektorii (-2pp/rok dla kart), udzial kart w polskim e-commerce moze spasc **ponizej 10% do 2027**. Strategia Visa musi skupic sie na obronie subskrypcji, wygrywaniu zakupow miedzynarodowych i uczynieniu platnosci karta tak bezproblemowa jak BLIK (Click to Pay, tokenizacja)."))


# ══════════════════════════════════════════════════════════════════════════
# PAGE: CARD-FREE ZONES
# ══════════════════════════════════════════════════════════════════════════
elif current_page == "cardfree":
    st.header(t("Card-Free Zones: Where Cards Are Not Used", "Strefy bez Kart: Gdzie Karty Nie Są Używane"))
    st.caption(t("Cross-referencing GUS household spending structure with Visa transaction data",
                  "Analiza krzyzowa struktury wydatkow gospodarstw domowych GUS z danymi transakcyjnymi Visa"))

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
    df_gap = pd.DataFrame(gap_data)
    st.dataframe(df_gap, use_container_width=True, hide_index=True)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Gap Index by Category", "Indeks Luki wg Kategorii"))
        df_gap_sorted = df_gap.sort_values("Gap Index")
        colors = df_gap_sorted["Gap Index"].apply(lambda x: "#E85D75" if x <= 10 else ("#F39C12" if x < 70 else ("#4A90D9" if x <= 100 else "#2ECC71")))
        fig = go.Figure(go.Bar(y=df_gap_sorted["Category"], x=df_gap_sorted["Gap Index"], orientation="h",
                                marker_color=colors.tolist()))
        fig.add_vline(x=100, line_dash="dash", line_color=VISA_GOLD, annotation_text="100 = proportional")
        fig.update_layout(height=500, margin=dict(t=10,b=10), xaxis_title="Gap Index (100 = expected share)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("GUS Spending vs Visa Card Value", "Wydatki GUS vs Wartosc Kart Visa"))
        fig = go.Figure()
        fig.add_trace(go.Bar(name="GUS Spending %", y=df_gap["Category"], x=df_gap["GUS %"], orientation="h", marker_color=VISA_BLUE, opacity=0.6))
        fig.add_trace(go.Bar(name="Visa Value %", y=df_gap["Category"], x=df_gap["Visa Value %"], orientation="h", marker_color=ACCENT[1]))
        fig.update_layout(height=500, margin=dict(t=10,b=10), barmode="group", xaxis_title="% share",
                          legend=dict(orientation="h",y=-0.1))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader(t("The 3 Biggest Card-Free Zones Explained", "3 Najwieksze Strefy bez Kart"))

    tab1, tab2, tab3 = st.tabs([t("🏠 Housing & Utilities (20.6%)", "🏠 Mieszkanie i Media (20.6%)"),
                                 t("📱 Communications (4.0%)", "📱 Komunikacja (4.0%)"),
                                 t("🏥 Healthcare (5.5%)", "🏥 Opieka Zdrowotna (5.5%)")])

    with tab1:
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

    with tab2:
        st.markdown("""
        **4.0% of spending, ~0% on cards (Gap Index: ~1)**

        | Item | Payment Method | Card Opportunity |
        |---|---|---|
        | Mobile phone bill | Direct debit / BLIK | Card-on-file subscription |
        | Home internet | Direct debit | Card-on-file subscription |
        | Prepaid top-up | BLIK / transfer | In-app card payment |

        **Structural barrier:** Telcos set up direct debit at contract signing. Card-on-file requires active user choice.
        """)

    with tab3:
        st.markdown(f"""
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
        st.subheader(t("Top Subscription Services (by unique cardholders)", "Top Uslugi Subskrypcyjne (wg unikalnych posiadaczy kart)"))
        fig = go.Figure()
        fig.add_trace(go.Bar(y=df_s["mrch_nm_raw"][:20], x=df_s["unique_cards"][:20]/1e3, orientation="h",
                             name="Unique cards (K)", marker_color=VISA_BLUE))
        fig.update_layout(height=600, margin=dict(t=10,b=10,l=10), yaxis=dict(autorange="reversed"),
                          xaxis_title="Unique cards (thousands)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("Transaction Frequency (TX per card)", "Czestotliwosc Transakcji (TX na karte)"))
        fig = go.Figure()
        fig.add_trace(go.Bar(y=df_s["mrch_nm_raw"][:20], x=df_s["tx_per_card"][:20], orientation="h",
                             name="TX per card", marker_color=VISA_GOLD))
        fig.update_layout(height=600, margin=dict(t=10,b=10,l=10), yaxis=dict(autorange="reversed"),
                          xaxis_title="Transactions per card (18-month period)")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader(t("Recurring vs One-Time: Value Distribution", "Cykliczne vs Jednorazowe: Rozklad Wartosci"))
    recur = precise["recurring_vs_onetime"]
    df_r = pd.DataFrame(recur)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(df_r, names="frequency", values="total_transactions",
                     color_discrete_sequence=ACCENT, hole=0.35, title="Share of total transactions")
        fig.update_layout(height=350, margin=dict(t=40,b=30))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(df_r, names="frequency", values="total_amount",
                     color_discrete_sequence=ACCENT, hole=0.35, title="Share of total value")
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

    To stali klienci spozywczy, uslugi subskrypcyjne i ulubieni merchanci.
    **Ochrona i rozwijanie tych cyklicznych relacji to priorytet strategiczny nr 1 Visa.**
    """))

    st.divider()
    st.subheader(t("Subscription Categories Breakdown", "Podzial Kategorii Subskrypcyjnych"))

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
    c3.metric(t("Cash at POS", "Gotowka w POS"), "35%", "-2pp YoY")
    c4.metric(t("ATM avg withdrawal", "Średnia wypłata ATM"), "1,521", t("8.3× avg card TX", "8.3× średnia TX kartowa"))

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Sectors with Lowest Terminal Coverage", "Sektory z Najnizsza Pokryciem Terminali"))
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
        df_sec = pd.DataFrame(sectors)
        colors = df_sec["Terminal %"].apply(lambda x: "#E85D75" if x < 30 else ("#F39C12" if x < 50 else "#4A90D9"))
        fig = go.Figure(go.Bar(y=df_sec["Sector"], x=df_sec["Terminal %"], orientation="h",
                                marker_color=colors.tolist()))
        fig.update_layout(height=500, margin=dict(t=10,b=10), xaxis_title="% with POS terminal", xaxis_range=[0,100])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("Cash Usage by Transaction Size", "Uzycie Gotowki wg Wielkosci Transakcji"))
        sizes = ["Under 10 PLN", "10-50 PLN", "50-100 PLN", "100-500 PLN", "Over 500 PLN"]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Cash", x=sizes, y=[65,40,30,25,20], marker_color=ACCENT[1]))
        fig.add_trace(go.Bar(name="Card", x=sizes, y=[30,50,55,55,50], marker_color=VISA_BLUE))
        fig.add_trace(go.Bar(name="BLIK", x=sizes, y=[5,10,15,20,15], marker_color=BLIK_PINK))
        fig.add_trace(go.Bar(name="Transfer", x=sizes, y=[0,0,0,0,15], marker_color=ACCENT[4], opacity=0.5))
        fig.update_layout(barmode="stack", height=500, yaxis_title="% of payments", yaxis_range=[0,100],
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=10,b=40))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader(t("Transaction Size Distribution in Visa Data", "Rozkład Wielkości Transakcji w Danych Visa"))
    small = precise["small_transactions"]
    df_sm = pd.DataFrame(small)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=df_sm["bucket"], y=df_sm["tx_count"]/1e6, name="Transactions (M)", marker_color=VISA_BLUE, opacity=0.7), secondary_y=False)
    fig.add_trace(go.Scatter(x=df_sm["bucket"], y=df_sm["total_amount"]/1e9, name="Value (B)", line=dict(color=VISA_GOLD, width=3)), secondary_y=True)
    fig.update_yaxes(title_text="Transactions (M)", secondary_y=False)
    fig.update_yaxes(title_text="Value (B)", secondary_y=True)
    fig.update_layout(height=400, margin=dict(t=10,b=30), legend=dict(orientation="h",y=-0.15))
    st.plotly_chart(fig, use_container_width=True)

    st.info(t("""
    💡 **Micro-payments:** 19.3M transactions are under 5 units (avg 2.86). These exist because contactless payments
    removed the friction of small amounts. But per NBP data, 65% of sub-10 PLN transactions in Poland are still cash.
    **Opportunity:** "Tap for everything" campaigns + zero-fee micro-transactions for merchants.
    """, """
    💡 **Mikroplatnosci:** 19.3M transakcji jest ponizej 5 jednostek (srednia 2.86). Istnieja, bo platnosci zblizeniowe
    usunely tarcie malych kwot. Ale wg danych NBP, 65% transakcji ponizej 10 PLN w Polsce to nadal gotowka.
    **Szansa:** Kampanie "Przykładaj za wszystko" + zerowe oplaty za mikroplatnosci dla merchantow.
    """))

    st.divider()
    st.subheader(t("The ATM Cash Flow", "Przeplyw Gotowki ATM"))
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
            <p style="color:#555; font-size:0.95em; margin-top:4px;">Nowy paradygmat płatności: zamiast wpisywać dane karty, skanujesz kod QR na fizycznej karcie. Zadanie platnosci pojawia sie na Twoim telefonie. Zatwierdzasz lub odrzucasz — to wszystko.</p>
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
        **🤝 Platnosci P2P: Karty Nie Istnieja**

        Dzielenie rachunku za kolacje, platnosc za przedmiot z marketplace, zbiorka na prezent —
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

        *A gdybys nigdy wiecej nie musial wpisywac numeru karty?*
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
    > Skanowanie tego kodu QR nie ujawnia numeru karty. Tworzy **bezpieczny kanal zadania platnosci**
    > miedzy placacy a posiadaczem karty.
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
                <h2 style="color: #1A1F71; margin:0;">Tryb 1: Zadanie Platnosci P2P</h2>
                <p style="color: #333; margin-top:8px; font-size:1.05em;">Ktos jest Ci winien pieniadze? Skanuje kod QR Twojej karty i wysyla Ci platnosc — natychmiast, karta.</p>
            </div>
            """, unsafe_allow_html=True)

        st.subheader(t("How It Works", "Jak To Działa"))

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">📱</div>
                <h4 style="color:#1A1F71;">Step 1: Scan</h4>
                <p style="font-size:0.9em; color:#666;">Your friend scans the QR code on your Visa card using their phone camera</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">💲</div>
                <h4 style="color:#1A1F71;">Step 2: Enter Amount</h4>
                <p style="font-size:0.9em; color:#666;">They type the amount, add a short description (e.g. "dinner split"), and confirm</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">🔔</div>
                <h4 style="color:#1A1F71;">Step 3: You Get a Request</h4>
                <p style="font-size:0.9em; color:#666;">A push notification appears on your phone: "Adam wants to pay you 45 PLN — dinner split"</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">✅</div>
                <h4 style="color:#1A1F71;">Step 4: Approve or Decline</h4>
                <p style="font-size:0.9em; color:#666;">You review the request and tap Approve. The money moves via Visa Direct — instantly to your card.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        st.subheader(t("Use Cases", "Przypadki Użycia"))
        uc1, uc2, uc3, uc4 = st.columns(4)
        with uc1:
            st.info(t("**🍕 Split the bill**\n\nScan the card of whoever paid, enter your share. No IBAN, no phone number needed.",
                       "**🍕 Podziel rachunek**\n\nZeskanuj karte osoby, ktora placila, wpisz swoja czesc. Bez IBAN, bez numeru telefonu."))
        with uc2:
            st.info(t("**🏪 Marketplace sale**\n\nSelling on OLX? Buyer scans your card QR at meetup. Instant card-to-card payment.",
                       "**🏪 Sprzedaz na marketplace**\n\nSprzedajesz na OLX? Kupujacy skanuje Twoj QR przy spotkaniu. Natychmiastowa platnosc karta-do-karty."))
        with uc3:
            st.info(t("**🎁 Group collection**\n\nOrganizing a gift? Share your card QR in the group chat. Everyone scans & pays.",
                       "**🎁 Zbiorka grupowa**\n\nOrganizujesz prezent? Udostepnij QR karty na czacie grupowym. Kazdy skanuje i placi."))
        with uc4:
            st.info(t("**🔧 Pay the plumber**\n\nNo terminal needed. The tradesman shows their card, you scan and pay. Done.",
                       "**🔧 Zaplac hydraulikowi**\n\nBez terminala. Fachowiec pokazuje swoja karte, skanujesz i placisz. Gotowe."))

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
        - **Model Pull → Push** — *odbiorca* nie sciaga pieniedzy; *nadawca* wysyla zadanie, ktore musi byc zatwierdzone
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
                <p style="color: #333; margin-top:8px; font-size:1.05em;">Zamiast wpisywac numer karty przy kasie, zeskanuj QR swojej karty telefonem lub kamerka laptopa. Zadanie platnosci pojawia sie na telefonie — zatwierdz i gotowe.</p>
            </div>
            """, unsafe_allow_html=True)

        st.subheader(t("How It Works", "Jak To Działa"))

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">🛒</div>
                <h4 style="color:#1A1F71;">Step 1: Checkout</h4>
                <p style="font-size:0.9em; color:#666;">At any online store, choose "Visa QR Pay" as your payment method</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">📷</div>
                <h4 style="color:#1A1F71;">Step 2: Scan Your Card</h4>
                <p style="font-size:0.9em; color:#666;">Hold your Visa card's QR code up to your phone camera or laptop webcam</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">🔔</div>
                <h4 style="color:#1A1F71;">Step 3: Approve on Phone</h4>
                <p style="font-size:0.9em; color:#666;">A push notification: "Allegro — 289 PLN — headphones". You verify and approve with biometrics.</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">🎉</div>
                <h4 style="color:#1A1F71;">Step 4: Done</h4>
                <p style="font-size:0.9em; color:#666;">Payment confirmed. No card number typed. No 3DS redirect. Faster than BLIK.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        st.subheader(t("Why This Beats Current Methods", "Dlaczego To Bije Obecne Metody"))

        comp = pd.DataFrame([
            {"Step": "Select payment method", "Traditional Card": "Choose 'card'", "BLIK": "Choose 'BLIK'", "Visa QR Pay": "Choose 'Visa QR Pay'"},
            {"Step": "Identify yourself", "Traditional Card": "Type 16-digit card number + expiry + CVV", "BLIK": "Open bank app, copy 6-digit code", "Visa QR Pay": "Scan QR on your card (1 second)"},
            {"Step": "Authenticate", "Traditional Card": "3D Secure redirect → bank app → confirm", "BLIK": "Confirm in bank app", "Visa QR Pay": "Approve push notification (biometric)"},
            {"Step": "Total steps", "Traditional Card": "5-7 steps, 30-60 seconds", "BLIK": "3-4 steps, 15-20 seconds", "Visa QR Pay": "2-3 steps, 5-10 seconds"},
            {"Step": "Card number exposed?", "Traditional Card": "Yes — typed into website", "BLIK": "No (different system)", "Visa QR Pay": "No — only tokenized ID transmitted"},
            {"Step": "Works internationally?", "Traditional Card": "Yes", "BLIK": "No (Poland only)", "Visa QR Pay": "Yes (any Visa-accepting merchant)"},
            {"Step": "Works on laptop without phone?", "Traditional Card": "Yes (but must type number)", "BLIK": "No (requires phone app)", "Visa QR Pay": "Yes (laptop webcam scans QR)"},
        ])
        st.dataframe(comp, use_container_width=True, hide_index=True)

        st.success(t("""
        **The key advantage over BLIK:** Visa QR Pay is **faster** (scan vs. type 6-digit code), **more secure**
        (no card data shared, tokenized), **global** (works on any Visa-accepting website worldwide), and uses
        **biometric approval** (Face ID / fingerprint) instead of manually confirming in the bank app.
        """, """
        **Kluczowa przewaga nad BLIK:** Visa QR Pay jest **szybszy** (skan vs. wpisywanie 6-cyfrowego kodu), **bezpieczniejszy**
        (brak udostepniania danych karty, tokenizacja), **globalny** (dziala na kazdej stronie akceptujacej Visa na swiecie) i korzysta z
        **zatwierdzenia biometrycznego** (Face ID / odcisk palca) zamiast recznego potwierdzania w aplikacji bankowej.
        """))

    st.divider()

    # ── DATA-BACKED OPPORTUNITY ──
    st.header(t("Data-Backed: Why This Solution Addresses Real Gaps", "Dane Potwierdzaja: Dlaczego To Rozwiazanie Adresuje Realne Luki"))

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Gaps Addressed by Visa QR Pay", "Luki Adresowane przez Visa QR Pay"))
        gaps = pd.DataFrame([
            {"Gap": "P2P payments (cards = 2%)", "Current Winner": "BLIK (55%)", "QR Pay Impact": "Direct competitor — scan card to send money", "TAM": "~280B PLN/year"},
            {"Gap": "E-commerce checkout friction", "Current Winner": "BLIK (67%)", "QR Pay Impact": "Faster than BLIK: scan vs type code", "TAM": "~65B PLN/year"},
            {"Gap": "Cash services (plumber, tutor)", "Current Winner": "Cash (90%+)", "QR Pay Impact": "No terminal needed — just show your card", "TAM": "~50B PLN/year"},
            {"Gap": "Marketplace payments (OLX)", "Current Winner": "BLIK/Transfer", "QR Pay Impact": "Instant card-to-card at meetup", "TAM": "~15B PLN/year"},
            {"Gap": "Group collections", "Current Winner": "BLIK/Transfer", "QR Pay Impact": "Share QR in chat, everyone scans & pays", "TAM": "~5B PLN/year"},
            {"Gap": "International online shopping", "Current Winner": "Card (but friction)", "QR Pay Impact": "Scan & approve — no number entry on foreign sites", "TAM": "~20B PLN/year"},
        ])
        st.dataframe(gaps, use_container_width=True, hide_index=True)

    with col2:
        st.subheader(t("Total Addressable Market", "Calkowity Rynek Docelowy"))
        fig = go.Figure(go.Funnel(
            y=["P2P Payments", "Domestic E-Commerce", "Cash Services", "International E-Com", "Marketplace P2P", "Group Collections"],
            x=[280, 65, 50, 20, 15, 5],
            textinfo="value+text",
            text=["280B PLN", "65B PLN", "50B PLN", "20B PLN", "15B PLN", "5B PLN"],
            marker=dict(color=[VISA_BLUE, ACCENT[0], ACCENT[1], ACCENT[3], ACCENT[4], ACCENT[5]]),
        ))
        fig.update_layout(height=400, margin=dict(t=10,b=10), title_text="Estimated Annual Volume (PLN)")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── TECHNICAL ARCHITECTURE ──
    st.header(t("Technical Concept", "Koncepcja Techniczna"))

    col1, col2 = st.columns(2)
    with col1:
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

    with col2:
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

    st.divider()

    # ── COMPETITIVE ADVANTAGE ──
    st.header(t("Competitive Advantage vs BLIK", "Przewaga Konkurencyjna vs BLIK"))

    col1, col2 = st.columns(2)
    with col1:
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

    with col2:
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

    st.divider()

    # ── ROLLOUT PLAN ──
    st.header(t("Proposed Rollout", "Proponowany Plan Wdrozenia"))

    phases = pd.DataFrame([
        {"Phase": "Phase 1 (0-3 months)", "Action": "Pilot with 2-3 Polish banks — QR in mobile banking app", "Target": "P2P payments between bank customers", "KPI": "10K active QR payers"},
        {"Phase": "Phase 2 (3-6 months)", "Action": "QR stickers sent to all Visa cardholders by mail", "Target": "P2P + marketplace (OLX, Vinted)", "KPI": "100K active QR payers"},
        {"Phase": "Phase 3 (6-12 months)", "Action": "Merchant SDK — 'Visa QR Pay' button at checkout", "Target": "Top 50 Polish e-commerce sites", "KPI": "1M online QR transactions/month"},
        {"Phase": "Phase 4 (12-18 months)", "Action": "QR printed on all new Visa cards in Poland", "Target": "Full market — P2P, e-com, services", "KPI": "5% of e-commerce share (from ~9%)"},
        {"Phase": "Phase 5 (18-24 months)", "Action": "International rollout — EU, then global", "Target": "Cross-border P2P & e-commerce", "KPI": "Pan-European Visa QR standard"},
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
        st.metric(t("Cash services converted", "Konwersja uslug gotowkowych"), "5-10%", help=t("Of ~50B PLN cash service economy", "Z ~50B PLN gospodarki uslug gotowkowych"))
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
            bezpieczenstwo i ochrone kupujacego, ktorych BLIK nie moze zapewnic.</p>
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

    with col2:
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

    st.divider()

    st.subheader(t("Synergy: QR Pay + Marketplace Shield", "Synergia: QR Pay + Marketplace Shield"))

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


# ══════════════════════════════════════════════════════════════════════════
# PAGE: PREDICTIVE MODELS & SIMULATIONS
# ══════════════════════════════════════════════════════════════════════════
elif current_page == "models":
    models = load_json("model_results.json")
    st.header(t("Predictive Models & Simulations", "Modele Predykcyjne i Symulacje"))
    st.caption(t("6 models projecting Visa QR Pay adoption, transaction volume, BLIK cannibalization, ROI, and market share impact over 36 months",
                  "6 modeli prognozujacych adopcje Visa QR Pay, wolumen transakcji, kanibalizacje BLIK, ROI i wplyw na udzial rynkowy w ciagu 36 miesiecy"))

    scenario = st.radio(t("Select scenario:", "Wybierz scenariusz:"), ["Conservative", "Base", "Optimistic"], index=1, horizontal=True)

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
        fig.update_layout(height=400, yaxis_title="Cumulative adopters (millions)", title_text="QR Pay Adoption Curve",
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        for name in ["Conservative", "Base", "Optimistic"]:
            ad = models["adoption"][name]
            fig.add_trace(go.Bar(x=months_labels, y=np.array(ad["monthly_new"])/1e3,
                                 name=name, marker_color=colors_sc[name],
                                 visible=True if name==scenario else "legendonly"))
        fig.update_layout(height=400, yaxis_title="New adopters per month (K)", title_text="Monthly New Adopters",
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
                                 name="Services", fill="tonexty", line=dict(color=ACCENT[2]), stackgroup="one"))
        fig.update_layout(height=400, yaxis_title="Monthly TX (millions)", title_text=f"Monthly Transactions — {scenario}",
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["p2p_val_monthly"])/1e9,
                                 name="P2P", fill="tonexty", line=dict(color=ACCENT[0]), stackgroup="one"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["ecom_val_monthly"])/1e9,
                                 name="E-Commerce", fill="tonexty", line=dict(color=ACCENT[3]), stackgroup="one"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["svc_val_monthly"])/1e9,
                                 name="Services", fill="tonexty", line=dict(color=ACCENT[2]), stackgroup="one"))
        fig.update_layout(height=400, yaxis_title="Monthly value (B PLN)", title_text=f"Monthly Transaction Value — {scenario}",
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
                                 name="Net new to Visa (from cash/transfer)", fill="tozeroy",
                                 line=dict(color=ACCENT[2]), fillcolor="rgba(46,204,113,0.3)"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(cn["from_blik_monthly"])/1e6,
                                 name="Cannibalized from BLIK", fill="tozeroy",
                                 line=dict(color=BLIK_PINK), fillcolor="rgba(212,14,106,0.2)"))
        fig.update_layout(height=400, yaxis_title="Monthly value (M PLN)", title_text=f"Source of QR Pay Volume — {scenario}",
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Pie at month 36
        net_new_36 = cn["net_new_monthly"][35]
        blik_36 = cn["from_blik_monthly"][35]
        existing_36 = cn["from_existing_card"][35]
        fig = px.pie(names=["Net new (cash/transfer → card)", "From BLIK", "From existing card"],
                     values=[net_new_36, blik_36, existing_36],
                     color_discrete_sequence=[ACCENT[2], BLIK_PINK, ACCENT[0]], hole=0.35,
                     title=f"Volume Source at Month 36 — {scenario}")
        fig.update_layout(height=400, margin=dict(t=40,b=30))
        st.plotly_chart(fig, use_container_width=True)

    net_new_pct = cn["net_new_pct"][35]
    st.info(f"**{scenario} scenario at Month 36:** {net_new_pct:.0f}% of QR Pay volume is NET NEW to the card ecosystem (from cash/transfers). {100-net_new_pct:.0f}% is cannibalized from BLIK or existing card channels.")

    st.divider()

    # ── MODEL 4: REVENUE & ROI ──
    st.subheader(t("Model 4: Revenue & ROI Projection", "Model 4: Prognoza Przychodu i ROI"))

    rv = models["revenue"][scenario]
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["cumulative_revenue"])/1e6,
                                 name="Cumulative Revenue", line=dict(color=ACCENT[2], width=3), fill="tozeroy", fillcolor="rgba(46,204,113,0.15)"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["cumulative_costs"])/1e6,
                                 name="Cumulative Costs", line=dict(color=ACCENT[1], width=3, dash="dash")))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["cumulative_profit"])/1e6,
                                 name="Cumulative Profit", line=dict(color=VISA_BLUE, width=3)))
        if rv["breakeven_month"]:
            fig.add_vline(x=rv["breakeven_month"]-1, line_dash="dot", line_color=VISA_GOLD,
                          annotation_text=f"Break-even: M{rv['breakeven_month']}")
        fig.update_layout(height=400, yaxis_title="PLN (millions)", title_text=f"Cumulative P&L — {scenario}",
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["p2p_rev"])/1e6,
                                 name="P2P revenue", fill="tonexty", stackgroup="one", line=dict(color=ACCENT[0])))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["ecom_rev"])/1e6,
                                 name="E-commerce revenue", fill="tonexty", stackgroup="one", line=dict(color=ACCENT[3])))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["svc_rev"])/1e6,
                                 name="Services revenue", fill="tonexty", stackgroup="one", line=dict(color=ACCENT[2])))
        fig.update_layout(height=400, yaxis_title="Monthly revenue (M PLN)", title_text=f"Revenue by Channel — {scenario}",
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with st.expander(t("Cost breakdown", "Rozkład kosztów")):
        st.json(models["costs"])

    st.divider()

    # ── MODEL 5: E-COMMERCE MARKET SHARE ──
    st.subheader(t("Model 5: E-Commerce Market Share Simulation", "Model 5: Symulacja Udzialu w Rynku E-Commerce"))
    st.caption(t("How QR Pay changes Visa's share of the Polish e-commerce payments market",
                  "Jak QR Pay zmienia udzial Visa w polskim rynku platnosci e-commerce"))

    es = models["ecom_share"][scenario]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months_labels, y=es["visa_share_pct"], name="Visa total (card + QR Pay)",
                             line=dict(color=VISA_BLUE, width=3)))
    fig.add_trace(go.Scatter(x=months_labels, y=es["visa_base_share"], name="Visa baseline (without QR Pay)",
                             line=dict(color=VISA_BLUE, width=1.5, dash="dot")))
    fig.add_trace(go.Scatter(x=months_labels, y=es["blik_share_pct"], name="BLIK (adjusted)",
                             line=dict(color=BLIK_PINK, width=3)))
    fig.add_hline(y=es["visa_base_share"][0], line_dash="dash", line_color="#ccc",
                  annotation_text=f"Current Visa e-com share: {es['visa_base_share'][0]:.1f}%")
    fig.update_layout(height=450, yaxis_title="Market share (%)", title_text=f"E-Commerce Payment Share — {scenario}",
                      legend=dict(orientation="h",y=-0.12), margin=dict(t=40,b=40))
    st.plotly_chart(fig, use_container_width=True)

    visa_start = es["visa_share_pct"][0]
    visa_end = es["visa_share_pct"][35]
    blik_start = es["blik_share_pct"][0]
    blik_end = es["blik_share_pct"][35]
    st.success(f"**{scenario}:** Visa e-commerce share moves from **{visa_start:.1f}%** to **{visa_end:.1f}%** (+{visa_end-visa_start:.1f}pp). BLIK declines from **{blik_start:.1f}%** to **{blik_end:.1f}%** ({blik_end-blik_start:+.1f}pp).")

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
    fig.add_hline(y=base_rev, line_dash="dash", line_color=VISA_GOLD, annotation_text=f"Base: {base_rev:.0f}M PLN")
    fig.update_layout(height=400, yaxis_title="3-year revenue (M PLN)",
                      xaxis_title=f"{param_choice} (multiplier vs base)",
                      title_text=f"Sensitivity: {param_choice}", margin=dict(t=40,b=40))
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
    fig.add_trace(go.Bar(y=df_torn["Parameter"], x=df_torn["Low (50%)"], name="50% of base",
                         orientation="h", marker_color=ACCENT[1]))
    fig.add_trace(go.Bar(y=df_torn["Parameter"], x=df_torn["High (150%)"], name="150% of base",
                         orientation="h", marker_color=ACCENT[2]))
    fig.update_layout(height=400, xaxis_title="Impact on 3Y revenue (M PLN vs base)",
                      barmode="overlay", title_text="Tornado: Which Parameters Matter Most",
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
            ale co zrobic, by karta byla ich najwygodniejszym wyborem — online i w platnosci prywatnych.</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader(t("For Three Target Audiences", "Dla Trzech Grup Docelowych"))

    tab1, tab2, tab3 = st.tabs([t("🛍️ Online Merchants", "🛍️ Dla Sklepów Internetowych"),
                                 t("🏦 Banks & Visa", "🏦 Dla Banków i Visa"),
                                 t("🏙️ Cities & Municipalities", "🏙️ Dla Miast i Samorządów")])

    with tab1:
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

    with tab2:
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

    with tab3:
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

    st.divider()
    st.subheader(t("Priority Matrix", "Macierz Priorytetów"))

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
            handel miedzynarodowy, subskrypcje, zakupy o wysokiej wartości z ochrona kupujacego, P2P przez Visa Direct
            i niewykorzystany rynek rachunkow cyklicznych. Lacznie to <strong style="color:#1A1F71;">dziesiatki miliardow PLN rocznego wolumenu platnosci</strong>
            plynacych obecnie przez kanaly nie-kartowe.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.divider()
st.caption(t("CardFlow — Visa DataSprint Hackathon 2026 | Data: Visa synthetic transactions (305.5M), GUS (2024), NBP (2024), Gemius (2024)",
              "CardFlow — Visa DataSprint Hackathon 2026 | Dane: Syntetyczne transakcje Visa (305.5M), GUS (2024), NBP (2024), Gemius (2024)"))
