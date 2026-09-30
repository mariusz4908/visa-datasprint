"""Page: Who First — ML Targeting."""
import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app_pages.common import DATA_DIR, load_json, source, t, VISA_BLUE, VISA_GOLD, BLIK_PINK, ACCENT


def render():
    ml_results = {"target_audiences.json": "target_audiences.ipynb", "readiness_model.json": "readiness_model.ipynb"}
    missing = [nb for f, nb in ml_results.items()
               if not os.path.exists(os.path.join(DATA_DIR, "ml_readiness", "results", f))]
    if missing:
        st.warning(t("ML results not found. Run these notebooks in `ml_readiness/` first: ",
                     "Brak wyników ML. Najpierw uruchom notatniki w `ml_readiness/`: ") + ", ".join(missing))
        st.stop()
    aud_data = load_json(os.path.join("ml_readiness", "results", "target_audiences.json"))
    model_data = load_json(os.path.join("ml_readiness", "results", "readiness_model.json"))

    st.header(t("Who First — ML Targeting for Visa QR Pay", "Kto pierwszy — targetowanie ML dla Visa QR Pay"))
    st.caption(t("Card behaviour Jan–Jun 2026 · readiness model trained and validated on Visa data · "
                 "all figures aggregated to groups of 30+ cards",
                 "Zachowania kart sty–cze 2026 · model gotowości uczony i walidowany na danych Visa · "
                 "wszystkie liczby dla grup min. 30 kart"))

    intro = t("QR Pay removes the typed card number. Three data-driven tools decide who gets it first: "
              "a <strong>data rule</strong> finds cards that type their number today, "
              "<strong>new cards</strong> get QR at issuance, and a <strong>machine-learning model</strong> "
              "finds the never-online cards that are about to make their first online payment.",
              "QR Pay eliminuje przepisywanie numeru karty. O tym, kto dostanie go pierwszy, decydują trzy narzędzia "
              "oparte na danych: <strong>reguła z danych</strong> wskazuje karty, które dziś przepisują numer, "
              "<strong>nowe karty</strong> dostają QR przy wydaniu, a <strong>model uczenia maszynowego</strong> "
              "znajduje karty bez zakupów online, które zaraz dokonają pierwszej płatności online.")
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #E8F0FE, #D0E0FF); padding: 20px 24px; border-radius: 14px; border-left: 5px solid #1A1F71;">
        <p style="margin:0; font-size:1em; color:#0D1137;">{intro}</p>
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
    new_typed = roi["new_cards"]["first_online_payment_typed"]
    new_per_month = roi["new_cards"]["per_month_avg"] / 1000
    k1.metric(t("Wave 1 · mostly typing", "Fala 1 · głównie przepisują"),
              t(f"{a.cards / 1000:.0f}K cards", f"{a.cards / 1000:.0f} tys. kart"),
              t(f"{a.share_of_typed_tx:.0%} of all typed online payments",
                f"{a.share_of_typed_tx:.0%} wszystkich przepisanych płatności online"), delta_color="off")
    k2.metric(t("From issuance · new cards", "Od wydania · nowe karty"),
              t(f"{new_per_month:.0f}K / month", f"{new_per_month:.0f} tys. / mies."),
              t(f"{new_typed:.0%} of first online payments typed",
                f"{new_typed:.0%} pierwszych płatności online przepisanych"), delta_color="off")
    k3.metric(t("Wave 2 · ready (ML)", "Fala 2 · gotowi (ML)"),
              t(f"{c.cards / 1000:.0f}K cards", f"{c.cards / 1000:.0f} tys. kart"),
              t(f"~{c.expected_starters_3m / 1000:.1f}K first online payments in 3 months",
                f"~{c.expected_starters_3m / 1000:.1f} tys. pierwszych płatności online w 3 mies."), delta_color="off")
    k4.metric(t("Model accuracy (AUC)", "Trafność modelu (AUC)"), f"{final['AUC']:.2f}",
              t(f"top 20% of cards = {top20_reach:.0f}% of starters", f"20% kart = {top20_reach:.0f}% startujących"),
              delta_color="off")
    source("visa_ml")

    tab_aud, tab_model, tab_personas, tab_new = st.tabs(
        [t("Audiences", "Grupy"), t("Readiness model", "Model gotowości"), t("Personas", "Persony"),
         t("New cards", "Nowe karty")])

    # ── Audiences ──
    with tab_aud:
        roles = {
            "A mostly typing": t("Wave 1 — QR in the banking app replaces typing", "Fala 1 — QR w aplikacji banku zastępuje przepisywanie"),
            "C ready to start": t("Wave 2 — QR at the first online payment (ML model)", "Fala 2 — QR przy pierwszej płatności online (model ML)"),
            "D sometimes typing": t("Wave 3", "Fala 3"),
            "E not ready": t("Not targeted", "Poza kampanią"),
            "F never typing": t("Not targeted — already one-click", "Poza kampanią — już płacą jednym kliknięciem"),
            "L lapsed": t("Not targeted", "Poza kampanią"),
        }
        tbl = aud.reset_index()
        tbl["Role"] = tbl.audience.map(roles)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(t("Active cards per audience", "Aktywne karty w grupach"))
            fig = px.bar(tbl.sort_values("audience", ascending=False), x="cards", y="audience", orientation="h",
                         color="audience", color_discrete_sequence=[VISA_BLUE, VISA_GOLD, ACCENT[0], "#bbb", "#999", "#ccc"])
            fig.update_layout(height=320, margin=dict(t=10, b=30), showlegend=False, xaxis_title=t("cards", "karty"), yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.subheader(t("Share of typed online card payments", "Udział w przepisanych płatnościach online"))
            fig = px.bar(tbl.sort_values("audience", ascending=False), x="share_of_typed_tx", y="audience",
                         orientation="h", color_discrete_sequence=[BLIK_PINK])
            fig.update_layout(height=320, margin=dict(t=10, b=30), xaxis_tickformat=".0%", xaxis_title="", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        source("visa_ml")

        st.dataframe(pd.DataFrame({
            t("Audience", "Grupa"): tbl.audience,
            t("Cards", "Karty"): tbl.cards.map("{:,.0f}".format),
            t("Share of active cards", "Udział aktywnych kart"): tbl.share_of_cards.map("{:.0%}".format),
            t("Typed payments / card / month", "Przepisane płatności / karta / mies."):
                tbl.typed_tx_per_card_month.map("{:.1f}".format),
            t("Mostly pay by phone in store", "Głównie telefon w sklepie"): tbl.mostly_wallet_share.map("{:.0%}".format),
            t("Role", "Rola"): tbl.Role,
        }), hide_index=True, use_container_width=True)

        st.divider()
        st.subheader(t("Wave 1: where do typers type their card number?", "Fala 1: gdzie przepisują numer karty?"))
        cats = pd.DataFrame(aud_data["audience_a_categories"]).head(10)
        device = aud_data["audience_a_device_typed_tx"]
        phone_share = device["phone"] / (device["phone"] + device["computer_other"])
        dec = pd.DataFrame(aud_data["audience_a_deciles"])
        col1, col2 = st.columns([3, 2])
        with col1:
            fig = px.bar(cats.sort_values("share_of_a_typed_pct"), x="share_of_a_typed_pct", y="category",
                         orientation="h", color="polish_merchant_pct", color_continuous_scale="Blues",
                         labels={"share_of_a_typed_pct": t("% of their typed payments", "% ich przepisanych płatności"), "category": "",
                                 "polish_merchant_pct": t("% Polish merchants", "% polskich sprzedawców")})
            fig.update_layout(height=380, margin=dict(t=10, b=30))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.metric(t("Typed payments made on a phone", "Przepisane płatności na telefonie"), f"{phone_share:.0%}")
            st.caption(t("QR Pay must work from the banking app / phone, not only from the plastic card.",
                          "QR Pay musi działać z aplikacji banku / telefonu, a nie tylko z plastikowej karty."))
            top20 = dec.loc[dec.group == "top 20%", "cum_share_of_typed_pct"].iloc[0]
            st.metric(t("Typing done by the heaviest 20% of typers", "Udział 20% najczęściej przepisujących"), f"{top20:.0f}%")
            st.caption(t("Contact order: start with the heaviest typers.",
                          "Kolejność kontaktu: najpierw ci, którzy przepisują najczęściej."))
            fig = go.Figure(go.Scatter(x=[0] + list(range(10, 101, 10)), y=[0] + dec.cum_share_of_typed_pct.tolist(),
                                       mode="lines+markers", line=dict(color=VISA_BLUE, width=3)))
            fig.add_trace(go.Scatter(x=[0, 100], y=[0, 100], mode="lines", line=dict(color="#bbb", dash="dash")))
            fig.update_layout(height=220, margin=dict(t=10, b=30), showlegend=False,
                              xaxis_title=t("% of typers contacted", "% kontaktowanych"),
                              yaxis_title=t("% of typing covered", "% objętych przepisanych płatności"))
            st.plotly_chart(fig, use_container_width=True)
        source("visa_ml")

    # ── Readiness model ──
    with tab_model:
        st.markdown(t(f"""
        **What it does:** for every card that has never paid online, it estimates the chance of a first online card
        payment in the next 3 months, using only in-store behaviour (LightGBM, calibrated).

        **How well:** tested on three later periods it never saw. On the final test ({final['period']},
        {final['cards']:,} cards, {final['start_rate']:.1%} start) the top 10% of cards start
        **{final['lift top 10%']:.1f}×** more often than average and the top 20% contain
        **{top20_reach:.0f}%** of all future starters.
        """, f"""
        **Co robi:** dla każdej karty, która nigdy nie płaciła online, szacuje szansę pierwszej płatności kartą online
        w ciągu 3 miesięcy, wyłącznie na podstawie zachowań w sklepach (LightGBM, skalibrowany).

        **Jak dobrze:** sprawdzony na trzech późniejszych okresach, których nie widział. Na teście końcowym
        ({final['period']}, {final['cards']:,} kart, {final['start_rate']:.1%} startuje) 10% kart z najwyższą oceną
        zaczyna **{final['lift top 10%']:.1f}×** częściej niż średnia, a 20% kart zawiera **{top20_reach:.0f}%**
        wszystkich przyszłych startujących.
        """))
        bt = pd.DataFrame(model_data["backtest"])
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(t("Backtest: AUC by test period", "Test wsteczny: AUC w okresach testowych"))
            fig = px.bar(bt, x="test snapshot", y="AUC", color="model", barmode="group",
                         color_discrete_sequence=["#bbb", ACCENT[0], VISA_BLUE])
            fig.update_layout(height=340, margin=dict(t=10, b=30), yaxis_range=[0.5, 0.8], xaxis_title="",
                              legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.subheader(t("Gains: reach of future starters", "Ilu przyszłych startujących obejmujemy"))
            fig = go.Figure(go.Scatter(x=[0] + gains.contacted_pct.tolist(), y=[0] + gains.starters_reached_pct.tolist(),
                                       mode="lines+markers", name="model", line=dict(color=VISA_BLUE, width=3)))
            fig.add_trace(go.Scatter(x=[0, 100], y=[0, 100], mode="lines", name="random",
                                     line=dict(color="#bbb", dash="dash")))
            fig.update_layout(height=340, margin=dict(t=10, b=30), xaxis_title=t("% of cards contacted", "% kontaktowanych kart"),
                              yaxis_title=t("% of starters reached", "% osiągniętych startujących"), legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig, use_container_width=True)
        source("visa_ml", note=("LightGBM readiness model, rolling backtest on later periods",
                                "model gotowości LightGBM, test wsteczny na późniejszych okresach"))

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
            st.subheader(t("What predicts a first online payment", "Co przewiduje pierwszą płatność online"))
            fig = px.bar(drv.sort_values("mean_abs_shap"), x="mean_abs_shap", y="label", orientation="h", color="effect",
                         color_discrete_map={"more → more likely": "#2ECC71", "more → less likely": "#E74C3C",
                                             "mixed": "#bbb"},
                         labels={"mean_abs_shap": "impact (mean |SHAP|)", "label": ""})
            fig.update_layout(height=420, margin=dict(t=10, b=30), legend=dict(orientation="h", y=-0.15))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.subheader(t("Calibration", "Kalibracja"))
            cal = pd.DataFrame(model_data["calibration_deciles"])
            fig = go.Figure()
            fig.add_trace(go.Bar(x=cal.decile, y=cal.actual * 100, name="actual", marker_color=VISA_BLUE))
            fig.add_trace(go.Scatter(x=cal.decile, y=cal.calibrated * 100, name="predicted", mode="lines+markers",
                                     line=dict(color=VISA_GOLD, width=3)))
            fig.update_layout(height=420, margin=dict(t=10, b=30), xaxis_title="score decile (10 = highest)",
                              yaxis_title="start rate (%)", legend=dict(orientation="h", y=-0.15))
            st.plotly_chart(fig, use_container_width=True)
        source("visa_ml", note=("LightGBM readiness model, rolling backtest on later periods",
                                "model gotowości LightGBM, test wsteczny na późniejszych okresach"))
        st.info(t("The model predicts who is **about to** start paying online — the moment QR Pay should take over. "
                  "What QR itself adds is measured in the pilot with a random control group (~10% of each audience).",
                  "Model przewiduje, kto **zaraz** zacznie płacić online — to moment, który powinien przejąć QR Pay. "
                  "Efekt samego QR mierzymy w pilotażu z losową grupą kontrolną (~10% każdej grupy)."))

    # ── Personas ──
    with tab_personas:
        st.markdown(t("Six behavioural personas from **in-store behaviour only** (KMeans). The model finds ready cards "
                      "even inside low-adoption personas, which persona targeting alone would miss.",
                      "Sześć person zbudowanych **wyłącznie z zachowań w sklepach** (KMeans). Model znajduje gotowe karty "
                      "nawet w personach o niskiej adopcji, które samo targetowanie po personach by pominęło."))
        per = pd.DataFrame(model_data["personas"])
        fig = go.Figure()
        fig.add_trace(go.Bar(x=per.persona, y=per.actual_start_pct, name=t("all cards in persona", "wszystkie karty persony"), marker_color="#bbb"))
        fig.add_trace(go.Bar(x=per.persona, y=per.top10_start_pct, name=t("model's top 10% inside persona", "top 10% modelu w personie"),
                             marker_color=VISA_BLUE))
        fig.update_layout(height=380, barmode="group", margin=dict(t=10, b=30), yaxis_title=t("start within 3 months (%)", "start w 3 mies. (%)"),
                          legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig, use_container_width=True)
        mix = pd.DataFrame(aud_data["audience_persona_cards"])
        mix = mix[mix.audience.isin(["A mostly typing", "C ready to start", "E not ready"])]
        mix["share"] = mix.cards / mix.groupby("audience").cards.transform("sum")
        fig = px.bar(mix, x="share", y="audience", color="persona", orientation="h",
                     color_discrete_sequence=ACCENT, labels={"share": "share of audience", "audience": ""})
        fig.update_layout(height=260, margin=dict(t=10, b=30), xaxis_tickformat=".0%", legend=dict(orientation="h", y=-0.3))
        st.subheader(t("Persona mix of the audiences", "Skład person w grupach"))
        st.plotly_chart(fig, use_container_width=True)
        source("visa_ml", note=("KMeans personas from in-store behaviour", "persony KMeans z zachowań w sklepach"))

    # ── New cards ──
    with tab_new:
        coh = pd.DataFrame(aud_data["new_card_cohorts"])
        coh["month"] = coh.cohort_m.apply(lambda m: f"{2025 + m // 12}-{m % 12 + 1:02d}")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(t("New cards per month", "Nowe karty miesięcznie"))
            fig = px.bar(coh, x="month", y="cards", color_discrete_sequence=[VISA_BLUE])
            fig.update_layout(height=340, margin=dict(t=10, b=30), xaxis_title="", yaxis_title=t("cards", "karty"))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.subheader(t("What new cards do", "Co robią nowe karty"))
            fig = go.Figure()
            for col, name, color in [("wallet_first_month", t("phone in store, 1st month", "telefon w sklepie, 1. miesiąc"), ACCENT[0]),
                                     ("online_within_3m", t("online within 3 months", "online w ciągu 3 miesięcy"), VISA_BLUE),
                                     ("first_online_typed", t("first online payment typed", "pierwsza płatność online przepisana"), BLIK_PINK)]:
                fig.add_trace(go.Scatter(x=coh.month, y=coh[col] * 100, name=name, mode="lines+markers",
                                         line=dict(color=color, width=3)))
            fig.update_layout(height=340, margin=dict(t=10, b=30), yaxis_title="%", legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig, use_container_width=True)
        source("visa_ml")
        st.success(t(f"About half of new cards pay online within 3 months, and **{new_typed:.0%} of those first "
                     "online payments are typed**. QR on every new card makes the first online payment effortless — "
                     "the cheapest way to scale.",
                     f"Około połowa nowych kart płaci online w ciągu 3 miesięcy, a **{new_typed:.0%} tych pierwszych "
                     "płatności online to przepisany numer**. QR na każdej nowej karcie sprawia, że pierwsza płatność "
                     "online jest bez wysiłku — to najtańsza droga do skali."))
