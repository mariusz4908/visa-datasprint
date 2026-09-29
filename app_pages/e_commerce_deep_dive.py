"""Page: E-Commerce Deep Dive."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from app_pages.common import t, ecommerce, precise, VISA_BLUE, VISA_GOLD, ACCENT


def render():
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
        st.subheader(t("Online vs Physical: Avg Transaction Value", "Online vs Fizyczne: Średnia Wartosc Transakcji"))
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
                      xaxis_title="% of transactions that are online", coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    st.error(t("🛒 **E-Grocery Gap:** Groceries = 26.3% of all card TX but only **0.12%** are online. E-pharmacy = **0.18%**. In mature markets, e-grocery is 10-15% of food retail. At just 5% penetration this would mean millions of new high-value online card transactions.",
                "🛒 **Luka E-Grocery:** Spozywcze = 26.3% wszystkich TX kartowych, ale tylko **0.12%** online. E-apteka = **0.18%**. Na dojrzalych rynkach e-grocery to 10-15% handlu spożywczego. Przy zaledwie 5% penetracji to miliony nowych wysokowartościowych transakcji kartowych online."))
