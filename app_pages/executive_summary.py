"""Page: Executive Summary."""
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app_pages.common import VISA_BLUE, BLIK_PINK, ACCENT


def render():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0D1137, #1A1F71, #2A3090); padding: 40px 32px; border-radius: 16px; color: white; margin-bottom: 24px;">
        <h1 style="margin:0; font-size:2.2em;">CardFlow</h1>
        <p style="opacity:0.9; font-size:1.1em; margin-top:4px;">Transaction data as a roadmap for card adoption in e-commerce & P2P payments</p>
        <span style="background:#F7B600; color:#0D1137; padding:4px 16px; border-radius:16px; font-weight:700; font-size:0.85em;">VISA DATASPRINT HACKATHON 2026</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    > **Payment cards dominate in physical stores, but in e-commerce and peer-to-peer transactions they are being displaced
    > by other methods.** In Poland, BLIK, fast transfers, and cash are the main alternatives. Users choose them because
    > they're faster, don't require typing a card number, and feel more secure. The same person pays by card at a local
    > shop but uses a different method online or when paying a friend.
    >
    > **CardFlow** uses anonymized, aggregated transaction data to understand *when, where, and why* the card stops being
    > the first choice. We analyze behavioral patterns by merchant category, time of day, basket value, and location.
    > We identify **"escape points"** — moments where customers switch payment methods.
    """)

    st.divider()

    # KPIs
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Transactions", "305.5M", help="Total in sample dataset")
    c2.metric("Unique Cards", "1.95M", help="Unique card identifiers")
    c3.metric("Total Value", "55.7B", help="Fictional currency units")
    c4.metric("Avg Transaction", "182.30", help="Average transaction value")
    c5.metric("Online Share (TX)", "11.2%", delta="+1.4pp YoY")
    c6.metric("Online Share (Value)", "19.6%", help="Online = higher avg value")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("The Polish Payment Landscape")
        fig = go.Figure()
        years = ["2019", "2020", "2021", "2022", "2023", "2024"]
        fig.add_trace(go.Scatter(x=years, y=[44,50,53,55,57,58], name="Card at POS (%)", line=dict(color=VISA_BLUE, width=3)))
        fig.add_trace(go.Scatter(x=years, y=[54,47,43,40,37,35], name="Cash at POS (%)", line=dict(color=ACCENT[1], width=3, dash="dash")))
        fig.add_trace(go.Scatter(x=years, y=[5,10,15,22,30,42], name="BLIK tx (×100M)", line=dict(color=BLIK_PINK, width=3)))
        fig.update_layout(height=350, margin=dict(t=10,b=30), legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("E-Commerce Payment Methods 2024")
        fig = px.pie(
            names=["BLIK (67%)", "Card (16%)", "Bank Transfer (10%)", "Cash on Delivery (5%)", "Other (2%)"],
            values=[67, 16, 10, 5, 2],
            color_discrete_sequence=[BLIK_PINK, VISA_BLUE, ACCENT[0], ACCENT[3], "#ccc"],
            hole=0.4,
        )
        fig.update_layout(height=350, margin=dict(t=10,b=30))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Key Findings at a Glance")
    f1, f2, f3 = st.columns(3)
    with f1:
        st.error("**BLIK Threat:** 67% of e-commerce and growing +5pp/year. Cards fell from 20% to 16% in 2 years.")
    with f2:
        st.warning("**Card-Free Zones:** Housing (20.6% of spending), telecom (4.0%), education (1.1%) have <1% card penetration.")
    with f3:
        st.success("**Visa's Moat:** Subscriptions (Apple, Netflix, Spotify) + international e-commerce = ~8M tx locked on card rails.")

    f4, f5, f6 = st.columns(3)
    with f4:
        st.info("**E-Grocery Gap:** 26% of card tx are grocery but only 0.12% online. Online avg = 3.1x higher value.")
    with f5:
        st.error("**Cash Services:** Doctors (255K tx), dentists (76K), home repair (31K) — cash dominates services.")
    with f6:
        st.success("**Recurring Power:** 4.1% of card-merchant pairs generate 42.8% of transactions and 36.5% of value.")

    st.divider()

    st.markdown("""
    <div style="background: linear-gradient(135deg, #E8F0FE, #D0E0FF); padding: 24px 28px; border-radius: 14px; border-left: 5px solid #1A1F71;">
        <h3 style="color:#1A1F71; margin:0 0 8px 0;">💡 Our Proposed Solution: Visa QR Pay</h3>
        <p style="margin:0; font-size:1em;">
        A QR code on every Visa card that enables <strong>two new payment flows</strong>:
        (1) <strong>P2P payments</strong> — scan someone's card to send them money, competing directly with BLIK P2P;
        (2) <strong>E-commerce checkout</strong> — scan your own card instead of typing the number, faster and safer than any existing method.
        No card number shared, biometric approval, powered by Visa Direct.
        </p>
        <p style="margin:8px 0 0 0; font-size:0.9em; color:#555;">👈 Navigate to <strong>"Visa QR Pay — Our Solution"</strong> in the sidebar for the full concept.</p>
    </div>
    """, unsafe_allow_html=True)
