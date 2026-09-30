"""Page: Cash Deserts & Infrastructure."""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from app_pages.common import source, t, precise, VISA_BLUE, VISA_GOLD, BLIK_PINK, ACCENT


def render():
    lang = st.session_state.get("lang", "EN")

    st.header(t("Cash Deserts & Payment Infrastructure Gaps", "Gdzie rządzi gotówka: luki w infrastrukturze płatniczej"))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("POS Terminals", "Terminale POS"), "1.25M", "+8% YoY")
    c2.metric(t("Terminals/1000 pop", "Terminale/1000 mieszk."), "33.3", t("EU avg ~35", "Średnia UE ~35"))
    c3.metric(t("Cash at POS", "Gotówka w POS"), "35%", "-2pp YoY")
    c4.metric(t("ATM avg withdrawal", "Średnia wypłata z bankomatu"), "1,521", t("8.3× avg card TX", "8.3× średnia transakcja kartowa"))
    source("nbp", "visa", note=("ATM average withdrawal from the Visa data", "średnia wypłata z bankomatu wg danych Visa"))

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Sectors with Lowest Terminal Coverage", "Branże z najsłabszym dostępem do terminali"))
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
        source("estimate")

    with col2:
        st.subheader(t("Cash Usage by Transaction Size", "Udział gotówki wg kwoty transakcji"))
        sizes = [t("Under 10 PLN", "Poniżej 10 PLN"), "10-50 PLN", "50-100 PLN", "100-500 PLN", t("Over 500 PLN", "Powyżej 500 PLN")]
        fig = go.Figure()
        fig.add_trace(go.Bar(name=t("Cash", "Gotówka"), x=sizes, y=[65,40,30,25,20], marker_color=ACCENT[1]))
        fig.add_trace(go.Bar(name=t("Card", "Karta"), x=sizes, y=[30,50,55,55,50], marker_color=VISA_BLUE))
        fig.add_trace(go.Bar(name="BLIK", x=sizes, y=[5,10,15,20,15], marker_color=BLIK_PINK))
        fig.add_trace(go.Bar(name=t("Transfer", "Przelew"), x=sizes, y=[0,0,0,0,15], marker_color=ACCENT[4], opacity=0.5))
        fig.update_layout(barmode="stack", height=500, yaxis_title=t("% of payments", "% płatności"), yaxis_range=[0,100],
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=10,b=40))
        st.plotly_chart(fig, use_container_width=True)
        source("nbp_survey")

    st.divider()

    st.subheader(t("Transaction Size Distribution in Visa Data", "Rozkład kwot transakcji w danych Visa"))
    small = precise["small_transactions"]
    df_sm = pd.DataFrame(small)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=df_sm["bucket"], y=df_sm["tx_count"]/1e6, name=t("Transactions (M)", "Transakcje (M)"), marker_color=VISA_BLUE, opacity=0.7), secondary_y=False)
    fig.add_trace(go.Scatter(x=df_sm["bucket"], y=df_sm["total_amount"]/1e9, name=t("Value (B)", "Wartość (mld)"), line=dict(color=VISA_GOLD, width=3)), secondary_y=True)
    fig.update_yaxes(title_text=t("Transactions (M)", "Transakcje (M)"), secondary_y=False)
    fig.update_yaxes(title_text=t("Value (B)", "Wartość (mld)"), secondary_y=True)
    fig.update_layout(height=400, margin=dict(t=10,b=30), legend=dict(orientation="h",y=-0.15))
    st.plotly_chart(fig, use_container_width=True)
    source("visa")

    st.info(t("""
    **Micro-payments:** 19.3M transactions are under 5 units (avg 2.86). These exist because contactless payments
    removed the friction of small amounts. But per NBP data, 65% of sub-10 PLN transactions in Poland are still cash.
    **Opportunity:** "Tap for everything" campaigns + zero-fee micro-transactions for merchants.
    """, """
    **Mikropłatności:** 19.3M transakcji jest poniżej 5 jednostek (średnia 2.86). Istnieją, bo płatności zbliżeniowe
    usunęły tarcie małych kwot. Ale wg danych NBP, 65% transakcji poniżej 10 PLN w Polsce to nadal gotówka.
    **Szansa:** Kampanie "Przykładaj za wszystko" + zerowe opłaty za mikropłatności dla sprzedawców.
    """))

    st.divider()
    st.subheader(t("The ATM Cash Flow", "Wypłaty z bankomatów"))
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
        | Wypłaty z bankomatów w próbce Visa | 5.4M |
        | Średnia wypłata z bankomatu | **1 521** (8.3× średnia transakcja kartowa 182) |
        | Łączna wartość wypłat | 8.2 mld (14.7% całej wartości w zbiorze) |
        | Szacowane przeznaczenie gotówki | Czynsz, prywatni lekarze, targowiska, usługi, szara strefa |

        **Wysoka średnia wypłata (1 521) sugeruje celowe, ukierunkowane użycie gotówki** — ludzie wypłacają duże
        kwoty specjalnie, by płacić za rzeczy, które nie akceptują kart (lub gdzie preferują gotówkę).
        """)
    source("visa")
