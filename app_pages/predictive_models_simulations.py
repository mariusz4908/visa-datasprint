"""Page: Predictive Models & Simulations."""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app_pages.common import load_json, t, VISA_BLUE, VISA_GOLD, BLIK_PINK, ACCENT


def render():
    lang = st.session_state.get("lang", "EN")

    models = load_json("model_results.json")
    st.header(t("Predictive Models & Simulations", "Modele Predykcyjne i Symulacje"))
    st.caption(t("6 models projecting Visa QR Pay adoption, transaction volume, BLIK cannibalization, ROI, and market share impact over 36 months",
                  "6 modeli prognozujacych adopcje Visa QR Pay, wolumen transakcji, kanibalizacje BLIK, ROI i wplyw na udzial rynkowy w ciagu 36 miesiecy"))

    scenario_labels = [t("Conservative", "Konserwatywny"), t("Base", "Bazowy"), t("Optimistic", "Optymistyczny")]
    scenario_map = {t("Conservative", "Konserwatywny"): "Conservative", t("Base", "Bazowy"): "Base", t("Optimistic", "Optymistyczny"): "Optimistic"}
    scenario_label = st.radio(t("Select scenario:", "Wybierz scenariusz:"), scenario_labels, index=1, horizontal=True)
    scenario = scenario_map[scenario_label]

    months_labels = [f"M{i+1}" for i in range(36)]
    year_labels = [""] * 36
    for i in [0, 11, 23, 35]:
        year_labels[i] = f"Y{i//12+1}" if i > 0 else "Start"

    # KPIs for selected scenario
    r = models["revenue"][scenario]
    a = models["adoption"][scenario]
    v = models["volume"][scenario]
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric(t("3Y Adopters", "Uzytkownicy 3L"), f"{a['cumulative'][35]/1e6:.1f}M", f"{a['penetration_pct'][35]:.0f}% {t('penetration', 'penetracji')}")
    c2.metric(t("3Y Total TX", "Lacznie TX 3L"), f"{v['cumulative_tx'][35]/1e6:.0f}M")
    c3.metric(t("3Y Total Value", "Łączna Wartość 3L"), f"{v['cumulative_val'][35]/1e9:.1f}B PLN")
    c4.metric(t("3Y Revenue", "Przychod 3L"), f"{r['total_3yr_revenue']/1e6:.0f}M PLN", f"ROI: {r['roi_pct']:.0f}%")
    be = r["breakeven_month"]
    c5.metric(t("Break-even", "Punkt Rentowności"), f"{t('Month', 'Miesiac')} {be}" if be else t("Not reached", "Nie osiagniety"), t("within 3 years", "w ciągu 3 lat") if be else t("needs more time", "potrzeba więcej czasu"))

    st.divider()

    # ── MODEL 1: ADOPTION S-CURVE ──
    st.subheader(t("Model 1: Adoption S-Curve (Bass Diffusion)", "Model 1: Krzywa Adopcji S (Dyfuzja Bassa)"))
    st.caption(t("Bass diffusion model: p = innovation coefficient (marketing), q = imitation coefficient (word-of-mouth)",
                  "Model dyfuzji Bassa: p = wspolczynnik innowacji (marketing), q = wspolczynnik imitacji (marketing szeptany)"))

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        colors_sc = {"Conservative": ACCENT[1], "Base": VISA_BLUE, "Optimistic": ACCENT[2]}
        for name in ["Conservative", "Base", "Optimistic"]:
            ad = models["adoption"][name]
            fig.add_trace(go.Scatter(x=months_labels, y=np.array(ad["cumulative"])/1e6,
                                     name=name, line=dict(color=colors_sc[name], width=3 if name==scenario else 1.5,
                                                          dash="solid" if name==scenario else "dot")))
        fig.update_layout(height=400, yaxis_title=t("Cumulative adopters (millions)", "Skumulowani użytkownicy (mln)"), title_text=t("QR Pay Adoption Curve", "Krzywa Adopcji QR Pay"),
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        for name in ["Conservative", "Base", "Optimistic"]:
            ad = models["adoption"][name]
            fig.add_trace(go.Bar(x=months_labels, y=np.array(ad["monthly_new"])/1e3,
                                 name=name, marker_color=colors_sc[name],
                                 visible=True if name==scenario else "legendonly"))
        fig.update_layout(height=400, yaxis_title=t("New adopters per month (K)", "Nowi użytkownicy/mies. (tys.)"), title_text=t("Monthly New Adopters", "Nowi Użytkownicy Miesięcznie"),
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with st.expander(t("Model assumptions", "Zalozenia modelu")):
        st.json(models["assumptions"]["adoption_params"])

    st.divider()

    # ── MODEL 2: TRANSACTION VOLUME ──
    st.subheader(t("Model 2: Transaction Volume Projection", "Model 2: Prognoza Wolumenu Transakcji"))

    sv = models["volume"][scenario]
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["p2p_tx_monthly"])/1e6,
                                 name="P2P", fill="tonexty", line=dict(color=ACCENT[0]), stackgroup="one"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["ecom_tx_monthly"])/1e6,
                                 name="E-Commerce", fill="tonexty", line=dict(color=ACCENT[3]), stackgroup="one"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["svc_tx_monthly"])/1e6,
                                 name=t("Services", "Usługi"), fill="tonexty", line=dict(color=ACCENT[2]), stackgroup="one"))
        fig.update_layout(height=400, yaxis_title=t("Monthly TX (millions)", "Miesięczne TX (mln)"), title_text=t(f"Monthly Transactions — {scenario}", f"Miesięczne Transakcje — {scenario}"),
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["p2p_val_monthly"])/1e9,
                                 name="P2P", fill="tonexty", line=dict(color=ACCENT[0]), stackgroup="one"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["ecom_val_monthly"])/1e9,
                                 name="E-Commerce", fill="tonexty", line=dict(color=ACCENT[3]), stackgroup="one"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(sv["svc_val_monthly"])/1e9,
                                 name=t("Services", "Usługi"), fill="tonexty", line=dict(color=ACCENT[2]), stackgroup="one"))
        fig.update_layout(height=400, yaxis_title=t("Monthly value (B PLN)", "Wartość miesięczna (mld PLN)"), title_text=t(f"Monthly Transaction Value — {scenario}", f"Miesięczna Wartość Transakcji — {scenario}"),
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with st.expander(t("Activity assumptions per user/month", "Zalozenia aktywnosci na uzytkownika/miesiac")):
        st.json(models["assumptions"]["activity_params"])

    st.divider()

    # ── MODEL 3: CANNIBALIZATION ──
    st.subheader(t("Model 3: BLIK Cannibalization vs Net New Volume", "Model 3: Kanibalizacja BLIK vs Nowy Wolumen Netto"))
    st.caption(t("How much QR Pay volume is taken from BLIK vs genuinely new card transaction volume?",
                  "Ile wolumenu QR Pay jest przejete od BLIK vs faktycznie nowy wolumen transakcji kartowych?"))

    cn = models["cannibalization"][scenario]
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(cn["net_new_monthly"])/1e6,
                                 name=t("Net new to Visa (from cash/transfer)", "Nowe netto dla Visa (z gotówki/przelewów)"), fill="tozeroy",
                                 line=dict(color=ACCENT[2]), fillcolor="rgba(46,204,113,0.3)"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(cn["from_blik_monthly"])/1e6,
                                 name=t("Cannibalized from BLIK", "Skanibalizowane z BLIK"), fill="tozeroy",
                                 line=dict(color=BLIK_PINK), fillcolor="rgba(212,14,106,0.2)"))
        fig.update_layout(height=400, yaxis_title=t("Monthly value (M PLN)", "Wartość miesięczna (M PLN)"), title_text=t(f"Source of QR Pay Volume — {scenario}", f"Źródło Wolumenu QR Pay — {scenario}"),
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Pie at month 36
        net_new_36 = cn["net_new_monthly"][35]
        blik_36 = cn["from_blik_monthly"][35]
        existing_36 = cn["from_existing_card"][35]
        fig = px.pie(names=[t("Net new (cash/transfer → card)", "Nowe netto (gotówka/przelew → karta)"), t("From BLIK", "Z BLIK"), t("From existing card", "Z istniejącej karty")],
                     values=[net_new_36, blik_36, existing_36],
                     color_discrete_sequence=[ACCENT[2], BLIK_PINK, ACCENT[0]], hole=0.35,
                     title=t(f"Volume Source at Month 36 — {scenario}", f"Źródło Wolumenu w Miesiącu 36 — {scenario}"))
        fig.update_layout(height=400, margin=dict(t=40,b=30))
        st.plotly_chart(fig, use_container_width=True)

    net_new_pct = cn["net_new_pct"][35]
    if lang == "EN":
        st.info(f"**{scenario} scenario at Month 36:** {net_new_pct:.0f}% of QR Pay volume is NET NEW to the card ecosystem (from cash/transfers). {100-net_new_pct:.0f}% is cannibalized from BLIK or existing card channels.")
    else:
        st.info(f"**Scenariusz {scenario} w Miesiącu 36:** {net_new_pct:.0f}% wolumenu QR Pay to NOWE NETTO dla ekosystemu kartowego (z gotówki/przelewów). {100-net_new_pct:.0f}% jest skanibalizowane z BLIK lub istniejących kanałów kartowych.")

    st.divider()

    # ── MODEL 4: REVENUE & ROI ──
    st.subheader(t("Model 4: Revenue & ROI Projection", "Model 4: Prognoza Przychodu i ROI"))

    rv = models["revenue"][scenario]
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["cumulative_revenue"])/1e6,
                                 name=t("Cumulative Revenue", "Skumulowany Przychód"), line=dict(color=ACCENT[2], width=3), fill="tozeroy", fillcolor="rgba(46,204,113,0.15)"))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["cumulative_costs"])/1e6,
                                 name=t("Cumulative Costs", "Skumulowane Koszty"), line=dict(color=ACCENT[1], width=3, dash="dash")))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["cumulative_profit"])/1e6,
                                 name=t("Cumulative Profit", "Skumulowany Zysk"), line=dict(color=VISA_BLUE, width=3)))
        if rv["breakeven_month"]:
            fig.add_vline(x=rv["breakeven_month"]-1, line_dash="dot", line_color=VISA_GOLD,
                          annotation_text=t(f"Break-even: M{rv['breakeven_month']}", f"Punkt rentowności: M{rv['breakeven_month']}"))
        fig.update_layout(height=400, yaxis_title=t("PLN (millions)", "PLN (mln)"), title_text=t(f"Cumulative P&L — {scenario}", f"Skumulowany P&L — {scenario}"),
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["p2p_rev"])/1e6,
                                 name=t("P2P revenue", "Przychód P2P"), fill="tonexty", stackgroup="one", line=dict(color=ACCENT[0])))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["ecom_rev"])/1e6,
                                 name=t("E-commerce revenue", "Przychód e-commerce"), fill="tonexty", stackgroup="one", line=dict(color=ACCENT[3])))
        fig.add_trace(go.Scatter(x=months_labels, y=np.array(rv["svc_rev"])/1e6,
                                 name=t("Services revenue", "Przychód z usług"), fill="tonexty", stackgroup="one", line=dict(color=ACCENT[2])))
        fig.update_layout(height=400, yaxis_title=t("Monthly revenue (M PLN)", "Przychód miesięczny (M PLN)"), title_text=t(f"Revenue by Channel — {scenario}", f"Przychód wg Kanału — {scenario}"),
                          legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with st.expander(t("Cost breakdown", "Rozkład kosztów")):
        st.json(models["costs"])

    st.divider()

    # ── MODEL 5: E-COMMERCE MARKET SHARE ──
    st.subheader(t("Model 5: E-Commerce Market Share Simulation", "Model 5: Symulacja Udzialu w Rynku E-Commerce"))
    st.caption(t("How QR Pay changes Visa's share of the Polish e-commerce payments market",
                  "Jak QR Pay zmienia udzial Visa w polskim rynku płatności e-commerce"))

    es = models["ecom_share"][scenario]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months_labels, y=es["visa_share_pct"], name=t("Visa total (card + QR Pay)", "Visa łącznie (karta + QR Pay)"),
                             line=dict(color=VISA_BLUE, width=3)))
    fig.add_trace(go.Scatter(x=months_labels, y=es["visa_base_share"], name=t("Visa baseline (without QR Pay)", "Visa bazowo (bez QR Pay)"),
                             line=dict(color=VISA_BLUE, width=1.5, dash="dot")))
    fig.add_trace(go.Scatter(x=months_labels, y=es["blik_share_pct"], name=t("BLIK (adjusted)", "BLIK (skorygowany)"),
                             line=dict(color=BLIK_PINK, width=3)))
    fig.add_hline(y=es["visa_base_share"][0], line_dash="dash", line_color="#ccc",
                  annotation_text=t(f"Current Visa e-com share: {es['visa_base_share'][0]:.1f}%", f"Obecny udział Visa e-com: {es['visa_base_share'][0]:.1f}%"))
    fig.update_layout(height=450, yaxis_title=t("Market share (%)", "Udział rynkowy (%)"), title_text=t(f"E-Commerce Payment Share — {scenario}", f"Udział w Płatnościach E-Commerce — {scenario}"),
                      legend=dict(orientation="h",y=-0.12), margin=dict(t=40,b=40))
    st.plotly_chart(fig, use_container_width=True)

    visa_start = es["visa_share_pct"][0]
    visa_end = es["visa_share_pct"][35]
    blik_start = es["blik_share_pct"][0]
    blik_end = es["blik_share_pct"][35]
    if lang == "EN":
        st.success(f"**{scenario}:** Visa e-commerce share moves from **{visa_start:.1f}%** to **{visa_end:.1f}%** (+{visa_end-visa_start:.1f}pp). BLIK declines from **{blik_start:.1f}%** to **{blik_end:.1f}%** ({blik_end-blik_start:+.1f}pp).")
    else:
        st.success(f"**{scenario}:** Udział Visa w e-commerce rośnie z **{visa_start:.1f}%** do **{visa_end:.1f}%** (+{visa_end-visa_start:.1f}pp). BLIK spada z **{blik_start:.1f}%** do **{blik_end:.1f}%** ({blik_end-blik_start:+.1f}pp).")

    st.divider()

    # ── MODEL 6: SENSITIVITY ──
    st.subheader(t("Model 6: Sensitivity Analysis", "Model 6: Analiza Wrazliwosci"))
    st.caption(t("How 3-year revenue changes when we vary each key parameter ±50% from base",
                  "Jak zmienia sie 3-letni przychod gdy modyfikujemy kazdy kluczowy parametr ±50% od bazy"))

    sens = pd.DataFrame(models["sensitivity"])
    base_rev = sens[(sens["parameter"]==sens["parameter"].iloc[0]) & (sens["multiplier"]==1.0)]["revenue_3yr_mln"].values[0]

    param_choice = st.selectbox(t("Select parameter:", "Wybierz parametr:"), sens["parameter"].unique())
    df_p = sens[sens["parameter"] == param_choice]

    fig = go.Figure()
    colors_bar = df_p["multiplier"].apply(lambda m: VISA_BLUE if m == 1.0 else (ACCENT[2] if m > 1 else ACCENT[1]))
    fig.add_trace(go.Bar(x=df_p["multiplier"].apply(lambda m: f"{m:.0%}"), y=df_p["revenue_3yr_mln"],
                         marker_color=colors_bar.tolist(), text=df_p["revenue_3yr_mln"].apply(lambda v: f"{v:.0f}M"),
                         textposition="outside"))
    fig.add_hline(y=base_rev, line_dash="dash", line_color=VISA_GOLD, annotation_text=t(f"Base: {base_rev:.0f}M PLN", f"Baza: {base_rev:.0f}M PLN"))
    fig.update_layout(height=400, yaxis_title=t("3-year revenue (M PLN)", "Przychód 3-letni (M PLN)"),
                      xaxis_title=t(f"{param_choice} (multiplier vs base)", f"{param_choice} (mnożnik vs baza)"),
                      title_text=t(f"Sensitivity: {param_choice}", f"Wrażliwość: {param_choice}"), margin=dict(t=40,b=40))
    st.plotly_chart(fig, use_container_width=True)

    # Tornado chart
    st.subheader(t("Tornado Chart: Revenue Sensitivity to All Parameters", "Wykres Tornado: Wrazliwosc Przychodu na Wszystkie Parametry"))
    tornado = []
    for param in sens["parameter"].unique():
        df_param = sens[sens["parameter"] == param]
        low = df_param[df_param["multiplier"] == 0.5]["revenue_3yr_mln"].values[0]
        high = df_param[df_param["multiplier"] == 1.5]["revenue_3yr_mln"].values[0]
        base = df_param[df_param["multiplier"] == 1.0]["revenue_3yr_mln"].values[0]
        tornado.append({"Parameter": param, "Low (50%)": low - base, "High (150%)": high - base, "Range": high - low})

    df_torn = pd.DataFrame(tornado).sort_values("Range", ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(y=df_torn["Parameter"], x=df_torn["Low (50%)"], name=t("50% of base", "50% bazy"),
                         orientation="h", marker_color=ACCENT[1]))
    fig.add_trace(go.Bar(y=df_torn["Parameter"], x=df_torn["High (150%)"], name=t("150% of base", "150% bazy"),
                         orientation="h", marker_color=ACCENT[2]))
    fig.update_layout(height=400, xaxis_title=t("Impact on 3Y revenue (M PLN vs base)", "Wpływ na przychód 3L (M PLN vs baza)"),
                      barmode="overlay", title_text=t("Tornado: Which Parameters Matter Most", "Tornado: Które Parametry Mają Największe Znaczenie"),
                      legend=dict(orientation="h",y=-0.15), margin=dict(t=40,b=40))
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── SCENARIO COMPARISON TABLE ──
    st.subheader(t("Scenario Comparison Summary", "Porównanie Scenariuszy"))
    comp_data = []
    for name in ["Conservative", "Base", "Optimistic"]:
        a = models["adoption"][name]
        v = models["volume"][name]
        r = models["revenue"][name]
        cn = models["cannibalization"][name]
        if lang == "EN":
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
        else:
            comp_data.append({
                "Scenariusz": name,
                "Użytkownicy 3L": f"{a['cumulative'][35]/1e6:.1f}M",
                "Penetracja 3L": f"{a['penetration_pct'][35]:.0f}%",
                "Mies. TX 3L": f"{v['total_tx_monthly'][35]/1e6:.1f}M",
                "Mies. Wartość 3L": f"{v['total_val_monthly'][35]/1e9:.1f} mld PLN",
                "Przychód 3L": f"{r['total_3yr_revenue']/1e6:.0f}M PLN",
                "Zysk 3L": f"{r['total_3yr_profit']/1e6:.0f}M PLN",
                "ROI": f"{r['roi_pct']:.0f}%",
                "Punkt rentowności": f"Miesiąc {r['breakeven_month']}" if r["breakeven_month"] else "Nie osiągnięty",
                "Nowe netto %": f"{cn['net_new_pct'][35]:.0f}%",
            })
    st.dataframe(pd.DataFrame(comp_data), use_container_width=True, hide_index=True)
