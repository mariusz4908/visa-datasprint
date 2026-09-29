"""Page: Subscription Economy."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app_pages.common import t, ecommerce, precise, VISA_BLUE, VISA_GOLD, ACCENT


def render():
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

    st.subheader(t("Recurring vs One-Time: Value Distribution", "Cykliczne vs Jednorazowe: Rozkład Wartosci"))
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

    To stali klienci spożywczy, usługi subskrypcyjne i ulubieni merchanci.
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
