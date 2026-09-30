"""Page: Recommendations."""
import pandas as pd
import streamlit as st

from app_pages.common import t


def render():
    lang = st.session_state.get("lang", "EN")

    st.header(t("Strategic Recommendations", "Rekomendacje strategiczne"))
    if lang == "EN":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8EDF8, #D0D9F0); padding: 24px 28px; border-radius: 14px; color: #0D1137; margin-bottom: 20px; border: 2px solid #B0BDE0;">
            <h3 style="margin:0; color:#1A1F71;">CardFlow — From Cash & Transfer to Card</h3>
            <p style="color:#333; margin-top:6px;">We turn transaction data into concrete decisions. We show not just how people pay,
            but what to do to make the card their most convenient choice — online and in private payments.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8EDF8, #D0D9F0); padding: 24px 28px; border-radius: 14px; color: #0D1137; margin-bottom: 20px; border: 2px solid #B0BDE0;">
            <h3 style="margin:0; color:#1A1F71;">CardFlow — od gotówki i przelewów do karty</h3>
            <p style="color:#333; margin-top:6px;">Zamieniamy dane transakcyjne w konkretne decyzje. Pokazujemy nie tylko jak ludzie płacą,
            ale co zrobić, by karta była ich najwygodniejszym wyborem — online i w płatnościach między znajomymi.</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader(t("For Three Target Audiences", "Dla trzech grup odbiorców"))

    tab1, tab2, tab3 = st.tabs([t("Online Merchants", "Dla sklepów internetowych"),
                                 t("Banks & Visa", "Dla banków i Visa"),
                                 t("Cities & Municipalities", "Dla miast i samorządów")])

    with tab1:
        if lang == "EN":
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
        else:
            st.markdown("""
            ### Sklepy internetowe: prostsza płatność, większy udział kart

            | Zidentyfikowany punkt ucieczki | Rekomendacja | Oczekiwany wpływ |
            |---|---|---|
            | **67% e-commerce używa BLIK** bo jest jednym kliknięciem | Wdrożyć **Visa Click to Pay** — tokenizowana płatność kartą jednym kliknięciem | +3-5pp udziału kart |
            | **Zakupy spożywcze online: 0.12%** | Karta jako domyślna płatność w dostawach zakupów (Frisco, Barbora) | Średni koszyk online 3.1× wyższy |
            | **Średnia online = 318 vs 165 fizyczna** | Promować kartę dla zakupów online o wysokiej wartości (elektronika, meble) | Wyższy przychód na TX |
            | **Odzież online: 5% TX, 16% wartości** | Zapisana karta i szybka płatność w sklepach z modą | Zatrzymanie stałych kupujących |
            | **Za pobraniem nadal 5% e-commerce** | Zaoferować "Zapłać kartą, dostawa gratis" | Konwersja pobrania → karta |
            | **BLIK nie ma ochrony chargeback** | Podkreślić ochronę kupującego Visa przy drogich zakupach | Przewaga zaufania >200 PLN |

            **Szybki efekt:** Partnerstwo z Allegro (już 1.8M TX kartowych), by Visa Click to Pay był tak widoczny jak BLIK przy kasie.
            """)

    with tab2:
        if lang == "EN":
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
        else:
            st.markdown("""
            ### Banki i Visa: Aktywuj karty w nowych kanałach

            | Segment | Obecny stan | Szansa Visa Direct / Karta |
            |---|---|---|
            | **Płatności P2P** | BLIK 55%, karta ~2% | **Visa Direct** na natychmiastowe P2P — "podziel rachunek kartą" |
            | **Subskrypcje** | 282K kart na Netflix, 240K na Apple | Promować zapisaną kartę dla WSZYSTKICH subskrypcji (telekom, ubezpieczenia) |
            | **Rachunki cykliczne** | 3% karta, 90% przelew/polecenie zapłaty | Płatność rachunków powiązana z kartą z **2% cashback** |
            | **Wiek 65+** | 72% preferencja gotówki | Uproszczona karta zbliżeniowa dla seniorów + edukacja |
            | **Wiek 45-64** | 40% gotówka | Kampania "Twoja karta działa też online" |
            | **Mikropłatności <10 PLN** | 65% gotówka | Zerowa opłata za zbliżeniowe poniżej 10 PLN dla sprzedawców |
            | **Intensywni użytkownicy ATM** | Średnia 1 521/wypłata | Kampania: „po co wypłacać, skoro możesz zapłacić zbliżeniowo?” |

            **Szybki efekt:** Uruchomienie "Visa Split" — przelewy karta-do-karty P2P zintegrowane w aplikacjach bankowych, bezpośrednia konkurencja z BLIK P2P.

            **Szansa Visa Direct:** 14.5M gospodarstw płacących 416 PLN/mies. czynszu + 68 PLN telekom = **7 mld PLN/mies.** potencjalnych płatności powiązanych z kartą.
            """)

    with tab3:
        if lang == "EN":
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
        else:
            st.markdown("""
            ### Miasta i samorządy: Bezgotówkowa lokalna gospodarka

            | Wyzwanie miejskie | Dane | Rozwiązanie |
            |---|---|---|
            | **Targowiska** | 15% pokrycia terminali | Program **Tap-to-Phone** dla sprzedawców targowych (zero kosztów) |
            | **Transport lokalny** | 3.8M tx, ale 1M tylko przez aplikacje | Walidatory kart zbliżeniowych we wszystkich autobusach/tramwajach |
            | **Parking** | 2.8M tx w parkometrach/garażach | Uniwersalne parkometry z tap kartą |
            | **Opłaty miejskie** | 60% pokrycia terminali | Portal płatności kartą online dla wszystkich usług miejskich |
            | **Lokalne imprezy/festiwale** | Tradycyjnie gotówkowe | Bezgotówkowe opaski eventowe powiązane z Visa |
            | **Food trucki i street food** | 50% pokrycia terminali | Program wdrożenia mikro-POS SumUp/Zettle |
            | **Instytucje publiczne** | 60% terminali | Kioski płatności kartą w urzędach |

            **Pilotaż w jednym mieście:** Partnerstwo z jednym polskim miastem (np. Kraków — najwyższa mobilność kartowa 17.7%)
            dla pilotażu **"Miasto Bezgotówkowe"** — pomiar wpływu na lokalny handel, widoczność przychodów podatkowych i wydatki turystów.
            """)

    st.divider()
    st.subheader(t("Priority Matrix", "Macierz priorytetów"))

    if lang == "EN":
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
    else:
        priorities = pd.DataFrame([
            {"Inicjatywa": "Visa Click to Pay u największych sprzedawców", "Wpływ": "Wysoki", "Nakład": "Średni", "Harmonogram": "3-6 miesięcy", "Cel": "Merchanci"},
            {"Inicjatywa": "E-grocery checkout karta-najpierw", "Wpływ": "Wysoki", "Nakład": "Średni", "Harmonogram": "3-6 miesięcy", "Cel": "Merchanci"},
            {"Inicjatywa": "Tap-to-Phone dla usługodawców", "Wpływ": "Wysoki", "Nakład": "Niski", "Harmonogram": "1-3 miesiące", "Cel": "Visa/Banki"},
            {"Inicjatywa": "Visa Direct P2P w aplikacjach bankowych", "Wpływ": "Bardzo Wysoki", "Nakład": "Wysoki", "Harmonogram": "6-12 miesięcy", "Cel": "Banki"},
            {"Inicjatywa": "Zapisana karta dla rachunków cyklicznych", "Wpływ": "Bardzo Wysoki", "Nakład": "Wysoki", "Harmonogram": "6-12 miesięcy", "Cel": "Banki"},
            {"Inicjatywa": "Zerowe opłaty za mikropłatności", "Wpływ": "Średni", "Nakład": "Niski", "Harmonogram": "1-3 miesiące", "Cel": "Visa"},
            {"Inicjatywa": "Pilotaż Miasto Bezgotówkowe", "Wpływ": "Wysoki", "Nakład": "Wysoki", "Harmonogram": "6-12 miesięcy", "Cel": "Miasta"},
            {"Inicjatywa": "Edukacja zbliżeniowa dla seniorów", "Wpływ": "Średni", "Nakład": "Niski", "Harmonogram": "1-3 miesiące", "Cel": "Banki"},
        ])
    st.dataframe(priorities, use_container_width=True, hide_index=True)

    st.divider()
    if lang == "EN":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFF9E6, #FFF3CC); padding: 20px 24px; border-radius: 14px; border-left: 4px solid #F7B600; color:#3D2E00;">
            <h3 style="color:#0D1137; margin:0 0 8px 0;">The Bottom Line</h3>
            <p style="margin:0; font-size:1.05em; color:#3D2E00;">
            Cards already dominate physical POS (58% and growing). But <strong style="color:#1A1F71;">~25% of household spending</strong> (housing, telecom, education)
            is invisible to cards, and in e-commerce <strong style="color:#1A1F71;">BLIK has captured 67%</strong>. The opportunity is not to fight BLIK head-on
            in domestic one-click payments, but to <strong style="color:#1A1F71;">own the niches where cards have structural advantages</strong>:
            international commerce, subscriptions, high-value purchases with buyer protection, P2P via Visa Direct,
            and the untapped recurring bills market. Combined, these represent <strong style="color:#1A1F71;">tens of billions of PLN in annual payment volume</strong>
            currently flowing through non-card channels.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFF9E6, #FFF3CC); padding: 20px 24px; border-radius: 14px; border-left: 4px solid #F7B600; color:#3D2E00;">
            <h3 style="color:#0D1137; margin:0 0 8px 0;">Podsumowanie</h3>
            <p style="margin:0; font-size:1.05em; color:#3D2E00;">
            Karty już dominują w sklepach stacjonarnych (58% i rośnie). Ale <strong style="color:#1A1F71;">~25% wydatków gospodarstw domowych</strong> (mieszkanie, telekom, edukacja)
            jest niewidoczne dla kart, a w e-commerce <strong style="color:#1A1F71;">BLIK przejął 67%</strong>. Szansa nie polega na walce z BLIK wprost
            w krajowych płatnościach jednym kliknięciem, ale na <strong style="color:#1A1F71;">zajmowaniu nisz, gdzie karty mają trwałą przewagę</strong>:
            handel międzynarodowy, subskrypcje, zakupy o wysokiej wartości z ochroną kupującego, P2P przez Visa Direct
            i niewykorzystany rynek rachunków cyklicznych. Łącznie to <strong style="color:#1A1F71;">dziesiątki miliardów PLN rocznego wolumenu płatności</strong>
            płynących dziś poza kartami.
            </p>
        </div>
        """, unsafe_allow_html=True)
