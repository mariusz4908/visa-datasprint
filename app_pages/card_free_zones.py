"""Page: Card-Free Zones."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from app_pages.common import t, VISA_BLUE, VISA_GOLD, ACCENT


def render():
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
        st.subheader(t("GUS Spending vs Visa Card Value", "Wydatki GUS vs Wartość Kart Visa"))
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
