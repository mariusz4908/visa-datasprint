"""
CardFlow — Pitch Deck (8 slides, focused on the idea)
Bilingual PL/EN
"""
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
import os

W, H = landscape(A4)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CardFlow_PitchDeck.pdf")

# Colors
VB = HexColor("#1A1F71")
VG = HexColor("#F7B600")
VD = HexColor("#0D1137")
LB = HexColor("#F0F4FF")
RED = HexColor("#E85D75")
GRN = HexColor("#2ECC71")
GRY = HexColor("#666666")
BLIK = HexColor("#D40E6A")
WHT = white
BLK = black
LGRY = HexColor("#999999")
DGRY = HexColor("#333333")


class Deck(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sn = 0
    def showPage(self):
        self.sn += 1
        super().showPage()

c = Deck(OUT, pagesize=landscape(A4))

def bg_dark(c):
    c.setFillColor(VD)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(HexColor("#F7B60010"))
    c.circle(W - 4*cm, H - 3*cm, 9*cm, fill=1, stroke=0)
    _footer(c)

def bg_light(c):
    c.setFillColor(WHT)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(VB)
    c.rect(0, H - 2.2*cm, W, 2.2*cm, fill=1, stroke=0)
    c.setFillColor(VG)
    c.rect(0, H - 2.2*cm - 2.5, W, 2.5, fill=1, stroke=0)
    _footer(c)

def _footer(c):
    c.setFillColor(HexColor("#F7F8FA"))
    c.rect(0, 0, W, 0.9*cm, fill=1, stroke=0)
    c.setFillColor(LGRY)
    c.setFont("Helvetica", 7)
    c.drawString(1*cm, 0.3*cm, "CardFlow — Visa DataSprint Hackathon 2026")
    c.drawRightString(W - 1*cm, 0.3*cm, f"{c.sn + 1} / 8")

def title(c, txt, y=None, sz=22, col=WHT):
    if y is None: y = H - 1.6*cm
    c.setFillColor(col); c.setFont("Helvetica-Bold", sz); c.drawString(1.5*cm, y, txt)

def txt(c, t, x, y, sz=11, col=BLK, font="Helvetica", bold=False, mw=None):
    if bold: font = "Helvetica-Bold"
    c.setFillColor(col); c.setFont(font, sz)
    if mw:
        words = t.split(); line = ""
        for w in words:
            test = (line + " " + w).strip()
            if c.stringWidth(test, font, sz) > mw:
                c.drawString(x, y, line); y -= sz * 1.35; line = w
            else:
                line = test
        if line: c.drawString(x, y, line); y -= sz * 1.35
        return y
    c.drawString(x, y, t); return y - sz * 1.35

def bullet(c, items, x, y, sz=10, col=BLK, mw=None):
    for item in items:
        c.setFillColor(VG); c.setFont("Helvetica-Bold", sz); c.drawString(x, y, "\u25b8")
        y = txt(c, item, x + 12, y, sz=sz, col=col, mw=mw or (W/2 - 3*cm))
        y -= 1
    return y

def kpi(c, x, y, w, h, val, label, col=VB):
    c.setFillColor(LB); c.roundRect(x, y, w, h, 4, fill=1, stroke=0)
    c.setFillColor(col); c.setFont("Helvetica-Bold", 18); c.drawCentredString(x+w/2, y+h-24, val)
    c.setFillColor(GRY); c.setFont("Helvetica", 7); c.drawCentredString(x+w/2, y+6, label)


# ═══════════════════════════════════════════════════════════════
# SLIDE 1: TITLE
# ═══════════════════════════════════════════════════════════════
bg_dark(c)
c.setFillColor(WHT); c.setFont("Helvetica-Bold", 42)
c.drawString(2*cm, H - 5*cm, "CardFlow")

c.setFont("Helvetica", 15); c.setFillColor(HexColor("#B0B8D0"))
c.drawString(2*cm, H - 6.5*cm, "Od gotówki i przelewu do karty")
c.drawString(2*cm, H - 7.5*cm, "From cash & transfer to card")

c.setFillColor(VG); c.roundRect(2*cm, H - 9.5*cm, 11*cm, 0.9*cm, 4, fill=1, stroke=0)
c.setFillColor(VD); c.setFont("Helvetica-Bold", 10)
c.drawCentredString(7.5*cm, H - 9.2*cm, "VISA DATASPRINT HACKATHON 2026")

c.setFillColor(HexColor("#777777")); c.setFont("Helvetica", 9)
c.drawString(2*cm, 2.2*cm, "Dane transakcyjne jako mapa drogowa popularyzacji kart")
c.drawString(2*cm, 1.5*cm, "w e-commerce i płatnościach P2P")
c.showPage()

# ═══════════════════════════════════════════════════════════════
# SLIDE 2: PROBLEM
# ═══════════════════════════════════════════════════════════════
bg_light(c)
title(c, "Problem: Why cards lose online / Dlaczego karty przegrywają online")

y = H - 3.5*cm
txt(c, "Cards = 58% at physical POS. But online and in P2P — they're losing to BLIK.", 2*cm, y, sz=13, bold=True, col=VB)
y -= 0.4*cm
txt(c, "Karty = 58% w POS fizycznym. Ale online i w P2P — przegrywają z BLIK.", 2*cm, y - 0.5*cm, sz=10, col=GRY)

y -= 2*cm
kpi(c, 1.5*cm, y - 2.2*cm, 4.5*cm, 2.2*cm, "67%", "BLIK share in e-commerce / Udział BLIK w e-com", BLIK)
kpi(c, 6.5*cm, y - 2.2*cm, 4.5*cm, 2.2*cm, "16%", "Card share in e-commerce / Udział kart w e-com", VB)
kpi(c, 11.5*cm, y - 2.2*cm, 4.5*cm, 2.2*cm, "55%", "BLIK share in P2P / Udział BLIK w P2P", BLIK)
kpi(c, 16.5*cm, y - 2.2*cm, 4.5*cm, 2.2*cm, "~2%", "Card share in P2P / Udział kart w P2P", RED)
kpi(c, 21.5*cm, y - 2.2*cm, 4.5*cm, 2.2*cm, "-2pp/yr", "Card decline rate / Tempo spadku kart", RED)

y -= 3.8*cm
txt(c, "The same person taps Visa at a store, but pays with BLIK online. Why?", 2*cm, y, sz=11, bold=True, col=VD)
y -= 0.5*cm
bullet(c, [
    "BLIK = 1 code, 1 tap. Card = type 16 digits + expiry + CVV + 3DS redirect",
    "BLIK feels safer — no card data shared with the website",
    "BLIK P2P is native in banking apps — cards have no P2P mechanism",
    "25% of household budget (rent, telecom, education) flows through transfers, not cards",
], 2*cm, y, sz=9, mw=W - 4*cm)
c.showPage()

# ═══════════════════════════════════════════════════════════════
# SLIDE 3: OUR INSIGHT (DATA-DRIVEN)
# ═══════════════════════════════════════════════════════════════
bg_light(c)
title(c, "Data Insight: Escape Points / Punkty ucieczki od karty")

y = H - 3.5*cm
txt(c, "We analyzed 305.5M Visa transactions and cross-referenced with GUS, NBP, Gemius data.", 2*cm, y, sz=11, bold=True, col=VB)
y -= 0.3*cm
txt(c, "Przeanalizowaliśmy 305.5M transakcji Visa i skrzyżowaliśmy z danymi GUS, NBP, Gemius.", 2*cm, y - 0.4*cm, sz=9, col=GRY)

y -= 1.8*cm
txt(c, "3 key escape points identified:", 2*cm, y, sz=12, bold=True, col=VD)
y -= 0.6*cm

# Escape point 1
c.setFillColor(HexColor("#FDE8EC")); c.roundRect(1.5*cm, y - 3.2*cm, 8.5*cm, 3.2*cm, 5, fill=1, stroke=0)
txt(c, "1. E-COMMERCE CHECKOUT", 2*cm, y - 0.4*cm, sz=10, bold=True, col=RED)
txt(c, "BLIK: 67% → Cards: 16%", 2*cm, y - 1*cm, sz=9, col=DGRY)
txt(c, "Typing card number is the #1", 2*cm, y - 1.6*cm, sz=8, col=GRY)
txt(c, "friction point. BLIK = 1 code.", 2*cm, y - 2.2*cm, sz=8, col=GRY)
txt(c, "Wpisywanie numeru = główna bariera.", 2*cm, y - 2.7*cm, sz=7, col=LGRY)

# Escape point 2
c.setFillColor(HexColor("#FDE8EC")); c.roundRect(10.5*cm, y - 3.2*cm, 8.5*cm, 3.2*cm, 5, fill=1, stroke=0)
txt(c, "2. P2P PAYMENTS", 11*cm, y - 0.4*cm, sz=10, bold=True, col=RED)
txt(c, "BLIK: 55% → Cards: ~2%", 11*cm, y - 1*cm, sz=9, col=DGRY)
txt(c, "No card-native way to split a bill", 11*cm, y - 1.6*cm, sz=8, col=GRY)
txt(c, "or pay a friend. BLIK owns this.", 11*cm, y - 2.2*cm, sz=8, col=GRY)
txt(c, "Brak kartowego sposobu na podział rachunku.", 11*cm, y - 2.7*cm, sz=7, col=LGRY)

# Escape point 3
c.setFillColor(HexColor("#FDE8EC")); c.roundRect(19.5*cm, y - 3.2*cm, 8*cm, 3.2*cm, 5, fill=1, stroke=0)
txt(c, "3. CASH SERVICES", 20*cm, y - 0.4*cm, sz=10, bold=True, col=RED)
txt(c, "Doctors, plumbers, tutors: 90%+ cash", 20*cm, y - 1*cm, sz=9, col=DGRY)
txt(c, "No terminals. ~50B PLN/year in cash.", 20*cm, y - 1.6*cm, sz=8, col=GRY)
txt(c, "Brak terminali = usługi za gotówkę.", 20*cm, y - 2.7*cm, sz=7, col=LGRY)

y -= 4.5*cm
txt(c, "Conclusion: Cards don't lose on trust. They lose on convenience and reach.", 2*cm, y, sz=11, bold=True, col=VB)
txt(c, "Wniosek: Karty nie przegrywają na zaufaniu. Przegrywają na wygodzie i zasięgu.", 2*cm, y - 0.6*cm, sz=9, col=GRY)
c.showPage()

# ═══════════════════════════════════════════════════════════════
# SLIDE 4: SOLUTION — VISA QR PAY
# ═══════════════════════════════════════════════════════════════
bg_dark(c)
c.setFillColor(VG); c.setFont("Helvetica-Bold", 28)
c.drawString(2*cm, H - 3*cm, "Solution: Visa QR Pay")
c.setFillColor(HexColor("#A0AAC0")); c.setFont("Helvetica", 13)
c.drawString(2*cm, H - 4*cm, "Rozwiązanie: Visa QR Pay")

c.setFillColor(WHT); c.setFont("Helvetica", 11)
c.drawString(2*cm, H - 5.2*cm, "Every Visa card gets a unique QR code. Scan it to pay — no card number needed.")
c.setFillColor(HexColor("#A0AAC0")); c.setFont("Helvetica", 9)
c.drawString(2*cm, H - 5.9*cm, "Każda karta Visa otrzymuje unikalny kod QR. Zeskanuj, żeby zapłacić — bez wpisywania numeru.")

# Two modes
y = H - 7.5*cm

# Mode 1 box
c.setFillColor(HexColor("#1A1F7140")); c.roundRect(1.5*cm, y - 5*cm, 12.5*cm, 5*cm, 6, fill=1, stroke=0)
c.setFillColor(VG); c.setFont("Helvetica-Bold", 13)
c.drawString(2*cm, y - 0.5*cm, "MODE 1: P2P Payment / Płatność P2P")
c.setFillColor(WHT); c.setFont("Helvetica", 9)
texts = [
    "1. Friend scans your card's QR / Znajomy skanuje QR Twojej karty",
    "2. Enters amount + description / Wpisuje kwotę + opis",
    "3. You get push notification / Dostajesz powiadomienie push",
    "4. Approve with Face ID / Zatwierdzasz biometrycznie",
    "→ Money via Visa Direct — instant / Pieniądze przez Visa Direct — natychmiast",
]
ty = y - 1.3*cm
for t_line in texts:
    c.drawString(2.3*cm, ty, t_line); ty -= 0.6*cm

c.setFillColor(WHT); c.setFont("Helvetica-Bold", 8)
c.drawString(2*cm, y - 4.6*cm, "Use: split bills, OLX, group collections, pay plumber")

# Mode 2 box
c.setFillColor(HexColor("#F7B60025")); c.roundRect(14.5*cm, y - 5*cm, 12.5*cm, 5*cm, 6, fill=1, stroke=0)
c.setFillColor(VG); c.setFont("Helvetica-Bold", 13)
c.drawString(15*cm, y - 0.5*cm, "MODE 2: E-Commerce / Płatności online")
c.setFillColor(WHT); c.setFont("Helvetica", 9)
texts2 = [
    "1. At checkout, choose Visa QR Pay / Przy kasie wybierz Visa QR Pay",
    "2. Scan YOUR card (phone/webcam) / Zeskanuj SWOJĄ kartę",
    "3. Approve push notification / Zatwierdź powiadomienie",
    "4. Done — no number typed! / Gotowe — bez wpisywania numeru!",
    "→ Faster than BLIK, works globally / Szybciej niż BLIK, działa globalnie",
]
ty = y - 1.3*cm
for t_line in texts2:
    c.drawString(15.3*cm, ty, t_line); ty -= 0.6*cm

c.setFillColor(WHT); c.setFont("Helvetica-Bold", 8)
c.drawString(15*cm, y - 4.6*cm, "Use: any online store, international shopping, laptop webcam")
c.showPage()

# ═══════════════════════════════════════════════════════════════
# SLIDE 5: WHY BETTER THAN BLIK
# ═══════════════════════════════════════════════════════════════
bg_light(c)
title(c, "Visa QR Pay vs BLIK — Why we win / Dlaczego wygrywamy")

y = H - 3.5*cm

# Comparison table
from reportlab.platypus import Table, TableStyle
data = [
    ["", "Traditional Card", "BLIK", "Visa QR Pay"],
    ["Steps online", "5-7 (type number)", "3-4 (code + confirm)", "2-3 (scan + approve)"],
    ["Card data exposed?", "YES", "No", "NO (tokenized)"],
    ["P2P payments", "Not supported", "55% market", "Full support"],
    ["Works globally", "Yes", "Poland only", "Yes (global)"],
    ["Dead phone?", "Yes (type number)", "Doesn't work", "Yes (QR on card)"],
    ["Laptop checkout", "Type number", "Needs phone", "Webcam scan"],
    ["Buyer protection", "Full Visa", "Limited", "Full Visa"],
    ["Auth method", "3DS redirect", "Bank app PIN", "Biometric push"],
]
t = Table(data, colWidths=[4*cm, 5.5*cm, 5.5*cm, 5.5*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), VB),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHT),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BACKGROUND', (3, 1), (3, -1), HexColor("#E8F0FE")),
    ('FONTNAME', (3, 1), (3, -1), 'Helvetica-Bold'),
    ('GRID', (0, 0), (-1, -1), 0.4, HexColor("#CCCCCC")),
    ('PADDING', (0, 0), (-1, -1), 4),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHT, HexColor("#F7F8FA")]),
]))
t.wrapOn(c, W, H)
t.drawOn(c, 3*cm, y - 6*cm)

y -= 7*cm
txt(c, "Key: QR Pay is faster than BLIK (scan vs type code), global (vs Poland-only), and works with dead phone.", 2*cm, y, sz=9, bold=True, col=VB, mw=W-4*cm)
txt(c, "Kluczowe: QR Pay jest szybszy niż BLIK, globalny (vs tylko Polska) i działa z wyładowanym telefonem.", 2*cm, y - 0.6*cm, sz=8, col=GRY, mw=W-4*cm)
c.showPage()

# ═══════════════════════════════════════════════════════════════
# SLIDE 6: MARKETPLACE SHIELD
# ═══════════════════════════════════════════════════════════════
bg_light(c)
title(c, "Visa Marketplace Shield — Escrow for P2P Commerce")

y = H - 3.5*cm
txt(c, "OLX, Vinted, FB Marketplace = ~15B PLN/year. No buyer protection today.", 2*cm, y, sz=12, bold=True, col=VD)
txt(c, "OLX, Vinted, FB Marketplace = ~15 mld PLN/rok. Dziś zero ochrony kupującego.", 2*cm, y - 0.6*cm, sz=9, col=GRY)

y -= 2*cm

# Flow
c.setFillColor(LB); c.roundRect(1.5*cm, y - 3.5*cm, W - 3*cm, 3.5*cm, 5, fill=1, stroke=0)
steps = [
    ("1. SCAN", "Buyer scans seller's\ncard QR code", "Kupujący skanuje\nQR karty sprzedawcy"),
    ("2. PAY", "Money charged to\nbuyer's card → ESCROW", "Kwota pobrana z karty\nkupującego → ESCROW"),
    ("3. RECEIVE", "Buyer receives item,\ninspects quality", "Kupujący odbiera towar,\nsprawdza jakość"),
    ("4. CONFIRM", "Tap 'Confirm' →\nmoney released to seller", "Kliknij 'Potwierdź' →\npieniądze do sprzedawcy"),
    ("5. DISPUTE?", "Full Visa chargeback\nprotection applies", "Pełna ochrona Visa\n(chargeback)"),
]
sx = 2*cm
for step_title, en, pl in steps:
    c.setFillColor(VB); c.setFont("Helvetica-Bold", 9)
    c.drawString(sx, y - 0.5*cm, step_title)
    c.setFillColor(DGRY); c.setFont("Helvetica", 7.5)
    for i, line in enumerate(en.split("\n")):
        c.drawString(sx, y - 1.2*cm - i*0.4*cm, line)
    c.setFillColor(LGRY); c.setFont("Helvetica", 6.5)
    for i, line in enumerate(pl.split("\n")):
        c.drawString(sx, y - 2.2*cm - i*0.35*cm, line)
    sx += 5*cm

y -= 5*cm
txt(c, "Key advantage vs BLIK P2P: BLIK transfer is instant & irreversible — if scammed, money is gone.", 2*cm, y, sz=9, bold=True, col=RED, mw=W-4*cm)
txt(c, "Visa Shield holds funds until both parties are satisfied. Trust = the differentiator.", 2*cm, y - 0.5*cm, sz=9, bold=True, col=GRN, mw=W-4*cm)

y -= 1.5*cm
kpi(c, 1.5*cm, y - 1.8*cm, 5*cm, 1.8*cm, "~15B PLN", "Marketplace TAM / year", VB)
kpi(c, 7*cm, y - 1.8*cm, 5*cm, 1.8*cm, "14M+", "OLX + Vinted users in PL", VB)
kpi(c, 12.5*cm, y - 1.8*cm, 5*cm, 1.8*cm, "1-2%", "Escrow fee (buyer pays)", VG)
kpi(c, 18*cm, y - 1.8*cm, 5*cm, 1.8*cm, "1.5-2.3B", "New card volume / year", GRN)
c.showPage()

# ═══════════════════════════════════════════════════════════════
# SLIDE 7: BUSINESS MODEL & PROJECTIONS
# ═══════════════════════════════════════════════════════════════
bg_light(c)
title(c, "Business Case / Model Biznesowy (Base Scenario)")

y = H - 3.5*cm

# KPIs row 1
kpi(c, 1.5*cm, y - 2*cm, 4.2*cm, 2*cm, "7.7M", "QR Pay adopters in 3 years", VB)
kpi(c, 6.2*cm, y - 2*cm, 4.2*cm, 2*cm, "18.2M", "Monthly TX at Year 3", VB)
kpi(c, 10.9*cm, y - 2*cm, 4.2*cm, 2*cm, "2.6B PLN", "Monthly volume at Year 3", VB)
kpi(c, 15.6*cm, y - 2*cm, 4.2*cm, 2*cm, "Month 16", "Break-even / Punkt rentowności", GRN)
kpi(c, 20.3*cm, y - 2*cm, 4.2*cm, 2*cm, "365%", "3-Year ROI", GRN)

y -= 3.5*cm

# Revenue table
rev_data = [
    ["", "Year 1", "Year 2", "Year 3", "Total"],
    ["Adopters", "2.3M", "6.1M", "7.7M", "—"],
    ["Monthly TX", "3.8M", "13.4M", "18.2M", "358M cum."],
    ["Monthly Value", "549M PLN", "1.9B PLN", "2.6B PLN", "51.6B cum."],
    ["Revenue", "12M PLN", "60M PLN", "77M PLN", "149M PLN"],
    ["Costs", "18M PLN", "8M PLN", "6M PLN", "32M PLN"],
    ["Profit", "-6M PLN", "+52M PLN", "+71M PLN", "+117M PLN"],
]
t = Table(rev_data, colWidths=[4*cm, 5*cm, 5*cm, 5*cm, 5*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), VB),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHT),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('GRID', (0, 0), (-1, -1), 0.4, HexColor("#CCCCCC")),
    ('PADDING', (0, 0), (-1, -1), 5),
    ('BACKGROUND', (0, -1), (-1, -1), HexColor("#E8F8F0")),
    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -2), [WHT, HexColor("#F7F8FA")]),
]))
t.wrapOn(c, W, H)
t.drawOn(c, 2*cm, y - 4.5*cm)

y -= 5.5*cm
txt(c, "~60% of QR Pay volume is NET NEW to Visa (from cash/transfers, not cannibalized from BLIK)", 2*cm, y, sz=9, bold=True, col=GRN, mw=W-4*cm)
txt(c, "~60% wolumenu QR Pay to NOWY wolumen dla Visa (z gotówki/przelewów, nie kanibalizacja BLIK)", 2*cm, y - 0.5*cm, sz=8, col=GRY, mw=W-4*cm)

y -= 1.3*cm
txt(c, "Models: Bass Diffusion adoption, per-user activity, BLIK cannibalization, ROI, sensitivity analysis", 2*cm, y, sz=7, col=LGRY, mw=W-4*cm)
c.showPage()

# ═══════════════════════════════════════════════════════════════
# SLIDE 8: CALL TO ACTION
# ═══════════════════════════════════════════════════════════════
bg_dark(c)
c.setFillColor(VG); c.setFont("Helvetica-Bold", 32)
c.drawString(2*cm, H - 4*cm, "CardFlow")

c.setFillColor(WHT); c.setFont("Helvetica", 15)
c.drawString(2*cm, H - 5.5*cm, "We turn transaction data into concrete decisions.")
c.setFont("Helvetica", 13); c.setFillColor(HexColor("#A0AAC0"))
c.drawString(2*cm, H - 6.5*cm, "Zamieniamy dane transakcyjne w konkretne decyzje.")

c.setFillColor(WHT); c.setFont("Helvetica-Bold", 12)
y = H - 8.5*cm
c.drawString(2*cm, y, "What we deliver:")
c.setFont("Helvetica", 10); c.setFillColor(HexColor("#D0D8F0"))
items = [
    "Visa QR Pay — 2 payment modes (P2P + e-commerce), no card number shared",
    "Visa Marketplace Shield — escrow for OLX/Vinted with Visa buyer protection",
    "6 predictive models with 3 scenarios — break-even month 16, 365% ROI",
    "Interactive Streamlit dashboard analyzing 305.5M transactions",
    "Data-backed gap analysis: Visa × GUS × NBP × Gemius",
]
for item in items:
    y -= 0.55*cm
    c.setFillColor(VG); c.drawString(2*cm, y, "\u25b8")
    c.setFillColor(HexColor("#D0D8F0")); c.drawString(2.4*cm, y, item)

c.setFillColor(VG); c.setFont("Helvetica-Bold", 12)
c.drawString(2*cm, 3.5*cm, "github.com/mariusz4908/visa-datasprint")

c.setFillColor(HexColor("#777777")); c.setFont("Helvetica", 9)
c.drawString(2*cm, 2.5*cm, "Live demo: Streamlit dashboard")
c.drawString(2*cm, 1.8*cm, "Team CardFlow — Visa DataSprint Hackathon 2026")

c.showPage()
c.save()
print(f"PDF saved: {OUT}")
