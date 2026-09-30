"""Page: Subscription Economy."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app_pages.common import source, t, ecommerce, precise, VISA_BLUE, VISA_GOLD, ACCENT


def render():
    lang = st.session_state.get("lang", "EN")

    st.header(t("The Subscription Economy: Visa's Competitive Moat", "Subskrypcje: trwała przewaga Visa"))

    subs = ecommerce["subscription_merchants"]
    df_s = pd.DataFrame(subs)

    c1, c2, c3 = st.columns(3)
    c1.metric(t("Subscription merchants", "Sprzedawcy subskrypcji"), f"{len(df_s)}", t("with >1K cards & 3+ TX/card", "z >1 tys. kart i 3+ transakcjami na kartę"))
    c2.metric("Top: Apple.com", "240K cards", "10.3 TX/card avg")
    c3.metric(t("Recurring pairs (12+/period)", "Stałe pary karta–sprzedawca (12+ transakcji)"), "4.1M", "= 42.8% TX")
    source("visa")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Top Subscription Services (by unique cardholders)", "Najpopularniejsze subskrypcje (wg liczby kart)"))
        fig = go.Figure()
        fig.add_trace(go.Bar(y=df_s["mrch_nm_raw"][:20], x=df_s["unique_cards"][:20]/1e3, orientation="h",
                             name=t("Unique cards (K)", "Unikalne karty (tys.)"), marker_color=VISA_BLUE))
        fig.update_layout(height=600, margin=dict(t=10,b=10,l=10), yaxis=dict(autorange="reversed"),
                          xaxis_title=t("Unique cards (thousands)", "Unikalne karty (tysiące)"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("Transaction Frequency (TX per card)", "Częstotliwość transakcji (na kartę)"))
        fig = go.Figure()
        fig.add_trace(go.Bar(y=df_s["mrch_nm_raw"][:20], x=df_s["tx_per_card"][:20], orientation="h",
                             name=t("TX per card", "TX na kartę"), marker_color=VISA_GOLD))
        fig.update_layout(height=600, margin=dict(t=10,b=10,l=10), yaxis=dict(autorange="reversed"),
                          xaxis_title=t("Transactions per card (18-month period)", "Transakcje na kartę (okres 18 miesięcy)"))
        st.plotly_chart(fig, use_container_width=True)
    source("visa")

    st.divider()

    st.subheader(t("Recurring vs One-Time: Value Distribution", "Płatności powtarzalne a jednorazowe: rozkład wartości"))
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
    source("visa")

    st.success(t("""
    **Key Insight:** Just **4.1% of card-merchant relationships** (those with 12+ transactions in 18 months) generate:
    - **42.8%** of all transactions (130.9M)
    - **36.5%** of all value (20.3B)

    These are the grocery regulars, subscription services, and habitual merchants.
    **Protecting and growing these recurring relationships is Visa's #1 strategic priority.**
    """, """
    **Kluczowy wniosek:** Zaledwie **4.1% par karta–sprzedawca** (z 12+ transakcjami w 18 miesięcy) generuje:
    - **42.8%** wszystkich transakcji (130.9M)
    - **36.5%** całej wartości (20.3B)

    To stałe zakupy spożywcze, subskrypcje i ulubieni sprzedawcy.
    **Ochrona i rozwijanie tych cyklicznych relacji to priorytet strategiczny nr 1 Visa.**
    """))

    st.divider()
    st.subheader(t("Subscription Categories Breakdown", "Podział kategorii subskrypcji"))

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
            "Transport": ["jakdojade.pl", "KOLEO bilety kolejowe", "www.bilet.intercity.pl", "Autopay Mobility"],
            "Finanse i Przelewy": ["Revolut*VISA MONEY TRANSF", "AllegroPay", "PAYSEND"],
            "Telekomunikacja": ["doladowania.play.pl", "T-MOBILE POLSKA"],
            "AI i Technologia": ["OPENAI *CHATGPT SUBSCR"],
        }

    for cat_name, merchants in sub_cats.items():
        cat_df = df_s[df_s["mrch_nm_raw"].isin(merchants)]
        if not cat_df.empty:
            total_cards = cat_df["unique_cards"].sum()
            st.markdown(f"**{cat_name}** — {total_cards/1e3:.0f}K unique cards")
