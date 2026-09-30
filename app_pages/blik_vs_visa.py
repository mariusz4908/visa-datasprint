"""Page: The problem. BLIK vs cards in Polish e-commerce, plus why each payment moved online is worth more."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from app_pages.common import source, t, ecommerce, VISA_BLUE, BLIK_PINK, ACCENT


def render():
    lang = st.session_state.get("lang", "EN")

    st.header(t("The Problem: Cards Lose the Online Checkout", "Problem: karty przegrywają płatność online"))

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
        st.subheader(t("Why It Matters: Online Baskets Are Bigger", "Dlaczego to ważne: koszyk online jest większy"))
        overall = ecommerce["ecommerce_overall"]
        phys = [r for r in overall if r["cp_flag"] == 1][0]
        onl = [r for r in overall if r["cp_flag"] == 0][0]
        # Categories that pass the 3/75 rule (cosmetics does not, so it is left out)
        cats = pd.DataFrame([
            {"cat": t("Family clothing", "Odzież"), "physical": 179, "online": 646},
            {"cat": t("Pharmacy", "Apteka"), "physical": 143, "online": 479},
            {"cat": t("Grocery", "Spożywcze"), "physical": 131, "online": 402},
            {"cat": t("Service stations", "Stacje paliw"), "physical": 216, "online": 344},
            {"cat": t("Restaurants", "Restauracje"), "physical": 121, "online": 152},
        ])
        fig = go.Figure()
        fig.add_trace(go.Bar(name=t("In store", "W sklepie"), y=cats["cat"], x=cats["physical"], orientation="h", marker_color=VISA_BLUE, opacity=0.7))
        fig.add_trace(go.Bar(name="Online", y=cats["cat"], x=cats["online"], orientation="h", marker_color=ACCENT[1]))
        fig.update_layout(height=400, margin=dict(t=10,b=40), barmode="group", yaxis=dict(autorange="reversed"),
                          xaxis_title=t("Average transaction value", "Średnia wartość transakcji"), legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig, use_container_width=True)
        source("visa")

    st.info(t(f"An online card payment averages **{onl['avg_amount']:.0f}** vs **{phys['avg_amount']:.0f}** in store "
              f"({onl['avg_amount']/phys['avg_amount']:.1f}×). Every checkout Visa wins back from BLIK is worth about twice a shop payment.",
              f"Płatność kartą online to średnio **{onl['avg_amount']:.0f}**, a w sklepie **{phys['avg_amount']:.0f}** "
              f"({onl['avg_amount']/phys['avg_amount']:.1f}×). Każda płatność odzyskana od BLIK jest warta mniej więcej dwie płatności w sklepie."))

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
    source("gemius", "nbp_survey", "estimate")

    st.divider()

    st.subheader(t("Where Visa Wins Despite BLIK Dominance", "Gdzie Visa wygrywa mimo dominacji BLIK"))
    col1, col2 = st.columns(2)
    with col1:
        st.success(t("""
        **Visa strongholds (BLIK can't easily displace):**
        - **Habits:** once a card is saved at a shop, it stays. **4.1% of card–merchant pairs make 42.8% of card payments** (36.5% of value)
        - **Subscriptions and in-app purchases:** card-on-file by default
        - **Cross-border shopping and travel:** BLIK doesn't work abroad
        - **B2B:** business cards for SaaS, ads, cloud services
        """, """
        **Mocne strony Visa (BLIK nie wyprze ich łatwo):**
        - **Nawyk:** karta raz zapisana w sklepie zostaje. **4,1% par karta–sprzedawca daje 42,8% płatności kartą** (36,5% wartości)
        - **Subskrypcje i zakupy w aplikacjach:** karta zapisana domyślnie
        - **Zakupy za granicą i podróże:** BLIK nie działa za granicą
        - **B2B:** karty firmowe na SaaS, reklamę, usługi chmurowe
        """))
        source("visa", note=("habit = card–merchant pair with 12+ payments in 18 months",
                             "nawyk = para karta–sprzedawca z 12+ płatnościami w 18 miesięcy"))
    with col2:
        st.error(t("""
        **BLIK strongholds (hard for Visa to compete):**
        - **Domestic e-commerce:** one-click BLIK, no card number to type
        - **P2P payments:** splitting bills, marketplace deals
        - **Bill payments:** telecom top-ups, utilities
        - **Trust:** built into banking apps, feels "safer" than typing a card number
        """, """
        **Mocne strony BLIK (trudne do przejęcia przez Visa):**
        - **Krajowy e-commerce:** BLIK jednym kliknięciem, bez wpisywania numeru karty
        - **Płatności P2P:** dzielenie rachunków, transakcje z ogłoszeń
        - **Opłacanie rachunków:** doładowania, media
        - **Zaufanie:** BLIK jest wbudowany w aplikacje bankowe i wydaje się „bezpieczniejszy” niż wpisywanie numeru karty
        """))

    st.warning(t("**The takeaway:** cards don't lose on trust, they lose on convenience. Visa wins where the card is already saved. "
                 "Visa QR Pay targets the checkouts where it is not saved yet.",
                 "**Wniosek:** karty nie przegrywają zaufaniem, tylko wygodą. Visa wygrywa tam, gdzie karta jest już zapisana. "
                 "Visa QR Pay celuje w płatności, przy których karta nie jest jeszcze zapisana."))
