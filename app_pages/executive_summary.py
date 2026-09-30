"""Page: Executive Summary."""
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app_pages.common import source, t, VISA_BLUE, BLIK_PINK, ACCENT


def render():
    lang = st.session_state.get("lang", "EN")

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
            <p style="opacity:0.9; font-size:1.1em; margin-top:4px;">Dane transakcyjne jako drogowskaz: jak przekonać Polaków do płacenia kartą w e-commerce i P2P</p>
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
        > **Karty płatnicze dominują w sklepach stacjonarnych, ale w e-commerce i płatnościach między osobami (P2P) są wypierane
        > przez inne metody.** W Polsce BLIK, szybkie przelewy i gotówka to główne alternatywy. Użytkownicy wybierają je,
        > bo są szybsze, nie wymagają wpisywania numeru karty i wydają się bezpieczniejsze. Ta sama osoba płaci kartą
        > w sklepie osiedlowym, ale online lub płacąc znajomemu — wybiera inną metodę.
        >
        > **CardFlow** wykorzystuje zanonimizowane, zagregowane dane transakcyjne, by zrozumieć *kiedy, gdzie i dlaczego*
        > karta przestaje być pierwszym wyborem. Analizujemy wzorce zachowań według kategorii sprzedawców, pory dnia,
        > wartości koszyka i lokalizacji. Identyfikujemy **"punkty ucieczki"** — momenty, w których klienci zmieniają metodę płatności.
        """)

    st.divider()

    # KPIs
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric(t("Transactions", "Transakcje"), "305.5M", help=t("Total in sample dataset", "Próbka danych"))
    c2.metric(t("Unique Cards", "Unikalne karty"), "1.95M", help=t("Unique card identifiers", "Unikalne identyfikatory kart"))
    c3.metric(t("Total Value", "Łączna wartość"), "55.7B", help=t("Fictional currency units", "Fikcyjne jednostki walutowe"))
    c4.metric(t("Avg Transaction", "Średnia transakcja"), "182.30", help=t("Average transaction value", "Średnia wartość transakcji"))
    c5.metric(t("Online Share (TX)", "Udział online (transakcje)"), "11.2%", delta="+1.4pp YoY")
    c6.metric(t("Online Share (Value)", "Udział online (wartość)"), "19.6%", help=t("Online = higher avg value", "Online = wyższa średnia wartość"))
    source("visa")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(t("The Polish Payment Landscape", "Rynek płatności w Polsce"))
        fig = go.Figure()
        years = ["2019", "2020", "2021", "2022", "2023", "2024"]
        fig.add_trace(go.Scatter(x=years, y=[44,50,53,55,57,58], name=t("Card at POS (%)", "Karta w POS (%)"), line=dict(color=VISA_BLUE, width=3)))
        fig.add_trace(go.Scatter(x=years, y=[54,47,43,40,37,35], name=t("Cash at POS (%)", "Gotówka w POS (%)"), line=dict(color=ACCENT[1], width=3, dash="dash")))
        fig.add_trace(go.Scatter(x=years, y=[5,10,15,22,30,42], name=t("BLIK tx (×100M)", "BLIK tx (×100M)"), line=dict(color=BLIK_PINK, width=3)))
        fig.update_layout(height=350, margin=dict(t=10,b=30), legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig, use_container_width=True)
        source("nbp", "blik")

    with col2:
        st.subheader(t("E-Commerce Payment Methods 2024", "Metody płatności w e-commerce 2024"))
        fig = px.pie(
            names=[t("BLIK (67%)", "BLIK (67%)"), t("Card (16%)", "Karta (16%)"), t("Bank Transfer (10%)", "Przelew (10%)"), t("Cash on Delivery (5%)", "Za pobraniem (5%)"), t("Other (2%)", "Inne (2%)")],
            values=[67, 16, 10, 5, 2],
            color_discrete_sequence=[BLIK_PINK, VISA_BLUE, ACCENT[0], ACCENT[3], "#ccc"],
            hole=0.4,
        )
        fig.update_layout(height=350, margin=dict(t=10,b=30))
        st.plotly_chart(fig, use_container_width=True)
        source("gemius")

    st.divider()
    st.subheader(t("Key Findings at a Glance", "Kluczowe wnioski"))
    f1, f2, f3 = st.columns(3)
    with f1:
        st.error(t("**BLIK Threat:** 67% of e-commerce and growing +5pp/year. Cards fell from 20% to 16% in 2 years.",
                    "**Zagrożenie BLIK:** 67% e-commerce i rośnie +5pp/rok. Karty spadły z 20% do 16% w 2 lata."))
    with f2:
        st.warning(t("**Card-Free Zones:** Housing (20.6% of spending), telecom (4.0%), education (1.1%) have <1% card penetration.",
                      "**Strefy bez kart:** mieszkanie (20.6% wydatków), telekom (4.0%) i edukacja (1.1%) mają <1% udziału kart."))
    with f3:
        st.success(t("**Visa's Moat:** Subscriptions (Apple, Netflix, Spotify) + international e-commerce = ~8M tx locked on card rails.",
                      "**Przewaga Visa:** subskrypcje (Apple, Netflix, Spotify) i zagraniczny e-commerce = ~8M transakcji kartą."))

    f4, f5, f6 = st.columns(3)
    with f4:
        st.info(t("**E-Grocery Gap:** 26% of card tx are grocery but only 0.12% online. Online avg = 3.1x higher value.",
                   "**Luka w zakupach spożywczych online:** 26% transakcji kartowych to zakupy spożywcze, ale tylko 0.12% z nich online. Średnia online = 3.1x wyższa wartość."))
    with f5:
        st.error(t("**Cash Services:** Doctors (255K tx), dentists (76K), home repair (31K) — cash dominates services.",
                    "**Usługi opłacane gotówką:** lekarze (255K tx), dentyści (76K), naprawy domowe (31K) — gotówka dominuje w usługach."))
    with f6:
        st.success(t("**Recurring Power:** 4.1% of card-merchant pairs generate 42.8% of transactions and 36.5% of value.",
                      "**Siła nawyku:** 4.1% par karta–sprzedawca generuje 42.8% transakcji i 36.5% wartości."))