"""Page: Card-Free Zones."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from app_pages.common import source, t, VISA_BLUE, VISA_GOLD, ACCENT


def render():
    lang = st.session_state.get("lang", "EN")

    st.header(t("Card-Free Zones: Where Cards Are Not Used", "Strefy bez kart: gdzie karty nie są używane"))
    st.caption(t("Cross-referencing GUS household spending structure with Visa transaction data",
                  "Zestawienie struktury wydatków gospodarstw domowych (GUS) z danymi transakcyjnymi Visa"))

    if lang == "EN":
        gap_data = [
            {"Category": "Housing & Utilities", "GUS %": 20.6, "Visa Value %": 0.3, "Gap Index": 2, "Status": "Card-Free Zone", "Barrier": "Bank transfers, direct debit"},
            {"Category": "Communications", "GUS %": 4.0, "Visa Value %": 0.01, "Gap Index": 1, "Status": "Card-Free Zone", "Barrier": "Direct debit, BLIK"},
            {"Category": "Education", "GUS %": 1.1, "Visa Value %": 0.03, "Gap Index": 3, "Status": "Card-Free Zone", "Barrier": "Bank transfers, cash tutoring"},
            {"Category": "Alcohol & Tobacco", "GUS %": 2.5, "Visa Value %": 0.8, "Gap Index": 32, "Status": "Very Underused", "Barrier": "Cash-only kiosks"},
            {"Category": "Healthcare", "GUS %": 5.5, "Visa Value %": 2.5, "Gap Index": 46, "Status": "Underused", "Barrier": "Cash at doctors, dentists"},
            {"Category": "Home Furnishings", "GUS %": 4.4, "Visa Value %": 2.6, "Gap Index": 59, "Status": "Underused", "Barrier": "Cash for services/repairs"},
            {"Category": "Recreation & Culture", "GUS %": 6.9, "Visa Value %": 5.1, "Gap Index": 74, "Status": "Slightly Under", "Barrier": "Cash at events, cinemas"},
            {"Category": "Transport", "GUS %": 9.1, "Visa Value %": 7.6, "Gap Index": 84, "Status": "Well Covered", "Barrier": "Insurance by transfer"},
            {"Category": "Food & Groceries", "GUS %": 27.1, "Visa Value %": 25.3, "Gap Index": 93, "Status": "Well Covered", "Barrier": "Small shops, markets"},
            {"Category": "Other Goods", "GUS %": 8.7, "Visa Value %": 9.5, "Gap Index": 109, "Status": "Well Covered", "Barrier": "—"},
            {"Category": "Clothing", "GUS %": 4.4, "Visa Value %": 5.6, "Gap Index": 127, "Status": "Overrepresented", "Barrier": "—"},
            {"Category": "Restaurants & Hotels", "GUS %": 5.7, "Visa Value %": 9.6, "Gap Index": 168, "Status": "Overrepresented", "Barrier": "—"},
        ]
    else:
        gap_data = [
            {"Kategoria": "Mieszkanie i media", "GUS %": 20.6, "Wartość Visa %": 0.3, "Indeks luki": 2, "Status": "Strefa bez kart", "Bariera": "Przelewy bankowe, polecenia zapłaty"},
            {"Kategoria": "Komunikacja", "GUS %": 4.0, "Wartość Visa %": 0.01, "Indeks luki": 1, "Status": "Strefa bez kart", "Bariera": "Polecenia zapłaty, BLIK"},
            {"Kategoria": "Edukacja", "GUS %": 1.1, "Wartość Visa %": 0.03, "Indeks luki": 3, "Status": "Strefa bez kart", "Bariera": "Przelewy bankowe, korepetycje za gotówkę"},
            {"Kategoria": "Alkohol i tytoń", "GUS %": 2.5, "Wartość Visa %": 0.8, "Indeks luki": 32, "Status": "Mocno niedoużywane", "Bariera": "Kioski tylko gotówkowe"},
            {"Kategoria": "Opieka zdrowotna", "GUS %": 5.5, "Wartość Visa %": 2.5, "Indeks luki": 46, "Status": "Niedoużywane", "Bariera": "Gotówka u lekarzy, dentystów"},
            {"Kategoria": "Wyposażenie domu", "GUS %": 4.4, "Wartość Visa %": 2.6, "Indeks luki": 59, "Status": "Niedoużywane", "Bariera": "Gotówka za usługi/naprawy"},
            {"Kategoria": "Rekreacja i kultura", "GUS %": 6.9, "Wartość Visa %": 5.1, "Indeks luki": 74, "Status": "Lekko poniżej", "Bariera": "Gotówka na imprezach, w kinach"},
            {"Kategoria": "Transport", "GUS %": 9.1, "Wartość Visa %": 7.6, "Indeks luki": 84, "Status": "Dobrze pokryte", "Bariera": "Ubezpieczenie przelewem"},
            {"Kategoria": "Żywność", "GUS %": 27.1, "Wartość Visa %": 25.3, "Indeks luki": 93, "Status": "Dobrze pokryte", "Bariera": "Małe sklepy, targowiska"},
            {"Kategoria": "Pozostałe towary", "GUS %": 8.7, "Wartość Visa %": 9.5, "Indeks luki": 109, "Status": "Dobrze pokryte", "Bariera": "—"},
            {"Kategoria": "Odzież", "GUS %": 4.4, "Wartość Visa %": 5.6, "Indeks luki": 127, "Status": "Ponad normę", "Bariera": "—"},
            {"Kategoria": "Restauracje i hotele", "GUS %": 5.7, "Wartość Visa %": 9.6, "Indeks luki": 168, "Status": "Ponad normę", "Bariera": "—"},
        ]
    df_gap = pd.DataFrame(gap_data)
    st.dataframe(df_gap, use_container_width=True, hide_index=True)
    source("gus_hbs", "visa", note=("Gap Index = Visa value share ÷ GUS spending share × 100; COICOP→MCC mapping in METHODOLOGY.md",
                                   "Indeks luki = udział wartości Visa ÷ udział wydatków GUS × 100; mapowanie COICOP→MCC w METHODOLOGY.md"))

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Gap Index by Category", "Indeks luki wg kategorii"))
        _cat_col = "Category" if lang == "EN" else "Kategoria"
        _gap_col = "Gap Index" if lang == "EN" else "Indeks luki"
        df_gap_sorted = df_gap.sort_values(_gap_col)
        colors = df_gap_sorted[_gap_col].apply(lambda x: "#E85D75" if x <= 10 else ("#F39C12" if x < 70 else ("#4A90D9" if x <= 100 else "#2ECC71")))
        fig = go.Figure(go.Bar(y=df_gap_sorted[_cat_col], x=df_gap_sorted[_gap_col], orientation="h",
                                marker_color=colors.tolist()))
        fig.add_vline(x=100, line_dash="dash", line_color=VISA_GOLD, annotation_text=t("100 = proportional", "100 = proporcjonalne"))
        fig.update_layout(height=500, margin=dict(t=10,b=10), xaxis_title=t("Gap Index (100 = expected share)", "Indeks luki (100 = oczekiwany udział)"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("GUS Spending vs Visa Card Value", "Wydatki wg GUS a wartość płatności kartami Visa"))
        _cat_col2 = "Category" if lang == "EN" else "Kategoria"
        _visa_val_col = "Visa Value %" if lang == "EN" else "Wartość Visa %"
        fig = go.Figure()
        fig.add_trace(go.Bar(name=t("GUS Spending %", "Wydatki GUS %"), y=df_gap[_cat_col2], x=df_gap["GUS %"], orientation="h", marker_color=VISA_BLUE, opacity=0.6))
        fig.add_trace(go.Bar(name=t("Visa Value %", "Wartość Visa %"), y=df_gap[_cat_col2], x=df_gap[_visa_val_col], orientation="h", marker_color=ACCENT[1]))
        fig.update_layout(height=500, margin=dict(t=10,b=10), barmode="group", xaxis_title=t("% share", "% udziału"),
                          legend=dict(orientation="h",y=-0.1))
        st.plotly_chart(fig, use_container_width=True)
    source("gus_hbs", "visa")

    st.divider()
    st.subheader(t("The 3 Biggest Card-Free Zones Explained", "3 największe strefy bez kart"))

    tab1, tab2, tab3 = st.tabs([t("Housing & Utilities (20.6%)", "Mieszkanie i media (20.6%)"),
                                 t("Communications (4.0%)", "Komunikacja (4.0%)"),
                                 t("Healthcare (5.5%)", "Opieka zdrowotna (5.5%)")])

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
            **20.6% wszystkich wydatków gospodarstw domowych jest praktycznie niewidoczne dla kart (Indeks luki: 2)**

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
            **4.0% wydatków, ~0% na kartach (Indeks luki: ~1)**

            | Pozycja | Metoda płatności | Szansa kartowa |
            |---|---|---|
            | Rachunek za telefon | Polecenie zapłaty / BLIK | Zapisana karta (płatność cykliczna) |
            | Internet domowy | Polecenie zapłaty | Zapisana karta (płatność cykliczna) |
            | Doładowanie prepaid | BLIK / przelew | Płatność kartą w aplikacji |

            **Bariera strukturalna:** Telekomy ustawiają polecenie zapłaty przy podpisaniu umowy. Zapisanie karty wymaga aktywnej decyzji klienta.
            """)

    with tab3:
        if lang == "EN":
            st.markdown("""
            **5.5% of spending, but only 2.5% of card value (Gap Index: 46)**

            | Service | Visa TX Count | Card Issue |
            |---|---|---|
            | Pharmacies | 8.8M | Well covered |
            | Doctors & physicians | 255K | Cash dominant |
            | Hospitals | 99K | Limited terminals |
            | Dentists | 76K | Cash dominant |
            | Opticians | 157K | Moderate |

            **The split:** Product sales (pharmacy) = good card adoption. **Service delivery** (doctor visits, dental) = cash economy.
            Private healthcare in Poland is ~40% of total health spending — and most of it is cash.
            """)
        else:
            st.markdown("""
            **5.5% wydatków, ale tylko 2.5% wartości kartowej (Indeks luki: 46)**

            | Usługa | Liczba TX Visa | Problem kartowy |
            |---|---|---|
            | Apteki | 8.8M | Dobrze pokryte |
            | Lekarze | 255K | Dominacja gotówki |
            | Szpitale | 99K | Ograniczone terminale |
            | Dentyści | 76K | Dominacja gotówki |
            | Optycy | 157K | Umiarkowane |

            **Podział:** Sprzedaż produktów (apteka) = dobra adopcja kart. **Świadczenie usług** (wizyty lekarskie, stomatologia) = gospodarka gotówkowa.
            Prywatna opieka zdrowotna w Polsce to ~40% wszystkich wydatków na zdrowie — i większość to gotówka.
            """)
