"""Page: Innovation Portfolio."""
import streamlit as st

from app_pages.common import t


def render():
    lang = st.session_state.get("lang", "EN")

    st.header(t("Visa Marketplace Shield — Escrow for P2P Commerce", "Visa Marketplace Shield — Escrow dla Handlu P2P"))
    st.caption(t("Card-powered escrow for marketplace transactions — backed by data gaps in our analysis",
                  "Escrow napedzany kartami dla transakcji marketplace — poparty lukami w naszej analizie"))
    st.subheader(t("3. Visa Marketplace Shield — Escrow for P2P Commerce", "3. Visa Marketplace Shield — Escrow dla Handlu P2P"))

    col1, col2 = st.columns([2, 1])
    with col1:
        if lang == "EN":
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
        else:
            st.markdown("""
            **Luka:** Transakcje marketplace (OLX, Vinted, Facebook Marketplace) = ~15 mld PLN/rok. Obecnie płacone przez
            BLIK P2P lub przelew — **bez żadnej ochrony kupującego**. Oszustwa są powszechne. Karty nie są używane, bo
            nie ma natywnego kartowego mechanizmu dla handlu osoby-z-osobą.

            **Rozwiązanie:** Escrow napędzany kartami dla transakcji marketplace:

            **Dla Kupujących:**
            1. Przy spotkaniu lub online zeskanuj kod QR Visa sprzedającego
            2. Wpisz kwotę + opis przedmiotu + zrób zdjęcie
            3. Pieniądze są **przechowywane w escrow Visa** (pobrane z karty kupującego)
            4. Kupujący potwierdza odbiór w ciągu 48h → pieniądze zwolnione do sprzedającego
            5. Spór? Uruchamia się **pełna ochrona chargeback Visa**

            **Dla Sprzedających:**
            - Gwarantowana płatność (bez zwróconych przelewów, bez fałszywych BLIK)
            - Pieniądze na karcie Visa w ciągu 24h od potwierdzenia kupującego
            - Reputacja sprzedającego buduje się z czasem

            **Kluczowa przewaga nad BLIK P2P:** Przelew BLIK jest natychmiastowy i nieodwracalny — jeśli zostaniesz oszukany, pieniądze przepadły.
            Visa Marketplace Shield przechowuje środki, aż obie strony będą zadowolone. **Zaufanie = wyróżnik.**
            """)

    with col2:
        if lang == "EN":
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
        else:
            st.markdown("""
            <div style="background:#E8F5E9; padding:20px; border-radius:12px; border:2px solid #A5D6A7; color:#1A3C2A;">
                <h4 style="color:#2E7D32; margin:0 0 12px 0;">Szacowany Wpływ</h4>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">TAM:</strong> ~15 mld PLN/rok</p>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Użytkownicy OLX:</strong> ~14M w Polsce</p>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Użytkownicy Vinted:</strong> ~5M w Polsce</p>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Średnia tx marketplace:</strong> 120 PLN</p>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Docelowe przejęcie:</strong> 10-15%</p>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Nowy wolumen kartowy:</strong> 1.5-2.3 mld PLN/rok</p>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Opłata escrow:</strong> 1-2% (płacona przez kupującego za ochronę)</p>
                <hr style="border-color:#A5D6A7;"/>
                <p style="margin:4px 0; color:#1A3C2A;"><strong style="color:#145A24;">Źródło danych:</strong></p>
                <p style="margin:2px 0; font-size:0.85em; color:#2E5A3A;">Dane Visa: Vinted 352K tx, Allegro 1.8M tx już na kartach. Ogromny niewykorzystany wolumen OLX/FB Marketplace.</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    st.subheader(t("Synergy: QR Pay + Marketplace Shield", "Synergia: QR Pay + Marketplace Shield"))

    if lang == "EN":
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
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8F5E9, #C8E6C9); padding: 20px 24px; border-radius: 14px; border-left: 4px solid #43A047; color:#1A3C2A;">
            <h4 style="color:#1B5E20; margin:0 0 8px 0;">Dwa rozwiązania, jeden ekosystem</h4>
            <p style="color:#1A3C2A; margin:0;"><strong style="color:#145A24;">Visa QR Pay</strong> zapewnia warstwę tożsamości (zeskanuj kartę, by zainicjować płatność).
            <strong style="color:#145A24;">Marketplace Shield</strong> dodaje warstwę zaufania (escrow + ochrona kupującego).
            Razem tworzą kompletne rozwiązanie handlu P2P, którego BLIK nie może dorównać:
            natychmiastowa identyfikacja przez QR + gwarantowana bezpieczna transakcja przez escrow + pełna ochrona chargeback Visa.
            To zamienia każdą kartę Visa zarówno w <strong style="color:#145A24;">narzędzie płatnicze</strong>, jak i <strong style="color:#145A24;">odznakę zaufania</strong>.</p>
        </div>
        """, unsafe_allow_html=True)
