"""Page: Predictive Models & Simulations."""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app_pages.common import load_json, VISA_BLUE, VISA_GOLD, BLIK_PINK, ACCENT


def render():
    models = load_json("model_results.json")
    st.header("Predictive Models & Simulations")
    st.caption("6 models projecting Visa QR Pay adoption, transaction volume, BLIK cannibalization, ROI, and market share impact over 36 months")

    scenario = st.radio("Select scenario:", ["Conservative", "Base", "Optimistic"], index=1, horizontal=True)

    months_labels = [f"M{i+1}" for i in range(36)]
    year_labels = [""] * 36
    for i in [0, 11, 23, 35]:
        year_labels[i] = f"Y{i//12+1}" if i > 0 else "Start"

    # KPIs for selected scenario
    r = models["revenue"][scenario]
    a = models["adoption"][scenario]
    v = models["volume"][scenario]
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("3Y Adopters", f"{a['cumulative'][35]/1e6:.1f}M", f"{a['penetration_pct'][35]:.0f}% penetration")
    c2.metric("3Y Total TX", f"{v['cumulative_tx'][35]/1e6:.0f}M")
    c3.metric("3Y Total Value", f"{v['cumulative_val'][35]/1e9:.1f}B PLN")
    c4.metric("3Y Revenue", f"{r['total_3yr_revenue']/1e6:.0f}M PLN", f"ROI: {r['roi_pct']:.0f}%")
    be = r["breakeven_month"]
    c5.metric("Break-even", f"Month {be}" if be else "Not reached", "within 3 years" if be else "needs more time")

    st.divider()

    # ── MODEL 1: ADOPTION S-CURVE ──
    st.subheader("Model 1: Adoption S-Curve (Bass Diffusion)")
    st.caption("Bass diffusion model: p = innovation coefficient (marketing), q = imitation coefficient (word-of-mouth)")

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        colors_sc = {"Conservative": ACCENT[1], "Base": VISA_BLUE, "Optimistic": ACCENT[2]}
        for name in ["Conservative", "Base", "Optimistic"]:
            ad = models["adoption"][name]
            fig.add_trace(go.Scatter(x=months_labels, y=np.array(ad["cumulative"])/1e6,
                                     name=name, line=dict(color=colors_sc[name], width=3 if name==scenario else 1.5,
                                                          dash="solid" if name==scenario else "dot")))
        fig.update_layout(height=400, yaxis_title="Cumulative adopters (millions)", title_text="QR Pay Adoption Curve",
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        for name in ["Conservative", "Base", "Optimistic"]:
            ad = models["adoption"][name]
            fig.add_trace(go.Bar(x=months_labels, y=np.array(ad["monthly_new"])/1e3,
                                 name=name, marker_color=colors_sc[name],
                                 visible=True if name==scenario else "legendonly"))
        fig.update_layout(height=400, yaxis_title="New adopters per month (K)", title_text="Monthly New Adopters",
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Model assumptions"):
        st.json(models["assumptions"]["adoption_params"])

    st.divider()

    # ── MODEL 2: TRANSACTION VOLUME ──
    st.subheader("Model 2: Transaction Volume Projection")

    sv = models["volume"][scenario]
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["p2p_tx_monthly"])/1e6,
                                 name="P2P", fill="tonexty", line=dict(color=ACCENT[0]), stackgroup="one"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["ecom_tx_monthly"])/1e6,
                                 name="E-Commerce", fill="tonexty", line=dict(color=ACCENT[3]), stackgroup="one"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["svc_tx_monthly"])/1e6,
                                 name="Services", fill="tonexty", line=dict(color=ACCENT[2]), stackgroup="one"))
        fig.update_layout(height=400, yaxis_title="Monthly TX (millions)", title_text=f"Monthly Transactions — {scenario}",
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["p2p_val_monthly"])/1e9,
                                 name="P2P", fill="tonexty", line=dict(color=ACCENT[0]), stackgroup="one"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["ecom_val_monthly"])/1e9,
                                 name="E-Commerce", fill="tonexty", line=dict(color=ACCENT[3]), stackgroup="one"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["svc_val_monthly"])/1e9,
                                 name="Services", fill="tonexty", line=dict(color=ACCENT[2]), stackgroup="one"))
        fig.update_layout(height=400, yaxis_title="Monthly value (B PLN)", title_text=f"Monthly Transaction Value — {scenario}",
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Activity assumptions per user/month"):
        st.json(models["assumptions"]["activity_params"])

    st.divider()

    # ── MODEL 3: CANNIBALIZATION ──
    st.subheader("Model 3: BLIK Cannibalization vs Net New Volume")
    st.caption("How much QR Pay volume is taken from BLIK vs genuinely new card transaction volume?")

    cn = models["cannibalization"][scenario]
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(cn["net_new_monthly"])/1e6,
                                 name="Net new to Visa (from cash/transfer)", fill="tozeroy",
                                 line=dict(color=ACCENT[2]), fillcolor="rgba(46,204,113,0.3)"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(cn["from_blik_monthly"])/1e6,
                                 name="Cannibalized from BLIK", fill="tozeroy",
                                 line=dict(color=BLIK_PINK), fillcolor="rgba(212,14,106,0.2)"))
        fig.update_layout(height=400, yaxis_title="Monthly value (M PLN)", title_text=f"Source of QR Pay Volume — {scenario}",
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Pie at month 36
        net_new_36 = cn["net_new_monthly"][35]
        blik_36 = cn["from_blik_monthly"][35]
        existing_36 = cn["from_existing_card"][35]
        fig = px.pie(names=["Net new (cash/transfer → card)", "From BLIK", "From existing card"],
                     values=[net_new_36, blik_36, existing_36],
                     color_discrete_sequence=[ACCENT[2], BLIK_PINK, ACCENT[0]], hole=0.35,
                     title=f"Volume Source at Month 36 — {scenario}")
        fig.update_layout(height=400, margin=dict(t=40,b=30))
        st.plotly_chart(fig, use_container_width=True)

    net_new_pct = cn["net_new_pct"][35]
    st.info(f"**{scenario} scenario at Month 36:** {net_new_pct:.0f}% of QR Pay volume is NET NEW to the card ecosystem (from cash/transfers). {100-net_new_pct:.0f}% is cannibalized from BLIK or existing card channels.")

    st.divider()

    # ── MODEL 4: REVENUE & ROI ──
    st.subheader("Model 4: Revenue & ROI Projection")

    rv = models["revenue"][scenario]
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["cumulative_revenue"])/1e6,
                                 name="Cumulative Revenue", line=dict(color=ACCENT[2], width=3), fill="tozeroy", fillcolor="rgba(46,204,113,0.15)"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["cumulative_costs"])/1e6,
                                 name="Cumulative Costs", line=dict(color=ACCENT[1], width=3, dash="dash")))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["cumulative_profit"])/1e6,
                                 name="Cumulative Profit", line=dict(color=VISA_BLUE, width=3)))
        if rv["breakeven_month"]:
            fig.add_vline(x=rv["breakeven_month"]-1, line_dash="dot", line_color=VISA_GOLD,
                          annotation_text=f"Break-even: M{rv['breakeven_month']}")
        fig.update_layout(height=400, yaxis_title="PLN (millions)", title_text=f"Cumulative P&L — {scenario}",
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["p2p_rev"])/1e6,
                                 name="P2P revenue", fill="tonexty", stackgroup="one", line=dict(color=ACCENT[0])))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["ecom_rev"])/1e6,
                                 name="E-commerce revenue", fill="tonexty", stackgroup="one", line=dict(color=ACCENT[3])))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["svc_rev"])/1e6,
                                 name="Services revenue", fill="tonexty", stackgroup="one", line=dict(color=ACCENT[2])))
        fig.update_layout(height=400, yaxis_title="Monthly revenue (M PLN)", title_text=f"Revenue by Channel — {scenario}",
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Cost breakdown"):
        st.json(models["costs"])

    st.divider()

    # ── MODEL 5: E-COMMERCE MARKET SHARE ──
    st.subheader("Model 5: E-Commerce Market Share Simulation")
    st.caption("How QR Pay changes Visa's share of the Polish e-commerce payments market")

    es = models["ecom_share"][scenario]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months_labels, y=es["visa_share_pct"], name="Visa total (card + QR Pay)",
                             line=dict(color=VISA_BLUE, width=3)))
    fig.add_trace(go.Scatter(x=months_labels, y=es["visa_base_share"], name="Visa baseline (without QR Pay)",
                             line=dict(color=VISA_BLUE, width=1.5, dash="dot")))
    fig.add_trace(go.Scatter(x=months_labels, y=es["blik_share_pct"], name="BLIK (adjusted)",
                             line=dict(color=BLIK_PINK, width=3)))
    fig.add_hline(y=es["visa_base_share"][0], line_dash="dash", line_color="#ccc",
                  annotation_text=f"Current Visa e-com share: {es['visa_base_share'][0]:.1f}%")
    fig.update_layout(height=450, yaxis_title="Market share (%)", title_text=f"E-Commerce Payment Share — {scenario}",
                      legend=dict(orientation="h",y=-0.12), margin=dict(t=40,b=40))
    st.plotly_chart(fig, use_container_width=True)

    visa_start = es["visa_share_pct"][0]
    visa_end = es["visa_share_pct"][35]
    blik_start = es["blik_share_pct"][0]
    blik_end = es["blik_share_pct"][35]
    st.success(f"**{scenario}:** Visa e-commerce share moves from **{visa_start:.1f}%** to **{visa_end:.1f}%** (+{visa_end-visa_start:.1f}pp). BLIK declines from **{blik_start:.1f}%** to **{blik_end:.1f}%** ({blik_end-blik_start:+.1f}pp).")

    st.divider()

    # ── MODEL 6: SENSITIVITY ──
    st.subheader("Model 6: Sensitivity Analysis")
    st.caption("How 3-year revenue changes when we vary each key parameter ±50% from base")

    sens = pd.DataFrame(models["sensitivity"])
    base_rev = sens[(sens["parameter"]==sens["parameter"].iloc[0]) & (sens["multiplier"]==1.0)]["revenue_3yr_mln"].values[0]

    param_choice = st.selectbox("Select parameter:", sens["parameter"].unique())
    df_p = sens[sens["parameter"] == param_choice]

    fig = go.Figure()
    colors_bar = df_p["multiplier"].apply(lambda m: VISA_BLUE if m == 1.0 else (ACCENT[2] if m > 1 else ACCENT[1]))
    fig.add_trace(go.Bar(x=df_p["multiplier"].apply(lambda m: f"{m:.0%}"), y=df_p["revenue_3yr_mln"],
                         marker_color=colors_bar.tolist(), text=df_p["revenue_3yr_mln"].apply(lambda v: f"{v:.0f}M"),
                         textposition="outside"))
    fig.add_hline(y=base_rev, line_dash="dash", line_color=VISA_GOLD, annotation_text=f"Base: {base_rev:.0f}M PLN")
    fig.update_layout(height=400, yaxis_title="3-year revenue (M PLN)",
                      xaxis_title=f"{param_choice} (multiplier vs base)",
                      title_text=f"Sensitivity: {param_choice}", margin=dict(t=40,b=40))
    st.plotly_chart(fig, use_container_width=True)

    # Tornado chart
    st.subheader("Tornado Chart: Revenue Sensitivity to All Parameters")
    tornado = []
    for param in sens["parameter"].unique():
        df_param = sens[sens["parameter"] == param]
        low = df_param[df_param["multiplier"] == 0.5]["revenue_3yr_mln"].values[0]
        high = df_param[df_param["multiplier"] == 1.5]["revenue_3yr_mln"].values[0]
        base = df_param[df_param["multiplier"] == 1.0]["revenue_3yr_mln"].values[0]
        tornado.append({"Parameter": param, "Low (50%)": low - base, "High (150%)": high - base, "Range": high - low})

    df_torn = pd.DataFrame(tornado).sort_values("Range", ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(y=df_torn["Parameter"], x=df_torn["Low (50%)"], name="50% of base",
                         orientation="h", marker_color=ACCENT[1]))
    fig.add_trace(go.Bar(y=df_torn["Parameter"], x=df_torn["High (150%)"], name="150% of base",
                         orientation="h", marker_color=ACCENT[2]))
    fig.update_layout(height=400, xaxis_title="Impact on 3Y revenue (M PLN vs base)",
                      barmode="overlay", title_text="Tornado: Which Parameters Matter Most",
                      legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── SCENARIO COMPARISON TABLE ──
    st.subheader("Scenario Comparison Summary")
    comp_data = []
    for name in ["Conservative", "Base", "Optimistic"]:
        a = models["adoption"][name]
        v = models["volume"][name]
        r = models["revenue"][name]
        cn = models["cannibalization"][name]
        comp_data.append({
            "Scenario": name,
            "Y3 Adopters": f"{a['cumulative'][35]/1e6:.1f}M",
            "Y3 Penetration": f"{a['penetration_pct'][35]:.0f}%",
            "Y3 Monthly TX": f"{v['total_tx_monthly'][35]/1e6:.1f}M",
            "Y3 Monthly Value": f"{v['total_val_monthly'][35]/1e9:.1f}B PLN",
            "3Y Revenue": f"{r['total_3yr_revenue']/1e6:.0f}M PLN",
            "3Y Profit": f"{r['total_3yr_profit']/1e6:.0f}M PLN",
            "ROI": f"{r['roi_pct']:.0f}%",
            "Break-even": f"Month {r['breakeven_month']}" if r["breakeven_month"] else "Not reached",
            "Net New %": f"{cn['net_new_pct'][35]:.0f}%",
        })
    st.dataframe(pd.DataFrame(comp_data), use_container_width=True, hide_index=True)
