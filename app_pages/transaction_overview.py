"""Page: Transaction Overview."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from app_pages.common import source, t, analysis, VISA_BLUE, VISA_GOLD, ACCENT


def render():
    st.header(t("Transaction Overview", "Przegląd transakcji"))
    st.caption(t("Sample dataset: 305.5M transactions, January 2025 – June 2026",
                  "Próbka danych: 305.5M transakcji, styczeń 2025 – czerwiec 2026"))

    # Monthly trends
    monthly = analysis["monthly_trends"]
    df_m = pd.DataFrame(monthly)
    df_m["month"] = df_m["prch_mnth_id"].astype(str).apply(lambda x: x[:4]+"-"+x[4:])

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Monthly Transaction Volume & Value", "Miesięczna liczba i wartość transakcji"))
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=df_m["month"], y=df_m["tx_count"]/1e6, name=t("Transactions (M)", "Transakcje (M)"), marker_color=VISA_BLUE, opacity=0.7), secondary_y=False)
        fig.add_trace(go.Scatter(x=df_m["month"], y=df_m["total_amount"]/1e9, name=t("Value (B)", "Wartość (mld)"), line=dict(color=VISA_GOLD, width=3)), secondary_y=True)
        fig.update_yaxes(title_text=t("Transactions (M)", "Transakcje (M)"), secondary_y=False)
        fig.update_yaxes(title_text=t("Value (B)", "Wartość (mld)"), secondary_y=True)
        fig.update_layout(height=400, margin=dict(t=10,b=30), legend=dict(orientation="h",y=-0.2))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("Average Transaction Value Over Time", "Średnia wartość transakcji w czasie"))
        fig = px.line(df_m, x="month", y="avg_amount", markers=True)
        fig.update_traces(line_color=ACCENT[0], line_width=3)
        fig.update_layout(height=400, margin=dict(t=10,b=30), yaxis_title=t("Avg amount", "Średnia kwota"), yaxis_range=[170,200])
        st.plotly_chart(fig, use_container_width=True)
    source("visa")

    st.divider()

    # Hourly & Daily
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Hourly Pattern (GMT → Poland = +1/+2h)", "Rozkład godzinowy (GMT → czas polski = +1/+2 h)"))
        hourly = analysis["hourly_pattern"]
        df_h = pd.DataFrame(hourly)
        df_h["hour_label"] = df_h["hour_gmt"].apply(lambda h: f"{(h+1)%24}:00")
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=df_h["hour_label"], y=df_h["tx_count"]/1e6, name=t("TX (M)", "TX (M)"), marker_color=VISA_BLUE, opacity=0.6), secondary_y=False)
        fig.add_trace(go.Scatter(x=df_h["hour_label"], y=df_h["avg_amount"], name=t("Avg amount", "Średnia kwota"), line=dict(color=VISA_GOLD, width=2)), secondary_y=True)
        fig.update_layout(height=350, margin=dict(t=10,b=30), legend=dict(orientation="h",y=-0.2))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("Day of Week Pattern", "Rozkład dzienny"))
        daily = analysis["day_of_week"]
        df_d = pd.DataFrame(daily)
        colors = [VISA_BLUE]*7
        colors[df_d["tx_count"].idxmax()] = VISA_GOLD
        colors[df_d["tx_count"].idxmin()] = ACCENT[1]
        fig = go.Figure(go.Bar(x=df_d["day_name"], y=df_d["tx_count"]/1e6, marker_color=colors))
        fig.update_layout(height=350, margin=dict(t=10,b=30), yaxis_title=t("TX (millions)", "TX (mln)"))
        st.plotly_chart(fig, use_container_width=True)
    source("visa")

    st.divider()

    # Top categories & merchants
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Top 15 Merchant Categories", "15 największych kategorii sprzedawców"))
        cats = analysis["top_categories"][:15]
        df_c = pd.DataFrame(cats)
        fig = px.bar(df_c, y="mrch_catg_nm", x="tx_count", orientation="h", color_discrete_sequence=[VISA_BLUE])
        fig.update_layout(height=500, margin=dict(t=10,b=10,l=10), yaxis=dict(autorange="reversed"), xaxis_title=t("Transactions", "Transakcje"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("Top 15 Merchants", "15 największych sprzedawców"))
        merch = analysis["top_merchants"][:15]
        df_me = pd.DataFrame(merch)
        fig = px.bar(df_me, y="mrch_nm_raw", x="tx_count", orientation="h", color_discrete_sequence=[ACCENT[3]])
        fig.update_layout(height=500, margin=dict(t=10,b=10,l=10), yaxis=dict(autorange="reversed"), xaxis_title=t("Transactions", "Transakcje"))
        st.plotly_chart(fig, use_container_width=True)
    source("visa")

    st.divider()

    # Payment channels
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader(t("Payment Channels", "Kanały płatności"))
        ch = analysis["channel"]
        df_ch = pd.DataFrame(ch)
        fig = px.pie(df_ch, names="channel_flg", values="tx_count", color_discrete_sequence=ACCENT, hole=0.35)
        fig.update_layout(height=350, margin=dict(t=10,b=30))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(t("Physical vs Online", "Sklepy a online"))
        cp = analysis["cp_flag"]
        labels = [t("Physical (88.8%)", "W sklepach (88.8%)"), t("Online (11.2%)", "Online (11.2%)")]
        fig = px.pie(names=labels, values=[cp[0]["tx_count"], cp[1]["tx_count"]], color_discrete_sequence=[VISA_BLUE, ACCENT[1]], hole=0.35)
        fig.update_layout(height=350, margin=dict(t=10,b=30))
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.subheader(t("Card Types", "Rodzaje kart"))
        ct = analysis["card_types"][:6]
        df_ct = pd.DataFrame(ct)
        fig = px.pie(df_ct, names="crd_typ_nm", values="tx_count", color_discrete_sequence=ACCENT, hole=0.35)
        fig.update_layout(height=350, margin=dict(t=10,b=30))
        st.plotly_chart(fig, use_container_width=True)
    source("visa")
