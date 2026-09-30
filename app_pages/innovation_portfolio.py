"""Page: Innovation Portfolio (Visa Marketplace Shield, the next product on the QR Pay rails)."""
import streamlit as st

from app_pages.common import source, t


def render():
    st.header("Visa Marketplace Shield")
    st.caption(t("Next on the same QR: safe card payments between people on OLX, Vinted and Facebook Marketplace",
                 "Kolejny krok na tym samym QR: bezpieczne płatności kartą między osobami na OLX, Vinted i Facebook Marketplace"))

    # ── Problem / solution / edge ──────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1.container(border=True, height="stretch"):
        st.markdown(t("#### The problem", "#### Problem"))
        st.markdown(t(
            "Second-hand deals are paid by BLIK or bank transfer. Both are instant and **irreversible**: "
            "if the seller never ships, the money is gone. Cards play no role here today.",
            "Transakcje z ogłoszeń opłaca się BLIK-iem lub przelewem. Oba są natychmiastowe i **nieodwracalne**: "
            "jeśli sprzedający nie wyśle towaru, pieniądze przepadają. Karty w ogóle tu dziś nie występują."))
    with c2.container(border=True, height="stretch"):
        st.markdown(t("#### Our solution", "#### Nasze rozwiązanie"))
        st.markdown(t(
            "The buyer pays by card, but **Visa holds the money** until the buyer confirms the item arrived. "
            "Then it goes to the seller's card.",
            "Kupujący płaci kartą, ale **Visa przechowuje pieniądze**, dopóki kupujący nie potwierdzi, że towar dotarł. "
            "Wtedy trafiają na kartę sprzedającego."))
    with c3.container(border=True, height="stretch"):
        st.markdown(t("#### Why it beats BLIK", "#### Przewaga nad BLIK"))
        st.markdown(t(
            "- Buyer: money back if something goes wrong (Visa chargeback)\n"
            "- Seller: guaranteed payment, no fake transfer confirmations\n"
            "- Both: a rating that builds trust over time",
            "- Kupujący: zwrot pieniędzy, gdy coś pójdzie nie tak (chargeback Visa)\n"
            "- Sprzedający: gwarantowana zapłata, bez fałszywych potwierdzeń przelewu\n"
            "- Obie strony: ocena, która z czasem buduje zaufanie"))

    # ── How it works ───────────────────────────────────────────────────
    st.subheader(t("How it works", "Jak to działa"))
    steps = [
        (t("Scan", "Skan"), t("The buyer scans the seller's Visa QR, online or at a meetup.",
                              "Kupujący skanuje QR karty Visa sprzedającego, online albo przy spotkaniu.")),
        (t("Pay", "Płatność"), t("The buyer pays by card. Visa holds the money.",
                                 "Kupujący płaci kartą. Visa przechowuje pieniądze.")),
        (t("Confirm", "Potwierdzenie"), t("The buyer confirms receipt within 48 h. The seller gets paid within 24 h.",
                                          "Kupujący potwierdza odbiór w ciągu 48 h. Sprzedający dostaje pieniądze w ciągu 24 h.")),
        (t("Dispute", "Spór"), t("Item missing or not as described? The buyer opens a Visa chargeback.",
                                 "Towar nie dotarł albo jest niezgodny z opisem? Kupujący zgłasza chargeback Visa.")),
    ]
    for i, (col, (title, text)) in enumerate(zip(st.columns(4), steps), 1):
        with col.container(border=True, height="stretch"):
            st.markdown(f"**{i}. {title}**")
            st.caption(text)

    # ── Numbers ────────────────────────────────────────────────────────
    st.subheader(t("Size of the opportunity", "Skala szansy"))
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(t("Marketplace deals per year", "Transakcje z ogłoszeń rocznie"), t("~15B PLN", "~15 mld PLN"))
    m2.metric(t("Target share", "Docelowy udział"), "10–15%")
    m3.metric(t("New card volume per year", "Nowy wolumen kartowy rocznie"), t("1.5–2.3B PLN", "1,5–2,3 mld PLN"))
    m4.metric(t("Protection fee", "Opłata za ochronę"), "1–2%", t("paid by the buyer", "płaci kupujący"), delta_color="off")
    source("estimate", note=("market size, share and fee are assumptions, not results from Visa data",
                             "wielkość rynku, udział i opłata to założenia, nie wyniki z danych Visa"))

    # ── Synergy ────────────────────────────────────────────────────────
    st.info(t(
        "**One QR, two products.** Visa QR Pay says *who* gets paid; Marketplace Shield makes sure the deal is *safe*. "
        "The same QR on the card powers both, so Shield needs no new rails.",
        "**Jeden QR, dwa produkty.** Visa QR Pay mówi, *komu* zapłacić, a Marketplace Shield pilnuje, żeby transakcja była *bezpieczna*. "
        "Ten sam QR na karcie obsługuje oba, więc Shield nie wymaga nowej infrastruktury."))
