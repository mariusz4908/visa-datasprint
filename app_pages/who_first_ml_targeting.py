"""Page: Who First — ML Targeting."""
import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app_pages.common import DATA_DIR, load_json, VISA_BLUE, VISA_GOLD, BLIK_PINK, ACCENT


def render():
    ml_results = {"target_audiences.json": "target_audiences.ipynb", "readiness_model.json": "readiness_model.ipynb"}
    missing = [nb for f, nb in ml_results.items()
               if not os.path.exists(os.path.join(DATA_DIR, "ml_readiness", "results", f))]
    if missing:
        st.warning("ML results not found. Run these notebooks in `ml_readiness/` first: " + ", ".join(missing))
        st.stop()
    aud_data = load_json(os.path.join("ml_readiness", "results", "target_audiences.json"))
    model_data = load_json(os.path.join("ml_readiness", "results", "readiness_model.json"))

    st.header("Who First — ML Targeting for Visa QR Pay")
    st.caption("Card behaviour Jan–Jun 2026 · readiness model trained and validated on Visa data · "
               "all figures aggregated to groups of 30+ cards")

    st.markdown("""
    <div style="background: linear-gradient(135deg, #E8F0FE, #D0E0FF); padding: 20px 24px; border-radius: 14px; border-left: 5px solid #1A1F71;">
        <p style="margin:0; font-size:1em;">
        QR Pay removes the typed card number. Three data-driven tools decide who gets it first:
        a <strong>data rule</strong> finds cards that type their number today,
        <strong>new cards</strong> get QR at issuance, and a <strong>machine-learning model</strong>
        finds the never-online cards that are about to make their first online payment.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

    aud = pd.DataFrame(aud_data["audiences"]).set_index("audience")
    roi = aud_data["roi_inputs"]
    a = aud.loc["A mostly typing"]
    c = aud.loc["C ready to start"]
    final = model_data["final_test"]
    gains = pd.DataFrame(model_data["gains"])
    top20_reach = gains.loc[gains.contacted_pct == 20, "starters_reached_pct"].iloc[0]

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Wave 1 · mostly typing", f"{a.cards / 1000:.0f}K cards",
              f"{a.share_of_typed_tx:.0%} of all typed online payments", delta_color="off")
    k2.metric("From issuance · new cards", f"{roi['new_cards']['per_month_avg'] / 1000:.0f}K / month",
              f"{roi['new_cards']['first_online_payment_typed']:.0%} of first online payments typed", delta_color="off")
    k3.metric("Wave 2 · ready (ML)", f"{c.cards / 1000:.0f}K cards",
              f"~{c.expected_starters_3m / 1000:.1f}K first online payments in 3 months", delta_color="off")
    k4.metric("Model accuracy (AUC)", f"{final['AUC']:.2f}",
              f"top 20% of cards = {top20_reach:.0f}% of starters", delta_color="off")

    tab_aud, tab_model, tab_personas, tab_new = st.tabs(
        ["🎯 Audiences", "🤖 Readiness model", "👥 Personas", "🆕 New cards"])

    # ── Audiences ──
    with tab_aud:
        roles = {
            "A mostly typing": "Wave 1 — QR in the banking app replaces typing",
            "C ready to start": "Wave 2 — QR at the first online payment (ML model)",
            "D sometimes typing": "Wave 3",
            "E not ready": "Not targeted",
            "F never typing": "Not targeted — already one-click",
            "L lapsed": "Not targeted",
        }
        tbl = aud.reset_index()
        tbl["Role"] = tbl.audience.map(roles)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Active cards per audience")
            fig = px.bar(tbl.sort_values("audience", ascending=False), x="cards", y="audience", orientation="h",
                         color="audience", color_discrete_sequence=[VISA_BLUE, VISA_GOLD, ACCENT[0], "#bbb", "#999", "#ccc"])
            fig.update_layout(height=320, margin=dict(t=10, b=30), showlegend=False, xaxis_title="cards", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.subheader("Share of typed online card payments")
            fig = px.bar(tbl.sort_values("audience", ascending=False), x="share_of_typed_tx", y="audience",
                         orientation="h", color_discrete_sequence=[BLIK_PINK])
            fig.update_layout(height=320, margin=dict(t=10, b=30), xaxis_tickformat=".0%", xaxis_title="", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)

        st.dataframe(pd.DataFrame({
            "Audience": tbl.audience,
            "Cards": tbl.cards.map("{:,.0f}".format),
            "Share of active cards": tbl.share_of_cards.map("{:.0%}".format),
            "Typed payments / card / month": tbl.typed_tx_per_card_month.map("{:.1f}".format),
            "Mostly pay by phone in store": tbl.mostly_wallet_share.map("{:.0%}".format),
            "Role": tbl.Role,
        }), hide_index=True, use_container_width=True)

        st.divider()
        st.subheader("Wave 1: where do typers type their card number?")
        cats = pd.DataFrame(aud_data["audience_a_categories"]).head(10)
        device = aud_data["audience_a_device_typed_tx"]
        phone_share = device["phone"] / (device["phone"] + device["computer_other"])
        dec = pd.DataFrame(aud_data["audience_a_deciles"])
        col1, col2 = st.columns([3, 2])
        with col1:
            fig = px.bar(cats.sort_values("share_of_a_typed_pct"), x="share_of_a_typed_pct", y="category",
                         orientation="h", color="polish_merchant_pct", color_continuous_scale="Blues",
                         labels={"share_of_a_typed_pct": "% of their typed payments", "category": "",
                                 "polish_merchant_pct": "% Polish merchants"})
            fig.update_layout(height=380, margin=dict(t=10, b=30))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.metric("Typed payments made on a phone", f"{phone_share:.0%}")
            st.caption("QR Pay must work from the banking app / phone, not only from the plastic card.")
            top20 = dec.loc[dec.group == "top 20%", "cum_share_of_typed_pct"].iloc[0]
            st.metric("Typing done by the heaviest 20% of typers", f"{top20:.0f}%")
            st.caption("Contact order: start with the heaviest typers.")
            fig = go.Figure(go.Scatter(x=[0] + list(range(10, 101, 10)), y=[0] + dec.cum_share_of_typed_pct.tolist(),
                                       mode="lines+markers", line=dict(color=VISA_BLUE, width=3)))
            fig.add_trace(go.Scatter(x=[0, 100], y=[0, 100], mode="lines", line=dict(color="#bbb", dash="dash")))
            fig.update_layout(height=220, margin=dict(t=10, b=30), showlegend=False,
                              xaxis_title="% of typers contacted", yaxis_title="% of typing covered")
            st.plotly_chart(fig, use_container_width=True)

    # ── Readiness model ──
    with tab_model:
        st.markdown(f"""
        **What it does:** for every card that has never paid online, it estimates the chance of a first online card
        payment in the next 3 months, using only in-store behaviour (LightGBM, calibrated).

        **How well:** tested on three later periods it never saw. On the final test ({final['period']},
        {final['cards']:,} cards, {final['start_rate']:.1%} start) the top 10% of cards start
        **{final['lift top 10%']:.1f}×** more often than average and the top 20% contain
        **{top20_reach:.0f}%** of all future starters.
        """)
        bt = pd.DataFrame(model_data["backtest"])
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Backtest: AUC by test period")
            fig = px.bar(bt, x="test snapshot", y="AUC", color="model", barmode="group",
                         color_discrete_sequence=["#bbb", ACCENT[0], VISA_BLUE])
            fig.update_layout(height=340, margin=dict(t=10, b=30), yaxis_range=[0.5, 0.8], xaxis_title="",
                              legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.subheader("Gains: reach of future starters")
            fig = go.Figure(go.Scatter(x=[0] + gains.contacted_pct.tolist(), y=[0] + gains.starters_reached_pct.tolist(),
                                       mode="lines+markers", name="model", line=dict(color=VISA_BLUE, width=3)))
            fig.add_trace(go.Scatter(x=[0, 100], y=[0, 100], mode="lines", name="random",
                                     line=dict(color="#bbb", dash="dash")))
            fig.update_layout(height=340, margin=dict(t=10, b=30), xaxis_title="% of cards contacted",
                              yaxis_title="% of starters reached", legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig, use_container_width=True)

        labels = {"evening_share": "Evening activity", "s_fast_food": "Fast food", "s_car_fuel": "Fuel & car",
                  "wallet_ever": "Ever paid by phone in store", "s_restaurants_bars": "Restaurants & bars",
                  "wallet_share": "Share paid by phone in store", "typical_store_amount": "Typical in-store amount",
                  "s_public_transport": "Public transport", "abroad_share": "Payments abroad",
                  "s_entertainment_betting": "Entertainment", "tx_trend": "Activity trend", "home_area": "Home area",
                  "s_fashion_sport": "Fashion & sport", "cnp_other_share": "Money transfers / top-ups",
                  "active_months": "Active months", "card_age_months": "Card age"}
        drv = pd.DataFrame(model_data["drivers"])
        drv["label"] = drv.feature.map(labels).fillna(drv.feature)
        drv["effect"] = drv.direction.map({"higher -> more likely": "more → more likely",
                                           "higher -> less likely": "more → less likely"}).fillna("mixed")
        col1, col2 = st.columns([3, 2])
        with col1:
            st.subheader("What predicts a first online payment")
            fig = px.bar(drv.sort_values("mean_abs_shap"), x="mean_abs_shap", y="label", orientation="h", color="effect",
                         color_discrete_map={"more → more likely": "#2ECC71", "more → less likely": "#E74C3C",
                                             "mixed": "#bbb"},
                         labels={"mean_abs_shap": "impact (mean |SHAP|)", "label": ""})
            fig.update_layout(height=420, margin=dict(t=10, b=30), legend=dict(orientation="h", y=-0.15))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.subheader("Calibration")
            cal = pd.DataFrame(model_data["calibration_deciles"])
            fig = go.Figure()
            fig.add_trace(go.Bar(x=cal.decile, y=cal.actual * 100, name="actual", marker_color=VISA_BLUE))
            fig.add_trace(go.Scatter(x=cal.decile, y=cal.calibrated * 100, name="predicted", mode="lines+markers",
                                     line=dict(color=VISA_GOLD, width=3)))
            fig.update_layout(height=420, margin=dict(t=10, b=30), xaxis_title="score decile (10 = highest)",
                              yaxis_title="start rate (%)", legend=dict(orientation="h", y=-0.15))
            st.plotly_chart(fig, use_container_width=True)
        st.info("The model predicts who is **about to** start paying online — the moment QR Pay should take over. "
                "What QR itself adds is measured in the pilot with a random control group (~10% of each audience).")

    # ── Personas ──
    with tab_personas:
        st.markdown("Six behavioural personas from **in-store behaviour only** (KMeans). The model finds ready cards "
                    "even inside low-adoption personas, which persona targeting alone would miss.")
        per = pd.DataFrame(model_data["personas"])
        fig = go.Figure()
        fig.add_trace(go.Bar(x=per.persona, y=per.actual_start_pct, name="all cards in persona", marker_color="#bbb"))
        fig.add_trace(go.Bar(x=per.persona, y=per.top10_start_pct, name="model's top 10% inside persona",
                             marker_color=VISA_BLUE))
        fig.update_layout(height=380, barmode="group", margin=dict(t=10, b=30), yaxis_title="start within 3 months (%)",
                          legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig, use_container_width=True)
        mix = pd.DataFrame(aud_data["audience_persona_cards"])
        mix = mix[mix.audience.isin(["A mostly typing", "C ready to start", "E not ready"])]
        mix["share"] = mix.cards / mix.groupby("audience").cards.transform("sum")
        fig = px.bar(mix, x="share", y="audience", color="persona", orientation="h",
                     color_discrete_sequence=ACCENT, labels={"share": "share of audience", "audience": ""})
        fig.update_layout(height=260, margin=dict(t=10, b=30), xaxis_tickformat=".0%", legend=dict(orientation="h", y=-0.3))
        st.subheader("Persona mix of the audiences")
        st.plotly_chart(fig, use_container_width=True)

    # ── New cards ──
    with tab_new:
        coh = pd.DataFrame(aud_data["new_card_cohorts"])
        coh["month"] = coh.cohort_m.apply(lambda m: f"{2025 + m // 12}-{m % 12 + 1:02d}")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("New cards per month")
            fig = px.bar(coh, x="month", y="cards", color_discrete_sequence=[VISA_BLUE])
            fig.update_layout(height=340, margin=dict(t=10, b=30), xaxis_title="", yaxis_title="cards")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.subheader("What new cards do")
            fig = go.Figure()
            for col, name, color in [("wallet_first_month", "phone in store, 1st month", ACCENT[0]),
                                     ("online_within_3m", "online within 3 months", VISA_BLUE),
                                     ("first_online_typed", "first online payment typed", BLIK_PINK)]:
                fig.add_trace(go.Scatter(x=coh.month, y=coh[col] * 100, name=name, mode="lines+markers",
                                         line=dict(color=color, width=3)))
            fig.update_layout(height=340, margin=dict(t=10, b=30), yaxis_title="%", legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig, use_container_width=True)
        st.success(f"About half of new cards pay online within 3 months, and "
                   f"**{roi['new_cards']['first_online_payment_typed']:.0%} of those first online payments are typed**. "
                   "QR on every new card makes the first online payment effortless — the cheapest way to scale.")
