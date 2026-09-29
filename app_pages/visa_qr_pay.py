"""Page: Visa QR Pay — Our Solution."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from app_pages.common import t, VISA_BLUE, ACCENT


def render():
    lang = st.session_state.get("lang", "EN")

    if lang == "EN":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8EDF8, #D0D9F0); padding: 44px 36px; border-radius: 18px; color: #1A1F71; margin-bottom: 28px; border: 2px solid #B0BDE0;">
            <h1 style="margin:0; font-size:2.4em; color:#0D1137;">Visa QR Pay</h1>
            <p style="color:#333; font-size:1.15em; margin-top:8px;">Your card is your identity. One scan — and the payment comes to you.</p>
            <p style="color:#555; font-size:0.95em; margin-top:4px;">A new payment paradigm: instead of entering card details, you scan a QR code on your physical card. The payment request comes to your phone. You approve or decline — that's it.</p>
            <span style="background:#F7B600; color:#0D1137; padding:5px 20px; border-radius:16px; font-weight:700; font-size:0.85em;">OUR PROPOSED SOLUTION</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8EDF8, #D0D9F0); padding: 44px 36px; border-radius: 18px; color: #1A1F71; margin-bottom: 28px; border: 2px solid #B0BDE0;">
            <h1 style="margin:0; font-size:2.4em; color:#0D1137;">Visa QR Pay</h1>
            <p style="color:#333; font-size:1.15em; margin-top:8px;">Twoja karta to Twoja tożsamość. Jedno skanowanie — i płatność przychodzi do Ciebie.</p>
            <p style="color:#555; font-size:0.95em; margin-top:4px;">Nowy paradygmat płatności: zamiast wpisywać dane karty, skanujesz kod QR na fizycznej karcie. Żądanie płatności pojawia sie na Twoim telefonie. Zatwierdzasz lub odrzucasz — to wszystko.</p>
            <span style="background:#F7B600; color:#0D1137; padding:5px 20px; border-radius:16px; font-weight:700; font-size:0.85em;">NASZE ROZWIĄZANIE</span>
        </div>
        """, unsafe_allow_html=True)

    # ── THE PROBLEM ──
    st.header(t("The Problem We're Solving", "Problem Który Rozwiązujemy"))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.error(t("""
        **🛒 Online Checkout Friction**

        Typing a 16-digit card number, expiry date, and CVV is the #1 reason people abandon cards online.
        In Poland, **67% choose BLIK** instead — because it's one code, one tap.

        *Cards lose not on trust, but on convenience.*
        """, """
        **🛒 Tarcie przy Platnosci Online**

        Wpisywanie 16-cyfrowego numeru karty, daty waznosci i CVV to powod nr 1, dla ktorego ludzie rezygnuja z kart online.
        W Polsce **67% wybiera BLIK** — bo to jeden kod, jedno klikniecie.

        *Karty przegrywaja nie na zaufaniu, lecz na wygodzie.*
        """))
    with col2:
        st.error(t("""
        **🤝 P2P Payments: Cards Don't Exist**

        Splitting a dinner bill, paying for a marketplace item, collecting for a group gift —
        cards are invisible here. **BLIK P2P owns 55%**, bank transfers 40%, cards ~2%.

        *There's no card-native way to request money from someone.*
        """, """
        **🤝 Płatności P2P: Karty Nie Istnieja**

        Dzielenie rachunku za kolację, płatność za przedmiot z marketplace, zbiórka na prezent —
        karty sa tu niewidoczne. **BLIK P2P ma 55%**, przelewy 40%, karty ~2%.

        *Nie ma natywnego sposobu, by karta poprosic kogos o pieniadze.*
        """))
    with col3:
        st.error(t("""
        **🔢 The Number Problem**

        Your card number is sensitive data. Every time you type it, there's a risk.
        Every time you share it, you worry. Every new website = another place your card data lives.

        *What if you never had to type your card number again?*
        """, """
        **🔢 Problem Numeru Karty**

        Numer Twojej karty to wrazliwe dane. Za kazdym razem, gdy go wpisujesz, ryzykujesz.
        Za kazdym razem, gdy go udostepniasz, martwisz sie. Kazda nowa strona = kolejne miejsce z danymi Twojej karty.

        *A gdybys nigdy więcej nie musiał wpisywać numeru karty?*
        """))

    st.divider()

    # ── THE SOLUTION ──
    st.header(t("The Solution: Visa QR Pay", "Rozwiązanie: Visa QR Pay"))
    st.markdown(t("""
    > **Every Visa card gets a unique QR code** — printed on the card, available in the banking app, or on a sticker.
    > Scanning this QR code doesn't reveal the card number. It creates a **secure payment request channel**
    > between the payer and the cardholder.
    """, """
    > **Kazda karta Visa otrzymuje unikalny kod QR** — wydrukowany na karcie, dostepny w aplikacji bankowej lub jako naklejka.
    > Skanowanie tego kodu QR nie ujawnia numeru karty. Tworzy **bezpieczny kanał żądania płatności**
    > między płacącym a posiadaczem karty.
    """))

    st.divider()

    # ── TWO MODES ──
    tab1, tab2 = st.tabs([t("💰 Mode 1: P2P — Request Payment", "💰 Tryb 1: P2P — Zadanie Platnosci"),
                           t("🛒 Mode 2: E-Commerce — Scan to Pay", "🛒 Tryb 2: E-Commerce — Skanuj i Plac")])

    with tab1:
        if lang == "EN":
            st.markdown("""
            <div style="background: linear-gradient(135deg, #E8F0FE, #D0E0FF); padding: 28px; border-radius: 16px; margin-bottom: 20px;">
                <h2 style="color: #1A1F71; margin:0;">Mode 1: P2P Payment Request</h2>
                <p style="color: #333; margin-top:8px; font-size:1.05em;">Someone owes you money? They scan your card's QR code and send you a payment — instantly, by card.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #E8F0FE, #D0E0FF); padding: 28px; border-radius: 16px; margin-bottom: 20px;">
                <h2 style="color: #1A1F71; margin:0;">Tryb 1: Zadanie Płatności P2P</h2>
                <p style="color: #333; margin-top:8px; font-size:1.05em;">Ktos jest Ci winien pieniadze? Skanuje kod QR Twojej karty i wysyla Ci platnosc — natychmiast, karta.</p>
            </div>
            """, unsafe_allow_html=True)

        st.subheader(t("How It Works", "Jak To Działa"))

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">📱</div>
                <h4 style="color:#1A1F71;">Step 1: Scan</h4>
                <p style="font-size:0.9em; color:#666;">Your friend scans the QR code on your Visa card using their phone camera</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">💲</div>
                <h4 style="color:#1A1F71;">Step 2: Enter Amount</h4>
                <p style="font-size:0.9em; color:#666;">They type the amount, add a short description (e.g. "dinner split"), and confirm</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">🔔</div>
                <h4 style="color:#1A1F71;">Step 3: You Get a Request</h4>
                <p style="font-size:0.9em; color:#666;">A push notification appears on your phone: "Adam wants to pay you 45 PLN — dinner split"</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">✅</div>
                <h4 style="color:#1A1F71;">Step 4: Approve or Decline</h4>
                <p style="font-size:0.9em; color:#666;">You review the request and tap Approve. The money moves via Visa Direct — instantly to your card.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        st.subheader(t("Use Cases", "Przypadki Użycia"))
        uc1, uc2, uc3, uc4 = st.columns(4)
        with uc1:
            st.info(t("**🍕 Split the bill**\n\nScan the card of whoever paid, enter your share. No IBAN, no phone number needed.",
                       "**🍕 Podziel rachunek**\n\nZeskanuj kartę osoby, która płaciła, wpisz swoją część. Bez IBAN, bez numeru telefonu."))
        with uc2:
            st.info(t("**🏪 Marketplace sale**\n\nSelling on OLX? Buyer scans your card QR at meetup. Instant card-to-card payment.",
                       "**🏪 Sprzedaż na marketplace**\n\nSprzedajesz na OLX? Kupujący skanuje Twój QR przy spotkaniu. Natychmiastowa płatność kartą-do-karty."))
        with uc3:
            st.info(t("**🎁 Group collection**\n\nOrganizing a gift? Share your card QR in the group chat. Everyone scans & pays.",
                       "**🎁 Zbiórka grupowa**\n\nOrganizujesz prezent? Udostępnij QR karty na czacie grupowym. Każdy skanuje i płaci."))
        with uc4:
            st.info(t("**🔧 Pay the plumber**\n\nNo terminal needed. The tradesman shows their card, you scan and pay. Done.",
                       "**🔧 Zapłać hydraulikowi**\n\nBez terminala. Fachowiec pokazuje swoją kartę, skanujesz i płacisz. Gotowe."))

        st.success(t("""
        **Why this changes the game:**
        - **No card number shared** — the QR contains a tokenized identifier, not the actual card number
        - **Works offline** — the QR is printed on the physical card, no internet needed to initiate
        - **Pull → Push model** — the *receiver* doesn't pull money; the *sender* pushes a request that must be approved
        - **Powered by Visa Direct** — instant settlement, 24/7, to any Visa card globally
        - **Directly competes with BLIK P2P** — but works across borders and doesn't require the same bank
        """, """
        **Dlaczego to zmienia gre:**
        - **Brak udostepniania numeru karty** — QR zawiera tokenizowany identyfikator, nie rzeczywisty numer karty
        - **Dziala offline** — QR jest wydrukowany na fizycznej karcie, nie potrzeba internetu do rozpoczecia
        - **Model Pull → Push** — *odbiorca* nie ściąga pieniędzy; *nadawca* wysyla zadanie, które musi być zatwierdzone
        - **Napedzane przez Visa Direct** — natychmiastowe rozliczenie, 24/7, na dowolna karte Visa na swiecie
        - **Bezposrednia konkurencja z BLIK P2P** — ale dziala transgranicznie i nie wymaga tego samego banku
        """))

    with tab2:
        if lang == "EN":
            st.markdown("""
            <div style="background: linear-gradient(135deg, #FFF3E0, #FFE0B2); padding: 28px; border-radius: 16px; margin-bottom: 20px;">
                <h2 style="color: #1A1F71; margin:0;">Mode 2: E-Commerce — Scan Your Card to Pay</h2>
                <p style="color: #333; margin-top:8px; font-size:1.05em;">Instead of typing your card number at checkout, scan your own card's QR with your phone or laptop webcam. The payment request appears on your phone — approve it and you're done.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #FFF3E0, #FFE0B2); padding: 28px; border-radius: 16px; margin-bottom: 20px;">
                <h2 style="color: #1A1F71; margin:0;">Tryb 2: E-Commerce — Zeskanuj Karte i Zaplac</h2>
                <p style="color: #333; margin-top:8px; font-size:1.05em;">Zamiast wpisywac numer karty przy kasie, zeskanuj QR swojej karty telefonem lub kamerka laptopa. Żądanie płatności pojawia sie na telefonie — zatwierdz i gotowe.</p>
            </div>
            """, unsafe_allow_html=True)

        st.subheader(t("How It Works", "Jak To Działa"))

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">🛒</div>
                <h4 style="color:#1A1F71;">Step 1: Checkout</h4>
                <p style="font-size:0.9em; color:#666;">At any online store, choose "Visa QR Pay" as your payment method</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">📷</div>
                <h4 style="color:#1A1F71;">Step 2: Scan Your Card</h4>
                <p style="font-size:0.9em; color:#666;">Hold your Visa card's QR code up to your phone camera or laptop webcam</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">🔔</div>
                <h4 style="color:#1A1F71;">Step 3: Approve on Phone</h4>
                <p style="font-size:0.9em; color:#666;">A push notification: "Allegro — 289 PLN — headphones". You verify and approve with biometrics.</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <div style="font-size:2.5em; margin-bottom:12px;">🎉</div>
                <h4 style="color:#1A1F71;">Step 4: Done</h4>
                <p style="font-size:0.9em; color:#666;">Payment confirmed. No card number typed. No 3DS redirect. Faster than BLIK.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        st.subheader(t("Why This Beats Current Methods", "Dlaczego To Bije Obecne Metody"))

        comp = pd.DataFrame([
            {"Step": "Select payment method", "Traditional Card": "Choose 'card'", "BLIK": "Choose 'BLIK'", "Visa QR Pay": "Choose 'Visa QR Pay'"},
            {"Step": "Identify yourself", "Traditional Card": "Type 16-digit card number + expiry + CVV", "BLIK": "Open bank app, copy 6-digit code", "Visa QR Pay": "Scan QR on your card (1 second)"},
            {"Step": "Authenticate", "Traditional Card": "3D Secure redirect → bank app → confirm", "BLIK": "Confirm in bank app", "Visa QR Pay": "Approve push notification (biometric)"},
            {"Step": "Total steps", "Traditional Card": "5-7 steps, 30-60 seconds", "BLIK": "3-4 steps, 15-20 seconds", "Visa QR Pay": "2-3 steps, 5-10 seconds"},
            {"Step": "Card number exposed?", "Traditional Card": "Yes — typed into website", "BLIK": "No (different system)", "Visa QR Pay": "No — only tokenized ID transmitted"},
            {"Step": "Works internationally?", "Traditional Card": "Yes", "BLIK": "No (Poland only)", "Visa QR Pay": "Yes (any Visa-accepting merchant)"},
            {"Step": "Works on laptop without phone?", "Traditional Card": "Yes (but must type number)", "BLIK": "No (requires phone app)", "Visa QR Pay": "Yes (laptop webcam scans QR)"},
        ])
        st.dataframe(comp, use_container_width=True, hide_index=True)

        st.success(t("""
        **The key advantage over BLIK:** Visa QR Pay is **faster** (scan vs. type 6-digit code), **more secure**
        (no card data shared, tokenized), **global** (works on any Visa-accepting website worldwide), and uses
        **biometric approval** (Face ID / fingerprint) instead of manually confirming in the bank app.
        """, """
        **Kluczowa przewaga nad BLIK:** Visa QR Pay jest **szybszy** (skan vs. wpisywanie 6-cyfrowego kodu), **bezpieczniejszy**
        (brak udostepniania danych karty, tokenizacja), **globalny** (dziala na kazdej stronie akceptujacej Visa na swiecie) i korzysta z
        **zatwierdzenia biometrycznego** (Face ID / odcisk palca) zamiast ręcznego potwierdzania w aplikacji bankowej.
        """))

    st.divider()

    # ── DATA-BACKED OPPORTUNITY ──
    st.header(t("Data-Backed: Why This Solution Addresses Real Gaps", "Dane Potwierdzaja: Dlaczego To Rozwiazanie Adresuje Realne Luki"))

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Gaps Addressed by Visa QR Pay", "Luki Adresowane przez Visa QR Pay"))
        gaps = pd.DataFrame([
            {"Gap": "P2P payments (cards = 2%)", "Current Winner": "BLIK (55%)", "QR Pay Impact": "Direct competitor — scan card to send money", "TAM": "~280B PLN/year"},
            {"Gap": "E-commerce checkout friction", "Current Winner": "BLIK (67%)", "QR Pay Impact": "Faster than BLIK: scan vs type code", "TAM": "~65B PLN/year"},
            {"Gap": "Cash services (plumber, tutor)", "Current Winner": "Cash (90%+)", "QR Pay Impact": "No terminal needed — just show your card", "TAM": "~50B PLN/year"},
            {"Gap": "Marketplace payments (OLX)", "Current Winner": "BLIK/Transfer", "QR Pay Impact": "Instant card-to-card at meetup", "TAM": "~15B PLN/year"},
            {"Gap": "Group collections", "Current Winner": "BLIK/Transfer", "QR Pay Impact": "Share QR in chat, everyone scans & pays", "TAM": "~5B PLN/year"},
            {"Gap": "International online shopping", "Current Winner": "Card (but friction)", "QR Pay Impact": "Scan & approve — no number entry on foreign sites", "TAM": "~20B PLN/year"},
        ])
        st.dataframe(gaps, use_container_width=True, hide_index=True)

    with col2:
        st.subheader(t("Total Addressable Market", "Calkowity Rynek Docelowy"))
        fig = go.Figure(go.Funnel(
            y=["P2P Payments", "Domestic E-Commerce", "Cash Services", "International E-Com", "Marketplace P2P", "Group Collections"],
            x=[280, 65, 50, 20, 15, 5],
            textinfo="value+text",
            text=["280B PLN", "65B PLN", "50B PLN", "20B PLN", "15B PLN", "5B PLN"],
            marker=dict(color=[VISA_BLUE, ACCENT[0], ACCENT[1], ACCENT[3], ACCENT[4], ACCENT[5]]),
        ))
        fig.update_layout(height=400, margin=dict(t=10,b=10), title_text="Estimated Annual Volume (PLN)")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── TECHNICAL ARCHITECTURE ──
    st.header(t("Technical Concept", "Koncepcja Techniczna"))

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### QR Code Structure
        ```
        visa://pay?token=VQR_8f3a...c7d2&ver=1
        ```

        The QR code on the card contains:
        - **Tokenized card identifier** (not the actual card number)
        - **Version flag** for future extensibility
        - **No sensitive data** — the token is meaningless without Visa's backend

        ### Security Model
        | Layer | Protection |
        |---|---|
        | QR Content | Tokenized ID only — no PAN, no CVV |
        | Request creation | Requires payer's authenticated session |
        | Approval | Push notification + biometric (Face ID / fingerprint) |
        | Transaction | Processed via Visa Direct — full Visa security & fraud detection |
        | Disputes | Full Visa chargeback protection applies |
        | Token revocation | Card owner can revoke/regenerate QR token anytime in bank app |
        """)

    with col2:
        st.markdown("""
        ### Flow Diagram

        **P2P Mode:**
        ```
        [Payer's Phone]          [Visa Cloud]          [Recipient's Phone]
             |                        |                        |
             |--- Scan QR code ------>|                        |
             |--- Enter amount ------>|                        |
             |                        |--- Push notification ->|
             |                        |    "Adam: 45 PLN       |
             |                        |     dinner split"      |
             |                        |                        |
             |                        |<--- APPROVE (biometric)|
             |                        |                        |
             |<-- Confirmation -------|------- Funds moved --->|
             |    "Payment sent"      |    via Visa Direct     |
        ```

        **E-Commerce Mode:**
        ```
        [Merchant Website]       [Visa Cloud]          [Your Phone]
             |                        |                        |
             |--- Initiate payment -->|                        |
             |                        |                        |
        [You scan your card QR with phone/webcam]              |
             |--- Token sent -------->|                        |
             |                        |--- Push notification ->|
             |                        |    "Allegro: 289 PLN   |
             |                        |     headphones"        |
             |                        |<--- APPROVE (biometric)|
             |<-- Payment confirmed --|                        |
             |    "Order placed!"     |                        |
        ```
        """)

    st.divider()

    # ── COMPETITIVE ADVANTAGE ──
    st.header(t("Competitive Advantage vs BLIK", "Przewaga Konkurencyjna vs BLIK"))

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #E8F0FE, #D4E2F9); padding:24px; border-radius:14px; border:2px solid #A8C4E8; color:#1F2937;">
            <h3 style="color:#1A1F71;">Why Visa QR Pay wins over BLIK:</h3>
            <ul style="font-size:0.95em; color:#1F2937;">
                <li><strong style="color:#0D1137;">No app needed to initiate</strong> — anyone with a camera can scan a QR code. BLIK requires the bank app open.</li>
                <li><strong style="color:#0D1137;">Physical card = always available</strong> — dead phone? Low battery? Your card QR still works for P2P.</li>
                <li><strong style="color:#0D1137;">Global reach</strong> — works on any Visa merchant worldwide. BLIK = Poland only.</li>
                <li><strong style="color:#0D1137;">One identity across all channels</strong> — same QR for P2P, e-commerce, in-person services.</li>
                <li><strong style="color:#0D1137;">No 6-digit code to mistype</strong> — scan is instant and error-free.</li>
                <li><strong style="color:#0D1137;">Biometric approval</strong> — Face ID / fingerprint vs. manually opening the app and confirming.</li>
                <li><strong style="color:#0D1137;">Works on laptop</strong> — webcam scans the QR for desktop e-commerce. BLIK always needs a phone.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #FFF3E0, #FFE8CC); padding:24px; border-radius:14px; border:2px solid #FFCC80; color:#3E2723;">
            <h3 style="color:#E65100;">What BLIK still does well:</h3>
            <ul style="font-size:0.95em; color:#3E2723;">
                <li><strong style="color:#4E342E;">Deeply integrated in Polish banks</strong> — 95% of mobile banking users have BLIK.</li>
                <li><strong style="color:#4E342E;">No physical card needed at all</strong> — pure digital, works with phone only.</li>
                <li><strong style="color:#4E342E;">ATM withdrawals</strong> — BLIK can withdraw cash without a card.</li>
                <li><strong style="color:#4E342E;">Brand trust in Poland</strong> — "BLIK" is almost a verb ("I'll BLIK you").</li>
            </ul>
            <br/>
            <h3 style="color:#E65100;">Visa QR Pay response:</h3>
            <ul style="font-size:0.95em; color:#3E2723;">
                <li>QR also available <strong style="color:#4E342E;">in banking app</strong> (digital card) — not just physical</li>
                <li>Partner with Polish banks to add <strong style="color:#4E342E;">"Visa QR Pay" button</strong> next to BLIK</li>
                <li>Leverage existing <strong style="color:#4E342E;">1.95M Visa cards</strong> in Poland — zero new issuance needed</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── ROLLOUT PLAN ──
    st.header(t("Proposed Rollout", "Proponowany Plan Wdrozenia"))

    phases = pd.DataFrame([
        {"Phase": "Phase 1 (0-3 months)", "Action": "Pilot with 2-3 Polish banks — QR in mobile banking app", "Target": "P2P payments between bank customers", "KPI": "10K active QR payers"},
        {"Phase": "Phase 2 (3-6 months)", "Action": "QR stickers sent to all Visa cardholders by mail", "Target": "P2P + marketplace (OLX, Vinted)", "KPI": "100K active QR payers"},
        {"Phase": "Phase 3 (6-12 months)", "Action": "Merchant SDK — 'Visa QR Pay' button at checkout", "Target": "Top 50 Polish e-commerce sites", "KPI": "1M online QR transactions/month"},
        {"Phase": "Phase 4 (12-18 months)", "Action": "QR printed on all new Visa cards in Poland", "Target": "Full market — P2P, e-com, services", "KPI": "5% of e-commerce share (from ~9%)"},
        {"Phase": "Phase 5 (18-24 months)", "Action": "International rollout — EU, then global", "Target": "Cross-border P2P & e-commerce", "KPI": "Pan-European Visa QR standard"},
    ])
    st.dataframe(phases, use_container_width=True, hide_index=True)

    st.divider()

    # ── IMPACT ESTIMATION ──
    st.header(t("Projected Impact", "Prognozowany Wplyw"))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(t("P2P market capture target", "Cel przejecia rynku P2P"), "10%", help=t("Of BLIK's 55% P2P share → ~28B PLN/year", "Z 55% udzialu BLIK P2P → ~28B PLN/rok"))
        st.metric(t("New annual card P2P volume", "Nowy roczny wolumen P2P kart"), "~28B PLN")
    with col2:
        st.metric(t("E-commerce share gain", "Wzrost udzialu e-commerce"), "+3-5pp", help=t("From ~9% to 12-14% of e-commerce", "Z ~9% do 12-14% e-commerce"))
        st.metric(t("New annual e-com volume", "Nowy roczny wolumen e-com"), "~3-4B PLN")
    with col3:
        st.metric(t("Cash services converted", "Konwersja usług gotówkowych"), "5-10%", help=t("Of ~50B PLN cash service economy", "Z ~50B PLN gospodarki usług gotówkowych"))
        st.metric(t("New annual service volume", "Nowy roczny wolumen uslug"), "~3-5B PLN")

    if lang == "EN":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8F8F0, #D5F5E3); padding: 20px 24px; border-radius: 14px; border-left: 4px solid #2ECC71; margin-top: 20px; color: #1A3C2A;">
            <h3 style="color:#1B7A3D; margin:0 0 8px 0;">Combined Potential: ~35B PLN in new annual card transaction volume</h3>
            <p style="margin:0; color:#1A3C2A;">By turning every Visa card into a payment acceptance point (via QR), we transform cards from a "spending tool"
            into a <strong style="color:#145A24;">universal payment platform</strong> — competing with BLIK on convenience while leveraging Visa's global infrastructure,
            security, and buyer protection that BLIK cannot match.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8F8F0, #D5F5E3); padding: 20px 24px; border-radius: 14px; border-left: 4px solid #2ECC71; margin-top: 20px; color: #1A3C2A;">
            <h3 style="color:#1B7A3D; margin:0 0 8px 0;">Laczny Potencjal: ~35B PLN nowego rocznego wolumenu transakcji kartowych</h3>
            <p style="margin:0; color:#1A3C2A;">Zamieniajac kazda karte Visa w punkt akceptacji platnosci (przez QR), transformujemy karty z "narzedzia wydatkow"
            w <strong style="color:#145A24;">uniwersalna platforme platnicza</strong> — konkurujac z BLIK na wygodzie, jednoczesnie wykorzystujac globalna infrastrukture Visa,
            bezpieczenstwo i ochronę kupującego, których BLIK nie może zapewnić.</p>
        </div>
        """, unsafe_allow_html=True)
