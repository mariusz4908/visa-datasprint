"""Generate CardFlow presentation PDF — 10 slides, bilingual PL/EN."""
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
import os

W, H = landscape(A4)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CardFlow_Presentation.pdf")

VISA_BLUE = HexColor("#1A1F71")
VISA_GOLD = HexColor("#F7B600")
LIGHT_BG = HexColor("#F0F4FF")
DARK = HexColor("#0D1137")
RED = HexColor("#E85D75")
GREEN = HexColor("#2ECC71")
GRAY = HexColor("#666666")
BLIK = HexColor("#D40E6A")

class PresentationCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slide_num = 0

    def showPage(self):
        self.slide_num += 1
        super().showPage()


def draw_slide_bg(c, title_bar=True, color=VISA_BLUE):
    c.saveState()
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    if title_bar:
        c.setFillColor(color)
        c.rect(0, H - 2.5*cm, W, 2.5*cm, fill=1, stroke=0)
        # Gold accent line
        c.setFillColor(VISA_GOLD)
        c.rect(0, H - 2.5*cm - 3, W, 3, fill=1, stroke=0)
    # Footer
    c.setFillColor(HexColor("#F7F8FA"))
    c.rect(0, 0, W, 1.2*cm, fill=1, stroke=0)
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8)
    c.drawString(1*cm, 0.4*cm, "CardFlow — Visa DataSprint Hackathon 2026")
    c.drawRightString(W - 1*cm, 0.4*cm, f"Slide {c.slide_num + 1} / 10")
    c.restoreState()


def title_text(c, text, y=None, size=24, color=white):
    if y is None:
        y = H - 1.8*cm
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", size)
    c.drawString(1.5*cm, y, text)


def body_text(c, text, x, y, size=12, color=black, font="Helvetica", max_width=None):
    c.setFillColor(color)
    c.setFont(font, size)
    if max_width:
        words = text.split()
        line = ""
        for word in words:
            test = line + " " + word if line else word
            if c.stringWidth(test, font, size) > max_width:
                c.drawString(x, y, line)
                y -= size * 1.4
                line = word
            else:
                line = test
        if line:
            c.drawString(x, y, line)
        return y - size * 1.4
    else:
        c.drawString(x, y, text)
        return y - size * 1.4


def bullet_list(c, items, x, y, size=11, indent=15, color=black):
    for item in items:
        c.setFillColor(VISA_GOLD)
        c.setFont("Helvetica-Bold", size)
        c.drawString(x, y, "\u25b8")
        y = body_text(c, item, x + indent, y, size=size, color=color, max_width=W/2 - 2*cm)
        y -= 2
    return y


def kpi_box(c, x, y, w, h, value, label, color=VISA_BLUE):
    c.setFillColor(HexColor("#F0F4FF"))
    c.roundRect(x, y, w, h, 5, fill=1, stroke=0)
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(x + w/2, y + h - 28, value)
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8)
    c.drawCentredString(x + w/2, y + 8, label)


c = PresentationCanvas(OUT, pagesize=landscape(A4))

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 1: TITLE
# ═══════════════════════════════════════════════════════════════════════
c.setFillColor(DARK)
c.rect(0, 0, W, H, fill=1, stroke=0)
# Gold circle accent
c.setFillColor(HexColor("#F7B60020"))
c.circle(W - 5*cm, H - 4*cm, 8*cm, fill=1, stroke=0)

c.setFillColor(white)
c.setFont("Helvetica-Bold", 36)
c.drawString(2*cm, H - 5*cm, "CardFlow")
c.setFont("Helvetica", 16)
c.setFillColor(HexColor("#CCCCCC"))
c.drawString(2*cm, H - 6.2*cm, "Transaction data as a roadmap for card adoption")
c.drawString(2*cm, H - 7.2*cm, "in e-commerce & P2P payments")

c.setFillColor(VISA_GOLD)
c.roundRect(2*cm, H - 9*cm, 10*cm, 1*cm, 5, fill=1, stroke=0)
c.setFillColor(DARK)
c.setFont("Helvetica-Bold", 11)
c.drawCentredString(7*cm, H - 8.65*cm, "VISA DATASPRINT HACKATHON 2026")

c.setFillColor(HexColor("#888888"))
c.setFont("Helvetica", 10)
c.drawString(2*cm, 2*cm, "Dane transakcyjne jako mapa drogowa popularyzacji kart w e-commerce i platno\u015bciach P2P")
c.drawString(2*cm, 1.2*cm, "Data sources: Visa (305.5M tx) | GUS | NBP | Gemius")
c.showPage()

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 2: THE PROBLEM
# ═══════════════════════════════════════════════════════════════════════
draw_slide_bg(c)
title_text(c, "The Problem / Problem")

y = H - 4*cm
y = body_text(c, "Cards dominate physical POS (58%) but lose in e-commerce (16%) and P2P (~2%).", 2*cm, y, size=13, font="Helvetica-Bold", color=VISA_BLUE, max_width=W-4*cm)
y -= 0.3*cm
y = body_text(c, "Karty dominuja w POS fizycznym (58%), ale przegrywaja w e-commerce (16%) i P2P (~2%).", 2*cm, y, size=11, color=GRAY, max_width=W-4*cm)
y -= 0.8*cm

# KPI boxes
kpi_box(c, 2*cm, y - 2.5*cm, 4*cm, 2.5*cm, "67%", "BLIK e-commerce share", BLIK)
kpi_box(c, 7*cm, y - 2.5*cm, 4*cm, 2.5*cm, "16%", "Card e-commerce share", VISA_BLUE)
kpi_box(c, 12*cm, y - 2.5*cm, 4*cm, 2.5*cm, "55%", "BLIK P2P share", BLIK)
kpi_box(c, 17*cm, y - 2.5*cm, 4*cm, 2.5*cm, "~2%", "Card P2P share", RED)
kpi_box(c, 22*cm, y - 2.5*cm, 4*cm, 2.5*cm, "45%", "Cash at small tx (<10 PLN)", RED)

y -= 4*cm
bullet_list(c, [
    "The same person taps Visa at a grocery store but uses BLIK online",
    "BLIK grew from 55% to 67% in e-commerce in just 2 years (2022-2024)",
    "Cards are losing -2pp/year in online payments",
    "25% of household spending (rent, telecom, education) is invisible to cards",
    "Services (doctors, plumbers, tutors) = 90%+ cash",
], 2*cm, y, size=10)
c.showPage()

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 3: DATA & METHODOLOGY
# ═══════════════════════════════════════════════════════════════════════
draw_slide_bg(c)
title_text(c, "Data & Methodology / Dane i Metodologia")

y = H - 4*cm
data_table = [
    ["Source / Zrodlo", "Description", "Records"],
    ["Visa Synthetic TX", "Anonymized card transactions, Jan 2025 - Jun 2026", "305.5M"],
    ["GUS Household Budget", "COICOP spending structure (12 categories)", "2024"],
    ["NBP Payment Stats", "Card/cash/BLIK shares, terminal counts", "2024"],
    ["Gemius E-Commerce", "Online payment method breakdown", "2024"],
    ["GUS BDL API", "Population by region (voivodeship/powiat)", "37.5M pop"],
]
t = Table(data_table, colWidths=[6*cm, 12*cm, 4*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), VISA_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BACKGROUND', (0, 1), (-1, -1), LIGHT_BG),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
    ('PADDING', (0, 0), (-1, -1), 6),
]))
t.wrapOn(c, W, H)
t.drawOn(c, 2*cm, y - 4.5*cm)

y -= 6*cm
body_text(c, "Methodology: Cross-reference GUS spending structure (COICOP) with Visa MCC categories.", 2*cm, y, size=10, font="Helvetica-Bold", color=VISA_BLUE)
y -= 0.6*cm
body_text(c, "Gap Index = (Visa value share / GUS spending share) x 100. Below 100 = cards underused.", 2*cm, y, size=10, color=GRAY)
y -= 0.6*cm
body_text(c, "Compliance: All analyses on groups of 30+ cards. 3/75 rule observed. No individual identification.", 2*cm, y, size=10, color=GRAY)
c.showPage()

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 4: KEY FINDINGS — CARD-FREE ZONES
# ═══════════════════════════════════════════════════════════════════════
draw_slide_bg(c)
title_text(c, "Key Findings: Card-Free Zones / Strefy bez Kart")

y = H - 4*cm
gap_table = [
    ["Category", "GUS %", "Visa %", "Gap Index", "Status"],
    ["Housing & Utilities", "20.6%", "0.3%", "2", "CARD-FREE ZONE"],
    ["Communications", "4.0%", "~0%", "~1", "CARD-FREE ZONE"],
    ["Education", "1.1%", "0.03%", "3", "CARD-FREE ZONE"],
    ["Healthcare (services)", "5.5%", "2.5%", "46", "UNDERUSED"],
    ["Alcohol & Tobacco", "2.5%", "0.8%", "32", "VERY UNDERUSED"],
    ["Home Furnishings", "4.4%", "2.6%", "59", "UNDERUSED"],
    ["Food & Groceries", "27.1%", "25.3%", "93", "WELL COVERED"],
    ["Restaurants & Hotels", "5.7%", "9.6%", "168", "OVERREPRESENTED"],
]
t = Table(gap_table, colWidths=[5.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 5*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), VISA_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BACKGROUND', (0, 1), (-1, 3), HexColor("#FFF0F2")),
    ('BACKGROUND', (0, 4), (-1, 6), HexColor("#FFF8F0")),
    ('BACKGROUND', (0, 7), (-1, 8), HexColor("#F0FFF5")),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
    ('PADDING', (0, 0), (-1, -1), 5),
]))
t.wrapOn(c, W, H)
t.drawOn(c, 3*cm, y - 5.5*cm)

y -= 7*cm
body_text(c, "~25% of household budgets (housing + telecom) flows through bank transfers — invisible to cards.", 2*cm, y, size=11, font="Helvetica-Bold", color=RED)
c.showPage()

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 5: E-COMMERCE & BLIK
# ═══════════════════════════════════════════════════════════════════════
draw_slide_bg(c)
title_text(c, "E-Commerce: BLIK vs Visa / BLIK vs Visa w E-Commerce")

y = H - 4*cm
body_text(c, "BLIK dominates Polish e-commerce and is growing. Cards are declining.", 2*cm, y, size=12, font="Helvetica-Bold", color=BLIK)

y -= 1.2*cm
ecom_table = [
    ["Method", "2022", "2023", "2024", "Trend"],
    ["BLIK", "55%", "62%", "67%", "+12pp in 2 years"],
    ["Card (Visa/MC)", "20%", "18%", "16%", "-4pp in 2 years"],
    ["Bank Transfer", "15%", "12%", "10%", "Declining"],
    ["Cash on Delivery", "8%", "6%", "5%", "Declining"],
]
t = Table(ecom_table, colWidths=[5*cm, 3*cm, 3*cm, 3*cm, 5*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), VISA_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BACKGROUND', (0, 1), (-1, 1), HexColor("#FCEDF3")),
    ('BACKGROUND', (0, 2), (-1, 2), HexColor("#E8F0FE")),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
    ('PADDING', (0, 0), (-1, -1), 6),
]))
t.wrapOn(c, W, H)
t.drawOn(c, 3*cm, y - 3.5*cm)

y -= 5.5*cm
body_text(c, "Visa's moat: international subscriptions (Apple, Netflix, Spotify, ChatGPT) = ~8M tx on card rails", 2*cm, y, size=10, font="Helvetica-Bold", color=GREEN)
y -= 0.6*cm
body_text(c, "E-grocery: 26% of card tx but only 0.12% online. Online avg = 402 vs 131 in-store (3.1x higher).", 2*cm, y, size=10, color=GRAY)
y -= 0.6*cm
body_text(c, "Projection: at -2pp/year, card share could fall below 10% by 2027 without intervention.", 2*cm, y, size=10, font="Helvetica-Bold", color=RED)
c.showPage()

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 6: VISA QR PAY — CONCEPT
# ═══════════════════════════════════════════════════════════════════════
draw_slide_bg(c, color=DARK)
title_text(c, "Our Solution: Visa QR Pay / Nasze Rozwiazanie")

y = H - 4*cm
body_text(c, "Every Visa card gets a unique QR code. Scan it to initiate a payment.", 2*cm, y, size=13, font="Helvetica-Bold", color=VISA_BLUE, max_width=W-4*cm)
y -= 0.5*cm
body_text(c, "No card number shared. Tokenized. Biometric approval. Powered by Visa Direct.", 2*cm, y, size=11, color=GRAY, max_width=W-4*cm)

y -= 1.5*cm
# Two columns
body_text(c, "MODE 1: P2P Payment Request", 2*cm, y, size=12, font="Helvetica-Bold", color=VISA_BLUE)
y1 = bullet_list(c, [
    "Friend scans your card's QR code",
    "Enters amount + description",
    "You get push notification on phone",
    "Approve with biometrics (Face ID)",
    "Money moves via Visa Direct — instant",
], 2*cm, y - 0.6*cm, size=9)

body_text(c, "MODE 2: E-Commerce Checkout", W/2 + 1*cm, y, size=12, font="Helvetica-Bold", color=VISA_GOLD)
bullet_list(c, [
    "At checkout, choose 'Visa QR Pay'",
    "Scan YOUR card with phone/webcam",
    "Approve push notification (biometric)",
    "Done — no card number typed ever",
    "Faster than BLIK, works globally",
], W/2 + 1*cm, y - 0.6*cm, size=9)

y2 = y1 - 1*cm
body_text(c, "Use cases: split bills, OLX/Vinted payments, pay the plumber, group collections, online shopping", 2*cm, y2, size=9, font="Helvetica-Bold", color=GREEN, max_width=W-4*cm)
c.showPage()

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 7: VISA QR PAY — VS BLIK
# ═══════════════════════════════════════════════════════════════════════
draw_slide_bg(c)
title_text(c, "Visa QR Pay vs BLIK — Comparison")

y = H - 4*cm
comp_table = [
    ["Feature", "Traditional Card", "BLIK", "Visa QR Pay"],
    ["Steps to pay online", "5-7 (type number)", "3-4 (code + confirm)", "2-3 (scan + approve)"],
    ["Card number exposed", "YES", "No (different system)", "NO (tokenized)"],
    ["Works internationally", "Yes", "Poland only", "Yes (global Visa)"],
    ["P2P payments", "Not supported", "55% market share", "Full support"],
    ["Works with dead phone", "Yes (type number)", "No", "Yes (QR on card)"],
    ["Laptop checkout", "Type number", "Needs phone app", "Webcam scans QR"],
    ["Buyer protection", "Full Visa", "Limited", "Full Visa"],
    ["Authentication", "3D Secure redirect", "Bank app confirm", "Biometric push"],
]
t = Table(comp_table, colWidths=[4.5*cm, 5*cm, 5*cm, 5.5*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), VISA_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8.5),
    ('BACKGROUND', (3, 1), (3, -1), HexColor("#E8F0FE")),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
    ('PADDING', (0, 0), (-1, -1), 5),
    ('FONTNAME', (3, 1), (3, -1), 'Helvetica-Bold'),
]))
t.wrapOn(c, W, H)
t.drawOn(c, 2.5*cm, y - 5.5*cm)
c.showPage()

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 8: PREDICTIVE MODELS
# ═══════════════════════════════════════════════════════════════════════
draw_slide_bg(c)
title_text(c, "Predictive Models / Modele Predykcyjne")

y = H - 4*cm
body_text(c, "6 models, 3 scenarios, 36-month projection", 2*cm, y, size=12, font="Helvetica-Bold", color=VISA_BLUE)

y -= 1.2*cm
model_table = [
    ["Model", "Method", "Key Output"],
    ["1. Adoption S-Curve", "Bass Diffusion (p,q)", "7.7M adopters in 3 years (Base)"],
    ["2. Transaction Volume", "Per-user activity model", "18.2M tx/month at Y3"],
    ["3. BLIK Cannibalization", "Source attribution", "~60% net new to Visa (Base)"],
    ["4. Revenue & ROI", "Fee model + cost structure", "Break-even M16, ROI 365%"],
    ["5. E-Com Market Share", "Share simulation", "Visa: 8.8% -> 15%+ (Base)"],
    ["6. Sensitivity", "Tornado analysis", "Virality (q) = #1 driver"],
]
t = Table(model_table, colWidths=[5*cm, 5*cm, 8*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), VISA_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9.5),
    ('BACKGROUND', (0, 1), (-1, -1), LIGHT_BG),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
    ('PADDING', (0, 0), (-1, -1), 6),
]))
t.wrapOn(c, W, H)
t.drawOn(c, 3*cm, y - 5*cm)

y -= 6.5*cm
kpi_box(c, 2*cm, y - 2*cm, 5*cm, 2*cm, "M16", "Break-even month", GREEN)
kpi_box(c, 8*cm, y - 2*cm, 5*cm, 2*cm, "365%", "3-year ROI (Base)", GREEN)
kpi_box(c, 14*cm, y - 2*cm, 5*cm, 2*cm, "149M PLN", "3Y Revenue (Base)", VISA_BLUE)
kpi_box(c, 20*cm, y - 2*cm, 5*cm, 2*cm, "~35B PLN", "New annual card volume", VISA_GOLD)
c.showPage()

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 9: RECOMMENDATIONS
# ═══════════════════════════════════════════════════════════════════════
draw_slide_bg(c)
title_text(c, "Recommendations / Rekomendacje")

y = H - 4*cm

body_text(c, "FOR ONLINE MERCHANTS:", 2*cm, y, size=11, font="Helvetica-Bold", color=VISA_BLUE)
y = bullet_list(c, [
    "Implement Visa Click to Pay / QR Pay at checkout",
    "E-grocery: card-first checkout for delivery platforms",
    "Highlight Visa buyer protection for high-value purchases",
], 2*cm, y - 0.4*cm, size=9)

y -= 0.5*cm
body_text(c, "FOR BANKS & VISA:", 2*cm, y, size=11, font="Helvetica-Bold", color=VISA_BLUE)
y = bullet_list(c, [
    "Launch Visa Direct P2P via QR in banking apps",
    "Card-on-file for recurring bills (rent, telecom) with cashback",
    "Tap-to-Phone rollout for service providers (doctors, tradesmen)",
    "Zero-fee micro-transactions under 10 PLN",
], 2*cm, y - 0.4*cm, size=9)

y -= 0.5*cm
body_text(c, "FOR CITIES:", 2*cm, y, size=11, font="Helvetica-Bold", color=VISA_BLUE)
y = bullet_list(c, [
    "Cashless City pilot (e.g., Krakow) — markets, parking, transport",
    "Tap-to-Phone for market vendors, food trucks, local services",
], 2*cm, y - 0.4*cm, size=9)

# Right column
body_text(c, "ROLLOUT PLAN:", W/2 + 1*cm, H - 4*cm, size=11, font="Helvetica-Bold", color=VISA_GOLD)
phases = [
    "M0-3: Pilot with 2-3 banks, QR in app",
    "M3-6: QR stickers to all cardholders",
    "M6-12: Merchant SDK, top 50 e-commerce",
    "M12-18: QR on all new Visa cards",
    "M18-24: International rollout (EU)",
]
bullet_list(c, phases, W/2 + 1*cm, H - 4.8*cm, size=9)
c.showPage()

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 10: SUMMARY & CALL TO ACTION
# ═══════════════════════════════════════════════════════════════════════
c.setFillColor(DARK)
c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFillColor(HexColor("#F7B60015"))
c.circle(W - 6*cm, 5*cm, 10*cm, fill=1, stroke=0)

c.setFillColor(VISA_GOLD)
c.setFont("Helvetica-Bold", 28)
c.drawString(2*cm, H - 4*cm, "CardFlow")

c.setFillColor(white)
c.setFont("Helvetica", 16)
c.drawString(2*cm, H - 5.5*cm, "We turn transaction data into concrete decisions.")
c.drawString(2*cm, H - 6.5*cm, "We show not just how people pay,")
c.drawString(2*cm, H - 7.5*cm, "but what to do to make the card their best choice.")

c.setFillColor(HexColor("#AAAAAA"))
c.setFont("Helvetica", 12)
c.drawString(2*cm, H - 9.5*cm, "Zamieniamy dane transakcyjne w konkretne decyzje.")
c.drawString(2*cm, H - 10.5*cm, "Pokazujemy nie tylko jak ludzie placa, ale co zrobic,")
c.drawString(2*cm, H - 11.5*cm, "zeby karta byla najwygodniejszym wyborem.")

c.setFillColor(VISA_GOLD)
c.setFont("Helvetica-Bold", 14)
c.drawString(2*cm, 3*cm, "github.com/mariusz4908/visa-datasprint")
c.setFillColor(HexColor("#888888"))
c.setFont("Helvetica", 10)
c.drawString(2*cm, 2*cm, "Live demo: Streamlit Cloud (link in README)")
c.drawString(2*cm, 1.2*cm, "Visa DataSprint Hackathon 2026 | Team CardFlow")

c.showPage()
c.save()
print(f"PDF saved: {OUT}")
