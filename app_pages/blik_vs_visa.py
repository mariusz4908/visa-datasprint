"""Page: BLIK vs Visa."""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from app_pages.common import source, t, VISA_BLUE, BLIK_PINK, ACCENT


def render():
    lang = st.session_state.get("lang", "EN")

    st.header(t("BLIK vs Visa: The Battle for Polish E-Commerce", "BLIK vs Visa: walka o polski e-commerce"))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("BLIK e-com share", "Udział BLIK w e-commerce"), "67%", "+5pp vs 2023", delta_color="inverse")
    c2.metric(t("Card e-com share", "Udział kart w e-commerce"), "16%", "-2pp vs 2023", delta_color="inverse")
    c3.metric(t("BLIK tx/year", "Transakcje BLIK/rok"), "4.2B", "+45% YoY", delta_color="inverse")
    c4.metric(t("Card tx/year (total)", "Transakcje kartowe/rok (łącznie)"), "9.2B", "+8% YoY")
    source("gemius", "blik", "nbp")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("E-Commerce Payment Trends 2022–2024", "Trendy płatności w e-commerce 2022–2024"))
        years = ["2022", "2023", "2024"]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=years, y=[55, 62, 67], name="BLIK", marker_color=BLIK_PINK))
        fig.add_trace(go.Bar(x=years, y=[20, 18, 16], name=t("Card (Visa/MC)", "Karta (Visa/MC)"), marker_color=VISA_BLUE))
        fig.add_trace(go.Bar(x=years, y=[15, 12, 10], name=t("Bank Transfer", "Przelew"), marker_color=ACCENT[0], opacity=0.6))
        fig.add_trace(go.Bar(x=years, y=[8, 6, 5], name=t("Cash on Delivery", "Za pobraniem"), marker_color=ACCENT[3], opacity=0.6))
        fig.update_layout(barmode="stack", height=400, yaxis_title=t("% of e-commerce payments", "% płatności e-commerce"),
                          legend=dict(orientation="h", y=-0.15), margin=dict(t=10,b=40))
        st.plotly_chart(fig, use_container_width=True)
        source("gemius")

    with col2:
        st.subheader(t("BLIK Growth vs Card Decline", "Wzrost BLIK a spadek kart"))
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        yrs = ["2019","2020","2021","2022","2023","2024"]
        fig.add_trace(go.Scatter(x=yrs, y=[0.5,0.9,1.5,2.1,2.9,4.2], name=t("BLIK tx (billions)", "BLIK tx (mld)"),
                                 line=dict(color=BLIK_PINK, width=4), fill="tozeroy", fillcolor="rgba(212,14,106,0.1)"), secondary_y=False)
        fig.add_trace(go.Scatter(x=yrs, y=[25,23,22,20,18,16], name=t("Card e-com share (%)", "Udział kart w e-commerce (%)"),
                                 line=dict(color=VISA_BLUE, width=3, dash="dash")), secondary_y=True)
        fig.update_yaxes(title_text=t("BLIK transactions (B)", "Transakcje BLIK (mld)"), secondary_y=False)
        fig.update_yaxes(title_text=t("Card e-com share (%)", "Udział kart w e-commerce (%)"), secondary_y=True)
        fig.update_layout(height=400, margin=dict(t=10,b=40), legend=dict(orientation="h",y=-0.15))
        st.plotly_chart(fig, use_container_width=True)
        source("blik", "gemius", "estimate", note=("card share 2019–2021 estimated", "udział kart 2019–2021 szacowany"))

    st.divider()
    st.subheader(t("BLIK vs Visa — Strategic Comparison", "BLIK vs Visa — porównanie strategiczne"))

    if lang == "EN":
        comparison = pd.DataFrame([
            {"Dimension": "E-commerce share 2024", "BLIK": "67%", "Visa Card": "~9%", "Advantage": "BLIK"},
            {"Dimension": "One-click checkout", "BLIK": "BLIK OneClick", "Visa Card": "Card-on-file / tokenized", "Advantage": "Tie"},
            {"Dimension": "Recurring / subscriptions", "BLIK": "BLIK Recurring (new)", "Visa Card": "Well established (COF)", "Advantage": "Visa"},
            {"Dimension": "International e-commerce", "BLIK": "Poland only", "Visa Card": "Global acceptance", "Advantage": "Visa"},
            {"Dimension": "In-app purchases (Apple/Google)", "BLIK": "Limited support", "Visa Card": "Native integration", "Advantage": "Visa"},
            {"Dimension": "P2P transfers", "BLIK": "55% share", "Visa Card": "~2% share", "Advantage": "BLIK"},
            {"Dimension": "Physical POS", "BLIK": "5% (BLIK tap, new)", "Visa Card": "58% (contactless)", "Advantage": "Visa"},
            {"Dimension": "Cross-border travel", "BLIK": "Not available abroad", "Visa Card": "Universal", "Advantage": "Visa"},
            {"Dimension": "Chargeback / buyer protection", "BLIK": "Limited", "Visa Card": "Full Visa protection", "Advantage": "Visa"},
            {"Dimension": "User trust in Poland", "BLIK": "Very high (bank app native)", "Visa Card": "High", "Advantage": "BLIK"},
        ])
    else:
        comparison = pd.DataFrame([
            {"Wymiar": "Udział w e-commerce 2024", "BLIK": "67%", "Karta Visa": "~9%", "Przewaga": "BLIK"},
            {"Wymiar": "Płatność jednym kliknięciem", "BLIK": "BLIK OneClick", "Karta Visa": "Card-on-file / tokenizacja", "Przewaga": "Remis"},
            {"Wymiar": "Cykliczne / subskrypcje", "BLIK": "BLIK Recurring (nowość)", "Karta Visa": "Ugruntowane (COF)", "Przewaga": "Visa"},
            {"Wymiar": "Międzynarodowy e-commerce", "BLIK": "Tylko Polska", "Karta Visa": "Akceptacja globalna", "Przewaga": "Visa"},
            {"Wymiar": "Zakupy w aplikacjach (Apple/Google)", "BLIK": "Ograniczone wsparcie", "Karta Visa": "Natywna integracja", "Przewaga": "Visa"},
            {"Wymiar": "Przelewy P2P", "BLIK": "55% udziału", "Karta Visa": "~2% udziału", "Przewaga": "BLIK"},
            {"Wymiar": "Fizyczny POS", "BLIK": "5% (BLIK tap, nowość)", "Karta Visa": "58% (zbliżeniowo)", "Przewaga": "Visa"},
            {"Wymiar": "Podróże zagraniczne", "BLIK": "Niedostępne za granicą", "Karta Visa": "Uniwersalne", "Przewaga": "Visa"},
            {"Wymiar": "Chargeback / ochrona kupującego", "BLIK": "Ograniczone", "Karta Visa": "Pełna ochrona Visa", "Przewaga": "Visa"},
            {"Wymiar": "Zaufanie użytkowników w Polsce", "BLIK": "Bardzo wysokie (wbudowany w aplikację banku)", "Karta Visa": "Wysokie", "Przewaga": "BLIK"},
        ])
    st.dataframe(comparison, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader(t("Where Visa Wins Despite BLIK Dominance", "Gdzie Visa wygrywa mimo dominacji BLIK"))
    col1, col2 = st.columns(2)
    with col1:
        if lang == "EN":
            st.success("""
            **Visa Strongholds (BLIK can't easily displace):**
            - **International subscriptions:** Apple (240K cards), Netflix (282K), Spotify (36K), Disney+ (42K), ChatGPT (26K)
            - **Cross-border shopping:** AliExpress, Temu, Shein, Amazon — BLIK doesn't work
            - **In-app purchases:** Google Play, App Store — card-on-file by default
            - **Travel:** Hotels, airlines, car rental — global card acceptance
            - **B2B / Corporate:** Business cards for SaaS, advertising, cloud services
            """)
        else:
            st.success("""
            **Mocne strony Visa (BLIK nie wyprze ich łatwo):**
            - **Międzynarodowe subskrypcje:** Apple (240K kart), Netflix (282K), Spotify (36K), Disney+ (42K), ChatGPT (26K)
            - **Zakupy transgraniczne:** AliExpress, Temu, Shein, Amazon — BLIK nie działa
            - **Zakupy w aplikacjach:** Google Play, App Store — karta domyślnie zapisana
            - **Podróże:** Hotele, linie lotnicze, wynajem aut — globalna akceptacja kart
            - **B2B / firmy:** Karty firmowe na SaaS, reklamę, usługi chmurowe
            """)
    with col2:
        if lang == "EN":
            st.error("""
            **BLIK Strongholds (hard for Visa to compete):**
            - **Domestic e-commerce:** Allegro, OLX, local shops — one-click BLIK
            - **P2P payments:** Splitting bills, marketplace transactions
            - **Quick mobile payments:** 6-digit code, no card number needed
            - **Bill payments:** Telecom top-ups, utility payments
            - **Trust factor:** Integrated in banking apps, feels "safer" than card number entry
            """)
        else:
            st.error("""
            **Mocne strony BLIK (trudne do przejęcia przez Visa):**
            - **Krajowy e-commerce:** Allegro, OLX, lokalne sklepy — BLIK jednym kliknięciem
            - **Płatności P2P:** Dzielenie rachunków, transakcje marketplace
            - **Szybkie płatności mobilne:** 6-cyfrowy kod, bez numeru karty
            - **Opłacanie rachunków:** Doładowania telekomów, opłaty za media
            - **Zaufanie:** BLIK jest wbudowany w aplikacje bankowe i wydaje się „bezpieczniejszy” niż wpisywanie numeru karty
            """)

    st.warning(t("**Projection:** At current trajectory (-2pp/year for cards), card share in Polish e-commerce could fall **below 10% by 2027**. Visa's strategy must focus on defending subscriptions, winning international shopping, and making card payment as frictionless as BLIK (Click to Pay, tokenization).",
                  "**Prognoza:** Przy obecnym trendzie (-2 pp/rok dla kart), udział kart w polskim e-commerce może spaść **poniżej 10% do 2027**. Strategia Visa musi skupić się na obronie subskrypcji, wygrywaniu zakupów międzynarodowych i uproszczeniu płatności kartą do poziomu BLIK (Click to Pay, tokenizacja)."))
