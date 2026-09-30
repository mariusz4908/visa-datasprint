"""Page: Visa QR Pay — Our Solution."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from app_pages.common import source, t, VISA_BLUE, ACCENT


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
            <p style="color:#555; font-size:0.95em; margin-top:4px;">Nowy sposób płacenia: zamiast wpisywać dane karty, skanujesz kod QR na fizycznej karcie. Prośba o płatność pojawia się na Twoim telefonie. Zatwierdzasz lub odrzucasz — to wszystko.</p>
            <span style="background:#F7B600; color:#0D1137; padding:5px 20px; border-radius:16px; font-weight:700; font-size:0.85em;">NASZE ROZWIĄZANIE</span>
        </div>
        """, unsafe_allow_html=True)

    # ── THE PROBLEM ──
    st.header(t("The Problem We're Solving", "Problem, który rozwiązujemy"))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.error(t("""
        **Online Checkout Friction**

        Typing a 16-digit card number, expiry date, and CVV is the #1 reason people abandon cards online.
        In Poland, **67% choose BLIK** instead — because it's one code, one tap.

        *Cards lose not on trust, but on convenience.*
        """, """
        **Uciążliwa płatność online**

        Wpisywanie 16-cyfrowego numeru karty, daty ważności i CVV to główny powód, dla którego ludzie rezygnują z kart online.
        W Polsce **67% wybiera BLIK** — bo to jeden kod, jedno kliknięcie.

        *Karty nie przegrywają zaufaniem, tylko wygodą.*
        """))
    with col2:
        st.error(t("""
        **P2P Payments: Cards Don't Exist**

        Splitting a dinner bill, paying for a marketplace item, collecting for a group gift —
        cards are invisible here. **BLIK P2P owns 55%**, bank transfers 40%, cards ~2%.

        *There's no card-native way to request money from someone.*
        """, """
        **Płatności P2P: tu kart nie ma**

        Dzielenie rachunku za kolację, płatność za przedmiot z marketplace, zbiórka na prezent —
        karty są tu niewidoczne. **BLIK P2P ma 55%**, przelewy 40%, karty ~2%.

        *Kartą nie da się dziś po prostu poprosić kogoś o pieniądze.*
        """))
    with col3:
        st.error(t("""
        **The Number Problem**

        Your card number is sensitive data. Every time you type it, there's a risk.
        Every time you share it, you worry. Every new website = another place your card data lives.

        *What if you never had to type your card number again?*
        """, """
        **Problem numeru karty**

        Numer Twojej karty to wrażliwe dane. Za każdym razem, gdy go wpisujesz, ryzykujesz.
        Za każdym razem, gdy go udostępniasz, martwisz się. Każda nowa strona = kolejne miejsce z danymi Twojej karty.

        *A gdybyś nigdy więcej nie musiał wpisywać numeru karty?*
        """))
    source("gemius", "nbp_survey", "blik", note=("shares of e-commerce and P2P payments in Poland", "udziały w e-commerce i płatnościach P2P w Polsce"))

    st.divider()

    # ── THE SOLUTION ──
    st.header(t("The Solution: Visa QR Pay", "Rozwiązanie: Visa QR Pay"))
    st.markdown(t("""
    > **Every Visa card gets a unique QR code** — printed on the card, available in the banking app, or on a sticker.
    > Scanning this QR code doesn't reveal the card number. It creates a **secure payment request channel**
    > between the payer and the cardholder.
    """, """
    > **Każda karta Visa dostaje unikalny kod QR** — wydrukowany na karcie, dostępny w aplikacji bankowej lub jako naklejka.
    > Skanowanie tego kodu QR nie ujawnia numeru karty. Tworzy **bezpieczny kanał prośby o płatność**
    > między płacącym a posiadaczem karty.
    """))

    st.divider()

    # ── TWO MODES ──
    tab1, tab2 = st.tabs([t("Mode 1: P2P — Request Payment", "Tryb 1: P2P — prośba o płatność"),
                           t("Mode 2: E-Commerce — Scan to Pay", "Tryb 2: e-commerce — zeskanuj i zapłać")])

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
                <h2 style="color: #1A1F71; margin:0;">Tryb 1: prośba o płatność P2P</h2>
                <p style="color: #333; margin-top:8px; font-size:1.05em;">Ktoś jest Ci winien pieniądze? Skanuje kod QR Twojej karty i wysyła Ci płatność — natychmiast, kartą.</p>
            </div>
            """, unsafe_allow_html=True)

        st.subheader(t("How It Works", "Jak to działa"))

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <h4 style="color:#1A1F71;">{t("Step 1: Scan", "Krok 1: Skanuj")}</h4>
                <p style="font-size:0.9em; color:#666;">{t("Your friend scans the QR code on your Visa card using their phone camera", "Twój znajomy skanuje kod QR na Twojej karcie Visa aparatem telefonu")}</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <h4 style="color:#1A1F71;">{t("Step 2: Enter Amount", "Krok 2: Wpisz kwotę")}</h4>
                <p style="font-size:0.9em; color:#666;">{t('They type the amount, add a short description (e.g. "dinner split"), and confirm', 'Wpisuje kwotę, dodaje krótki opis (np. „za kolację”) i potwierdza')}</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <h4 style="color:#1A1F71;">{t("Step 3: You Get a Request", "Krok 3: Dostajesz powiadomienie")}</h4>
                <p style="font-size:0.9em; color:#666;">{t('A push notification appears on your phone: "Adam wants to pay you 45 PLN — dinner split"', 'Na Twoim telefonie pojawia się powiadomienie push: „Adam chce Ci zapłacić 45 PLN — za kolację”')}</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <h4 style="color:#1A1F71;">{t("Step 4: Approve or Decline", "Krok 4: Zatwierdź lub odrzuć")}</h4>
                <p style="font-size:0.9em; color:#666;">{t("You review the request and tap Approve. The money moves via Visa Direct — instantly to your card.", "Sprawdzasz płatność i klikasz Zatwierdź. Pieniądze przechodzą przez Visa Direct — natychmiast na Twoją kartę.")}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        st.subheader(t("Use Cases", "Przykłady zastosowań"))
        uc1, uc2, uc3, uc4 = st.columns(4)
        with uc1:
            st.info(t("**Split the bill**\n\nScan the card of whoever paid, enter your share. No IBAN, no phone number needed.",
                       "**Podziel rachunek**\n\nZeskanuj kartę osoby, która płaciła, wpisz swoją część. Bez IBAN, bez numeru telefonu."))
        with uc2:
            st.info(t("**Marketplace sale**\n\nSelling on OLX? Buyer scans your card QR at meetup. Instant card-to-card payment.",
                       "**Sprzedaż na marketplace**\n\nSprzedajesz na OLX? Kupujący skanuje Twój QR przy spotkaniu. Natychmiastowa płatność kartą-do-karty."))
        with uc3:
            st.info(t("**Group collection**\n\nOrganizing a gift? Share your card QR in the group chat. Everyone scans & pays.",
                       "**Zbiórka grupowa**\n\nOrganizujesz prezent? Udostępnij QR karty na czacie grupowym. Każdy skanuje i płaci."))
        with uc4:
            st.info(t("**Pay the plumber**\n\nNo terminal needed. The tradesman shows their card, you scan and pay. Done.",
                       "**Zapłać hydraulikowi**\n\nBez terminala. Fachowiec pokazuje swoją kartę, skanujesz i płacisz. Gotowe."))

        st.success(t("""
        **Why this changes the game:**
        - **No card number shared** — the QR contains a tokenized identifier, not the actual card number
        - **Works offline** — the QR is printed on the physical card, no internet needed to initiate
        - **Pull → Push model** — the *receiver* doesn't pull money; the *sender* pushes a request that must be approved
        - **Powered by Visa Direct** — instant settlement, 24/7, to any Visa card globally
        - **Directly competes with BLIK P2P** — but works across borders and doesn't require the same bank
        """, """
        **Dlaczego to zmienia grę:**
        - **Bez udostępniania numeru karty** — QR zawiera tokenizowany identyfikator, nie rzeczywisty numer karty
        - **Działa offline** — QR jest wydrukowany na fizycznej karcie, do rozpoczęcia nie trzeba internetu
        - **Model Pull → Push** — *odbiorca* nie ściąga pieniędzy; *nadawca* wysyła prośbę, którą trzeba zatwierdzić
        - **Działa na Visa Direct** — natychmiastowe rozliczenie, 24/7, na dowolną kartę Visa na świecie
        - **Bezpośrednia konkurencja dla BLIK P2P** — ale działa transgranicznie i nie wymaga tego samego banku
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
                <h2 style="color: #1A1F71; margin:0;">Tryb 2: e-commerce — zeskanuj kartę i zapłać</h2>
                <p style="color: #333; margin-top:8px; font-size:1.05em;">Zamiast wpisywać numer karty przy kasie, zeskanuj QR swojej karty telefonem lub kamerką laptopa. Prośba o płatność pojawia się na telefonie — zatwierdź i gotowe.</p>
            </div>
            """, unsafe_allow_html=True)

        st.subheader(t("How It Works", "Jak to działa"))

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <h4 style="color:#1A1F71;">{t("Step 1: Checkout", "Krok 1: Wybór płatności")}</h4>
                <p style="font-size:0.9em; color:#666;">{t('At any online store, choose "Visa QR Pay" as your payment method', 'W dowolnym sklepie online wybierz "Visa QR Pay" jako metodę płatności')}</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <h4 style="color:#1A1F71;">{t("Step 2: Scan Your Card", "Krok 2: Zeskanuj kartę")}</h4>
                <p style="font-size:0.9em; color:#666;">{t("Hold your Visa card's QR code up to your phone camera or laptop webcam", "Przyłóż kod QR karty Visa do aparatu telefonu lub kamerki laptopa")}</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <h4 style="color:#1A1F71;">{t("Step 3: Approve on Phone", "Krok 3: Zatwierdź na telefonie")}</h4>
                <p style="font-size:0.9em; color:#666;">{t('A push notification: "Allegro — 289 PLN — headphones". You verify and approve with biometrics.', 'Powiadomienie push: "Allegro — 289 PLN — słuchawki". Weryfikujesz i zatwierdzasz biometrycznie.')}</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div style="background:white; border-radius:14px; padding:24px; text-align:center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height:280px;">
                <h4 style="color:#1A1F71;">{t("Step 4: Done", "Krok 4: Gotowe")}</h4>
                <p style="font-size:0.9em; color:#666;">{t("Payment confirmed. No card number typed. No 3DS redirect. Faster than BLIK.", "Płatność potwierdzona. Bez wpisywania numeru karty. Bez przekierowania 3DS. Szybciej niż BLIK.")}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        st.subheader(t("Why This Beats Current Methods", "Dlaczego to lepsze od obecnych metod"))

        if lang == "EN":
            comp = pd.DataFrame([
                {"Step": "Select payment method", "Traditional Card": "Choose 'card'", "BLIK": "Choose 'BLIK'", "Visa QR Pay": "Choose 'Visa QR Pay'"},
                {"Step": "Identify yourself", "Traditional Card": "Type 16-digit card number + expiry + CVV", "BLIK": "Open bank app, copy 6-digit code", "Visa QR Pay": "Scan QR on your card (1 second)"},
                {"Step": "Authenticate", "Traditional Card": "3D Secure redirect → bank app → confirm", "BLIK": "Confirm in bank app", "Visa QR Pay": "Approve push notification (biometric)"},
                {"Step": "Total steps", "Traditional Card": "5-7 steps, 30-60 seconds", "BLIK": "3-4 steps, 15-20 seconds", "Visa QR Pay": "2-3 steps, 5-10 seconds"},
                {"Step": "Card number exposed?", "Traditional Card": "Yes — typed into website", "BLIK": "No (different system)", "Visa QR Pay": "No — only tokenized ID transmitted"},
                {"Step": "Works internationally?", "Traditional Card": "Yes", "BLIK": "No (Poland only)", "Visa QR Pay": "Yes (any Visa-accepting merchant)"},
                {"Step": "Works on laptop without phone?", "Traditional Card": "Yes (but must type number)", "BLIK": "No (requires phone app)", "Visa QR Pay": "Yes (laptop webcam scans QR)"},
            ])
        else:
            comp = pd.DataFrame([
                {"Krok": "Wybierz metodę płatności", "Tradycyjna Karta": "Wybierz 'kartę'", "BLIK": "Wybierz 'BLIK'", "Visa QR Pay": "Wybierz 'Visa QR Pay'"},
                {"Krok": "Zidentyfikuj się", "Tradycyjna Karta": "Wpisz 16-cyfrowy numer karty + datę + CVV", "BLIK": "Otwórz aplikację banku, skopiuj 6-cyfrowy kod", "Visa QR Pay": "Zeskanuj QR na karcie (1 sekunda)"},
                {"Krok": "Uwierzytelnienie", "Tradycyjna Karta": "Przekierowanie 3D Secure → aplikacja banku → potwierdź", "BLIK": "Potwierdź w aplikacji banku", "Visa QR Pay": "Zatwierdź powiadomienie push (biometria)"},
                {"Krok": "Łączna liczba kroków", "Tradycyjna Karta": "5-7 kroków, 30-60 sekund", "BLIK": "3-4 kroki, 15-20 sekund", "Visa QR Pay": "2-3 kroki, 5-10 sekund"},
                {"Krok": "Numer karty ujawniony?", "Tradycyjna Karta": "Tak — wpisany na stronie", "BLIK": "Nie (inny system)", "Visa QR Pay": "Nie — przesyłane tylko tokenizowane ID"},
                {"Krok": "Działa międzynarodowo?", "Tradycyjna Karta": "Tak", "BLIK": "Nie (tylko Polska)", "Visa QR Pay": "Tak (każdy sprzedawca akceptujący Visa)"},
                {"Krok": "Działa na laptopie bez telefonu?", "Tradycyjna Karta": "Tak (ale trzeba wpisać numer)", "BLIK": "Nie (wymaga aplikacji na telefon)", "Visa QR Pay": "Tak (kamera laptopa skanuje QR)"},
            ])
        st.dataframe(comp, use_container_width=True, hide_index=True)

        st.success(t("""
        **The key advantage over BLIK:** Visa QR Pay is **faster** (scan vs. type 6-digit code), **more secure**
        (no card data shared, tokenized), **global** (works on any Visa-accepting website worldwide), and uses
        **biometric approval** (Face ID / fingerprint) instead of manually confirming in the bank app.
        """, """
        **Kluczowa przewaga nad BLIK:** Visa QR Pay jest **szybszy** (skan vs. wpisywanie 6-cyfrowego kodu), **bezpieczniejszy**
        (bez udostępniania danych karty, tokenizacja), **globalny** (działa na każdej stronie akceptującej Visa na świecie) i korzysta z
        **zatwierdzenia biometrycznego** (Face ID / odcisk palca) zamiast ręcznego potwierdzania w aplikacji bankowej.
        """))

    st.divider()

    # ── DATA-BACKED OPPORTUNITY ──
    st.header(t("Data-Backed: Why This Solution Addresses Real Gaps", "Co mówią dane: jakie realne luki wypełnia to rozwiązanie"))

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("Gaps Addressed by Visa QR Pay", "Luki, które wypełnia Visa QR Pay"))
        if lang == "EN":
            gaps = pd.DataFrame([
                {"Gap": "P2P payments (cards = 2%)", "Current Winner": "BLIK (55%)", "QR Pay Impact": "Direct competitor — scan card to send money", "TAM": "~280B PLN/year"},
                {"Gap": "E-commerce checkout friction", "Current Winner": "BLIK (67%)", "QR Pay Impact": "Faster than BLIK: scan vs type code", "TAM": "~65B PLN/year"},
                {"Gap": "Cash services (plumber, tutor)", "Current Winner": "Cash (90%+)", "QR Pay Impact": "No terminal needed — just show your card", "TAM": "~50B PLN/year"},
                {"Gap": "Marketplace payments (OLX)", "Current Winner": "BLIK/Transfer", "QR Pay Impact": "Instant card-to-card at meetup", "TAM": "~15B PLN/year"},
                {"Gap": "Group collections", "Current Winner": "BLIK/Transfer", "QR Pay Impact": "Share QR in chat, everyone scans & pays", "TAM": "~5B PLN/year"},
                {"Gap": "International online shopping", "Current Winner": "Card (but friction)", "QR Pay Impact": "Scan & approve — no number entry on foreign sites", "TAM": "~20B PLN/year"},
            ])
        else:
            gaps = pd.DataFrame([
                {"Luka": "Płatności P2P (karty = 2%)", "Obecny Lider": "BLIK (55%)", "Wpływ QR Pay": "Bezpośredni konkurent — zeskanuj kartę, wyślij pieniądze", "TAM": "~280 mld PLN/rok"},
                {"Luka": "Uciążliwa płatność w e-commerce", "Obecny Lider": "BLIK (67%)", "Wpływ QR Pay": "Szybszy niż BLIK: skan vs wpisywanie kodu", "TAM": "~65 mld PLN/rok"},
                {"Luka": "Usługi gotówkowe (hydraulik, korepetytor)", "Obecny Lider": "Gotówka (90%+)", "Wpływ QR Pay": "Bez terminala — pokaż kartę", "TAM": "~50 mld PLN/rok"},
                {"Luka": "Płatności marketplace (OLX)", "Obecny Lider": "BLIK/Przelew", "Wpływ QR Pay": "Natychmiastowa karta-do-karty przy spotkaniu", "TAM": "~15 mld PLN/rok"},
                {"Luka": "Zbiórki grupowe", "Obecny Lider": "BLIK/Przelew", "Wpływ QR Pay": "Udostępnij QR na czacie, każdy skanuje i płaci", "TAM": "~5 mld PLN/rok"},
                {"Luka": "Międzynarodowe zakupy online", "Obecny Lider": "Karta (ale z tarciem)", "Wpływ QR Pay": "Skanuj i zatwierdź — bez numeru na zagranicznych stronach", "TAM": "~20 mld PLN/rok"},
            ])
        st.dataframe(gaps, use_container_width=True, hide_index=True)
        source("gemius", "nbp_survey", "estimate", note=("TAM values are team estimates", "wartości TAM to szacunki zespołu"))

    with col2:
        st.subheader(t("Total Addressable Market", "Całkowity rynek docelowy"))
        fig = go.Figure(go.Funnel(
            y=[t("P2P Payments", "Płatności P2P"), t("Domestic E-Commerce", "Krajowy e-commerce"), t("Cash Services", "Usługi opłacane gotówką"), t("International E-Com", "Zagraniczny e-commerce"), t("Marketplace P2P", "Marketplace P2P"), t("Group Collections", "Zbiórki grupowe")],
            x=[280, 65, 50, 20, 15, 5],
            textinfo="value+text",
            text=[t("280B PLN", "280 mld PLN"), t("65B PLN", "65 mld PLN"), t("50B PLN", "50 mld PLN"), t("20B PLN", "20 mld PLN"), t("15B PLN", "15 mld PLN"), t("5B PLN", "5 mld PLN")],
            marker=dict(color=[VISA_BLUE, ACCENT[0], ACCENT[1], ACCENT[3], ACCENT[4], ACCENT[5]]),
        ))
        fig.update_layout(height=400, margin=dict(t=10,b=10), title_text=t("Estimated Annual Volume (PLN)", "Szacowany roczny wolumen (PLN)"))
        st.plotly_chart(fig, use_container_width=True)
        source("estimate")

    st.divider()

    # ── TECHNICAL ARCHITECTURE ──
    st.header(t("Technical Concept", "Koncepcja techniczna"))

    col1, col2 = st.columns(2)
    with col1:
        if lang == "EN":
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
        else:
            st.markdown("""
            ### Struktura Kodu QR
            ```
            visa://pay?token=VQR_8f3a...c7d2&ver=1
            ```

            Kod QR na karcie zawiera:
            - **Tokenizowany identyfikator karty** (nie rzeczywisty numer karty)
            - **Flagę wersji** dla przyszłej rozszerzalności
            - **Brak wrażliwych danych** — token jest bezużyteczny bez backendu Visa

            ### Model Bezpieczeństwa
            | Warstwa | Ochrona |
            |---|---|
            | Zawartość QR | Tylko tokenizowane ID — bez PAN, bez CVV |
            | Tworzenie płatności | Wymaga uwierzytelnionej sesji płacącego |
            | Zatwierdzenie | Powiadomienie push + biometria (Face ID / odcisk palca) |
            | Transakcja | Przetwarzana przez Visa Direct — pełne bezpieczeństwo i wykrywanie oszustw Visa |
            | Spory | Pełna ochrona chargeback Visa |
            | Unieważnienie tokenu | Właściciel karty może unieważnić/wygenerować nowy token QR w aplikacji banku |
            """)

    with col2:
        if lang == "EN":
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
        else:
            st.markdown("""
            ### Diagram Przepływu

            **Tryb P2P:**
            ```
            [Telefon Płacącego]      [Visa Cloud]          [Telefon Odbiorcy]
                 |                        |                        |
                 |--- Skanuj kod QR ----->|                        |
                 |--- Wpisz kwotę ------->|                        |
                 |                        |--- Powiadomienie push->|
                 |                        |    "Adam: 45 PLN       |
                 |                        |     za kolację"        |
                 |                        |                        |
                 |                        |<--- ZATWIERDŹ (biomet.)|
                 |                        |                        |
                 |<-- Potwierdzenie ------|--- Środki przelane --->|
                 |    "Płatność wysłana"  |    przez Visa Direct   |
            ```

            **Tryb E-Commerce:**
            ```
            [Strona sklepu]          [Visa Cloud]          [Twój Telefon]
                 |                        |                        |
                 |--- Zainicjuj płatność->|                        |
                 |                        |                        |
            [Skanujesz QR karty telefonem/kamerką]                 |
                 |--- Token wysłany ----->|                        |
                 |                        |--- Powiadomienie push->|
                 |                        |    "Allegro: 289 PLN   |
                 |                        |     słuchawki"         |
                 |                        |<--- ZATWIERDŹ (biomet.)|
                 |<-- Płatność potwierdz.-|                        |
                 |    "Zamówienie złożone!"|                        |
            ```
            """)

    st.divider()

    # ── COMPETITIVE ADVANTAGE ──
    st.header(t("Competitive Advantage vs BLIK", "Przewaga nad BLIK"))

    col1, col2 = st.columns(2)
    with col1:
        if lang == "EN":
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
        else:
            st.markdown("""
            <div style="background:linear-gradient(135deg, #E8F0FE, #D4E2F9); padding:24px; border-radius:14px; border:2px solid #A8C4E8; color:#1F2937;">
                <h3 style="color:#1A1F71;">Dlaczego Visa QR Pay wygrywa z BLIK:</h3>
                <ul style="font-size:0.95em; color:#1F2937;">
                    <li><strong style="color:#0D1137;">Nie potrzeba aplikacji do rozpoczęcia</strong> — każdy z aparatem może zeskanować kod QR. BLIK wymaga otwartej aplikacji banku.</li>
                    <li><strong style="color:#0D1137;">Fizyczna karta = zawsze dostępna</strong> — rozładowany telefon? Słaba bateria? QR na karcie nadal działa dla P2P.</li>
                    <li><strong style="color:#0D1137;">Globalny zasięg</strong> — działa u każdego sprzedawcy akceptującego Visa na świecie. BLIK = tylko Polska.</li>
                    <li><strong style="color:#0D1137;">Jedna tożsamość we wszystkich kanałach</strong> — ten sam QR dla P2P, e-commerce, usług osobistych.</li>
                    <li><strong style="color:#0D1137;">Brak 6-cyfrowego kodu do pomylenia</strong> — skan jest natychmiastowy i bezbłędny.</li>
                    <li><strong style="color:#0D1137;">Zatwierdzenie biometryczne</strong> — Face ID / odcisk palca vs. ręczne otwieranie aplikacji i potwierdzanie.</li>
                    <li><strong style="color:#0D1137;">Działa na laptopie</strong> — kamera skanuje QR dla desktopowego e-commerce. BLIK zawsze wymaga telefonu.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        if lang == "EN":
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
        else:
            st.markdown("""
            <div style="background:linear-gradient(135deg, #FFF3E0, #FFE8CC); padding:24px; border-radius:14px; border:2px solid #FFCC80; color:#3E2723;">
                <h3 style="color:#E65100;">W czym BLIK nadal jest dobry:</h3>
                <ul style="font-size:0.95em; color:#3E2723;">
                    <li><strong style="color:#4E342E;">Wbudowany w aplikacje polskich banków</strong> — 95% użytkowników bankowości mobilnej ma BLIK.</li>
                    <li><strong style="color:#4E342E;">Nie potrzeba fizycznej karty</strong> — czysto cyfrowy, działa tylko z telefonem.</li>
                    <li><strong style="color:#4E342E;">Wypłaty z bankomatów</strong> — BLIK może wypłacić gotówkę bez karty.</li>
                    <li><strong style="color:#4E342E;">Zaufanie do marki w Polsce</strong> — "BLIK" to prawie czasownik ("Zblikuję Ci").</li>
                </ul>
                <br/>
                <h3 style="color:#E65100;">Odpowiedź Visa QR Pay:</h3>
                <ul style="font-size:0.95em; color:#3E2723;">
                    <li>QR dostępny również <strong style="color:#4E342E;">w aplikacji bankowej</strong> (karta cyfrowa) — nie tylko fizyczna</li>
                    <li>Partnerstwo z polskimi bankami, by dodać <strong style="color:#4E342E;">przycisk "Visa QR Pay"</strong> obok BLIK</li>
                    <li>Wykorzystanie istniejących <strong style="color:#4E342E;">1.95M kart Visa</strong> w Polsce — zero nowych emisji</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ── ROLLOUT PLAN ──
    st.header(t("Proposed Rollout", "Proponowany plan wdrożenia"))

    if lang == "EN":
        phases = pd.DataFrame([
            {"Phase": "Phase 1 (0-3 months)", "Action": "Pilot with 2-3 Polish banks — QR in mobile banking app", "Target": "P2P payments between bank customers", "KPI": "10K active QR payers"},
            {"Phase": "Phase 2 (3-6 months)", "Action": "QR stickers sent to all Visa cardholders by mail", "Target": "P2P + marketplace (OLX, Vinted)", "KPI": "100K active QR payers"},
            {"Phase": "Phase 3 (6-12 months)", "Action": "Merchant SDK — 'Visa QR Pay' button at checkout", "Target": "Top 50 Polish e-commerce sites", "KPI": "1M online QR transactions/month"},
            {"Phase": "Phase 4 (12-18 months)", "Action": "QR printed on all new Visa cards in Poland", "Target": "Full market — P2P, e-com, services", "KPI": "5% of e-commerce share (from ~9%)"},
            {"Phase": "Phase 5 (18-24 months)", "Action": "International rollout — EU, then global", "Target": "Cross-border P2P & e-commerce", "KPI": "Pan-European Visa QR standard"},
        ])
    else:
        phases = pd.DataFrame([
            {"Faza": "Faza 1 (0-3 miesiące)", "Działanie": "Pilot z 2-3 polskimi bankami — QR w aplikacji mobilnej", "Cel": "Płatności P2P między klientami banków", "KPI": "10K aktywnych płatników QR"},
            {"Faza": "Faza 2 (3-6 miesięcy)", "Działanie": "Naklejki QR wysłane do wszystkich posiadaczy kart Visa", "Cel": "P2P + marketplace (OLX, Vinted)", "KPI": "100K aktywnych płatników QR"},
            {"Faza": "Faza 3 (6-12 miesięcy)", "Działanie": "SDK dla sprzedawców — przycisk 'Visa QR Pay' przy kasie", "Cel": "50 największych polskich sklepów internetowych", "KPI": "1M transakcji QR online/mies."},
            {"Faza": "Faza 4 (12-18 miesięcy)", "Działanie": "QR drukowany na wszystkich nowych kartach Visa w Polsce", "Cel": "Pełny rynek — P2P, e-com, usługi", "KPI": "5% udziału w e-commerce (z ~9%)"},
            {"Faza": "Faza 5 (18-24 miesiące)", "Działanie": "Międzynarodowe wdrożenie — UE, potem globalnie", "Cel": "Transgraniczne P2P i e-commerce", "KPI": "Paneuropejski standard Visa QR"},
        ])
    st.dataframe(phases, use_container_width=True, hide_index=True)

    st.divider()

    # ── IMPACT ESTIMATION ──
    st.header(t("Projected Impact", "Prognozowany wpływ"))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(t("P2P market capture target", "Docelowy udział w rynku P2P"), "10%", help=t("Of BLIK's 55% P2P share → ~28B PLN/year", "Z 55% udziału BLIK w P2P → ~28 mld PLN/rok"))
        st.metric(t("New annual card P2P volume", "Nowy roczny wolumen P2P na kartach"), "~28B PLN")
    with col2:
        st.metric(t("E-commerce share gain", "Wzrost udziału w e-commerce"), "+3-5pp", help=t("From ~9% to 12-14% of e-commerce", "Z ~9% do 12-14% e-commerce"))
        st.metric(t("New annual e-com volume", "Nowy roczny wolumen e-commerce"), "~3-4B PLN")
    with col3:
        st.metric(t("Cash services converted", "Przejście usług z gotówki na kartę"), "5-10%", help=t("Of ~50B PLN cash service economy", "Z ~50 mld PLN usług opłacanych gotówką"))
        st.metric(t("New annual service volume", "Nowy roczny wolumen usług"), "~3-5B PLN")
    source("sim", note=("targets, not forecasts from data", "cele, nie prognozy z danych"))

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
            <h3 style="color:#1B7A3D; margin:0 0 8px 0;">Łączny potencjał: ~35 mld PLN nowego rocznego wolumenu transakcji kartowych</h3>
            <p style="margin:0; color:#1A3C2A;">Zamieniając każdą kartę Visa w punkt przyjmowania płatności (przez QR), zmieniamy kartę z „narzędzia do wydawania”
            w <strong style="color:#145A24;">uniwersalną platformę płatniczą</strong> — konkurując z BLIK wygodą, a jednocześnie wykorzystując globalną infrastrukturę Visa,
            bezpieczeństwo i ochronę kupującego, których BLIK nie może zapewnić.</p>
        </div>
        """, unsafe_allow_html=True)
