"""Page: Innovation Portfolio."""
import streamlit as st

from app_pages.common import t


def render():
    st.header(t("Visa Marketplace Shield — Escrow for P2P Commerce", "Visa Marketplace Shield — Escrow dla Handlu P2P"))
    st.caption(t("Card-powered escrow for marketplace transactions — backed by data gaps in our analysis",
                  "Escrow napedzany kartami dla transakcji marketplace — poparty lukami w naszej analizie"))
    st.subheader(t("3. Visa Marketplace Shield — Escrow for P2P Commerce", "3. Visa Marketplace Shield — Escrow dla Handlu P2P"))

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **The Gap:** Marketplace transactions (OLX, Vinted, Facebook Marketplace) = ~15B PLN/year. Currently paid by
        BLIK P2P or bank transfer — **with zero buyer protection**. Scams are common. Cards are not used because
        there's no card-native mechanism for person-to-person commerce.

        **The Solution:** Card-powered escrow for marketplace transactions:

        **For Buyers:**
        1. At meetup or online, scan seller's Visa QR code
        2. Enter amount + item description + take a photo
        3. Money is **held in Visa escrow** (charged to buyer's card)
        4. Buyer confirms receipt within 48h → money released to seller
        5. Dispute? **Full Visa chargeback protection** kicks in

        **For Sellers:**
        - Guaranteed payment (no bounced transfers, no fake BLIK)
        - Money arrives to Visa card within 24h of buyer confirmation
        - Seller reputation score builds over time

        **Key advantage over BLIK P2P:** BLIK transfer is instant and irreversible — if you get scammed, the money is gone.
        Visa Marketplace Shield holds funds until both parties are satisfied. **Trust = the differentiator.**
        """)

    with col2:
        st.markdown("""
        <div style="background:#E8F5E9; padding:20px; border-radius:12px; border:2px solid #A5D6A7; color:#1A3C2A;">
            <h4 style="color:#2E7D32; margin:0 0 12px 0;">Impact Estimate</h4>
            <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">TAM:</strong> ~15B PLN/year</p>
            <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">OLX users:</strong> ~14M in Poland</p>
            <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Vinted users:</strong> ~5M in Poland</p>
            <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Avg marketplace tx:</strong> 120 PLN</p>
            <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Target capture:</strong> 10-15%</p>
            <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">New card volume:</strong> 1.5-2.3B PLN/yr</p>
            <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Escrow fee:</strong> 1-2% (paid by buyer for protection)</p>
            <hr style="border-color:#A5D6A7;"/>
            <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Data source:</strong></p>
            <p style="margin:2px 0; font-size:0.85em; color:#2E5A3A;">Visa data: Vinted 352K tx, Allegro 1.8M tx already on cards. Massive untapped OLX/FB Marketplace volume.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader(t("Synergy: QR Pay + Marketplace Shield", "Synergia: QR Pay + Marketplace Shield"))

    st.markdown("""
    <div style="background: linear-gradient(135deg, #E8F5E9, #C8E6C9); padding: 20px 24px; border-radius: 14px; border-left: 4px solid #43A047; color:#1A3C2A;">
        <h4 style="color:#1B5E20; margin:0 0 8px 0;">Two solutions, one ecosystem</h4>
        <p style="color:#1A3C2A; margin:0;"><strong style="color:#145A24;">Visa QR Pay</strong> provides the identity layer (scan a card to initiate payment).
        <strong style="color:#145A24;">Marketplace Shield</strong> adds the trust layer (escrow + buyer protection).
        Together they create a complete P2P commerce solution that BLIK cannot match:
        instant identification via QR + guaranteed safe transaction via escrow + full Visa chargeback protection.
        This transforms every Visa card into both a <strong style="color:#145A24;">payment tool</strong> and a <strong style="color:#145A24;">trust badge</strong>.</p>
    </div>
    """, unsafe_allow_html=True)
