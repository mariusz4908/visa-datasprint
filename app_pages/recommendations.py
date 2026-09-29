"""Page: Recommendations."""
import pandas as pd
import streamlit as st



def render():
    st.header("Strategic Recommendations")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0D1137, #1A1F71); padding: 24px 28px; border-radius: 14px; color: white; margin-bottom: 20px;">
        <h3 style="margin:0; color:#F7B600;">CardFlow — From Cash & Transfer to Card</h3>
        <p style="opacity:0.9; margin-top:6px;">We turn transaction data into concrete decisions. We show not just how people pay,
        but what to do to make the card their most convenient choice — online and in private payments.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("For Three Target Audiences")

    tab1, tab2, tab3 = st.tabs(["🛍️ Online Merchants", "🏦 Banks & Visa", "🏙️ Cities & Municipalities"])

    with tab1:
        st.markdown("""
        ### Online Merchants: Reduce Friction, Increase Card Share

        | Escape Point Identified | Recommendation | Expected Impact |
        |---|---|---|
        | **67% of e-commerce uses BLIK** because it's one-click | Implement **Visa Click to Pay** — tokenized one-click card payment | +3-5pp card share |
        | **E-grocery at 0.12%** online | Launch card-first checkout for grocery delivery (Frisco, Barbora) | Avg online basket 3.1× higher |
        | **Online avg = 318 vs 165 physical** | Promote card for high-value online purchases (electronics, furniture) | Higher revenue per TX |
        | **Clothing online: 5% of TX, 16% of value** | Card-on-file + saved checkout for fashion e-commerce | Lock in repeat buyers |
        | **COD still 5% of e-commerce** | Offer "Pay now with card, get free shipping" incentive | Convert COD → card |
        | **BLIK lacks chargeback protection** | Highlight Visa buyer protection for expensive purchases | Trust advantage for >200 PLN |

        **Quick Win:** Partner with Allegro (1.8M card TX already) to make Visa Click to Pay as prominent as BLIK at checkout.
        """)

    with tab2:
        st.markdown("""
        ### Banks & Visa: Activate Cards in New Channels

        | Segment | Current State | Visa Direct / Card Opportunity |
        |---|---|---|
        | **P2P payments** | BLIK 55%, card ~2% | **Visa Direct** for instant P2P — "split the bill by card" |
        | **Subscriptions** | 282K cards on Netflix, 240K on Apple | Promote card-on-file for ALL subscriptions (telecom, insurance) |
        | **Recurring bills** | 3% card, 90% transfer/direct debit | Card-linked bill payment with **2% cashback** incentive |
        | **Ages 65+** | 72% cash preference | Simplified contactless card for seniors + education |
        | **Ages 45-64** | 40% cash | "Your card works online too" campaign |
        | **Micro-payments <10 PLN** | 65% cash | Zero-fee contactless under 10 PLN for merchants |
        | **ATM heavy users** | Avg 1,521/withdrawal | Identify & target with "why withdraw when you can tap?" |

        **Quick Win:** Launch "Visa Split" — P2P card-to-card transfers integrated in banking apps, competing directly with BLIK P2P.

        **Visa Direct opportunity:** 14.5M households paying 416 PLN/month in rent + 68 PLN telecom = **7B PLN/month** in potential card-linked payments.
        """)

    with tab3:
        st.markdown("""
        ### Cities & Municipalities: Cashless Local Economy

        | Urban Challenge | Data Insight | Solution |
        |---|---|---|
        | **Open-air markets** | 15% terminal coverage | **Tap-to-Phone** program for market vendors (zero cost) |
        | **Local transport** | 3.8M tx, but 1M via apps only | Contactless card validators on all buses/trams |
        | **Parking** | 2.8M tx at meters/garages | Universal card-tap parking meters |
        | **Municipal fees** | 60% terminal coverage | Online card payment portal for all city services |
        | **Local events/festivals** | Cash-heavy by tradition | Cashless event wristbands linked to Visa |
        | **Food trucks & street food** | 50% terminal coverage | SumUp/Zettle micro-POS deployment program |
        | **Public institutions** | 60% terminals | Card payment kiosks in offices |

        **Case Study Potential:** Partner with one Polish city (e.g., Kraków — highest card mobility at 17.7%)
        for a **"Cashless City" pilot** — measure impact on local commerce, tax revenue visibility, and tourist spending.
        """)

    st.divider()
    st.subheader("Priority Matrix")

    priorities = pd.DataFrame([
        {"Initiative": "Visa Click to Pay at top merchants", "Impact": "High", "Effort": "Medium", "Timeline": "3-6 months", "Target": "Merchants"},
        {"Initiative": "E-grocery card-first checkout", "Impact": "High", "Effort": "Medium", "Timeline": "3-6 months", "Target": "Merchants"},
        {"Initiative": "Tap-to-Phone for service providers", "Impact": "High", "Effort": "Low", "Timeline": "1-3 months", "Target": "Visa/Banks"},
        {"Initiative": "Visa Direct P2P in banking apps", "Impact": "Very High", "Effort": "High", "Timeline": "6-12 months", "Target": "Banks"},
        {"Initiative": "Card-on-file for recurring bills", "Impact": "Very High", "Effort": "High", "Timeline": "6-12 months", "Target": "Banks"},
        {"Initiative": "Zero-fee micro-payments", "Impact": "Medium", "Effort": "Low", "Timeline": "1-3 months", "Target": "Visa"},
        {"Initiative": "Cashless City pilot", "Impact": "High", "Effort": "High", "Timeline": "6-12 months", "Target": "Cities"},
        {"Initiative": "Senior contactless education", "Impact": "Medium", "Effort": "Low", "Timeline": "1-3 months", "Target": "Banks"},
    ])
    st.dataframe(priorities, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFF9E6, #FFF3CC); padding: 20px 24px; border-radius: 14px; border-left: 4px solid #F7B600;">
        <h3 style="color:#0D1137; margin:0 0 8px 0;">The Bottom Line</h3>
        <p style="margin:0; font-size:1.05em;">
        Cards already dominate physical POS (58% and growing). But <strong>~25% of household spending</strong> (housing, telecom, education)
        is invisible to cards, and in e-commerce <strong>BLIK has captured 67%</strong>. The opportunity is not to fight BLIK head-on
        in domestic one-click payments, but to <strong>own the niches where cards have structural advantages</strong>:
        international commerce, subscriptions, high-value purchases with buyer protection, P2P via Visa Direct,
        and the untapped recurring bills market. Combined, these represent <strong>tens of billions of PLN in annual payment volume</strong>
        currently flowing through non-card channels.
        </p>
    </div>
    """, unsafe_allow_html=True)
