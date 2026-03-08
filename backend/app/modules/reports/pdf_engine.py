import os
from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
    Table,
    TableStyle
)

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from app.modules.reports.charts_engine import generate_radar_chart
from app.modules.reports.table_engine import (
    render_core_numbers_table,
    render_loshu_grid
)

# =========================================================
# PATH CONFIG
# =========================================================

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
ASSETS = os.path.join(BASE_DIR, "assets")

LOGO = os.path.join(ASSETS, "branding", "logo.png")
KRISHNA = os.path.join(ASSETS, "cover", "krishna.png")
GANESHA = os.path.join(ASSETS, "cover", "ganesha.png")

MANDALA = os.path.join(ASSETS, "background", "mandala_bg.png")

# FIXED ICON PATH
YANTRA = os.path.join(ASSETS, "icons", "chakra.png")

DEITIES = os.path.join(ASSETS, "deities")

FONT_PATH = os.path.join(ASSETS, "fonts", "NotoSans-Regular.ttf")

# =========================================================
# FONT CONFIG
# =========================================================

if os.path.exists(FONT_PATH):
    pdfmetrics.registerFont(TTFont("NotoSans", FONT_PATH))
    BASE_FONT = "NotoSans"
else:
    BASE_FONT = "Helvetica"

# =========================================================
# COLORS
# =========================================================

PRIMARY = colors.HexColor("#1f3c88")
LIGHT_BOX = colors.HexColor("#f4f7ff")

# =========================================================
# SAFE TEXT
# =========================================================

def safe_text(value):

    if value is None:
        return "N/A"

    if isinstance(value, list):
        return "<br/>".join([f"• {str(v)}" for v in value])

    if isinstance(value, dict):

        lines = []

        for k, v in value.items():

            key = k.replace("_", " ").title()

            lines.append(f"<b>{key}</b>: {v}")

        return "<br/>".join(lines)

    return str(value)

# =========================================================
# HEADER / FOOTER
# =========================================================

def add_header_footer(canvas, doc):

    canvas.saveState()

    page = canvas.getPageNumber()

    if os.path.exists(LOGO):

        canvas.drawImage(
            LOGO,
            20 * mm,
            283 * mm,
            width=35 * mm,
            height=12 * mm,
            mask="auto"
        )

    canvas.setFont(BASE_FONT, 10)
    canvas.setFillColor(PRIMARY)

    canvas.drawString(
        60 * mm,
        287 * mm,
        "Life Signify NumAI Intelligence Report"
    )

    canvas.setFont(BASE_FONT, 9)
    canvas.setFillColor(colors.grey)

    canvas.drawRightString(
        200 * mm,
        10 * mm,
        f"Page {page}"
    )

    canvas.restoreState()

# =========================================================
# BACKGROUND
# =========================================================

def draw_background(canvas):

    if os.path.exists(MANDALA):

        canvas.saveState()

        canvas.setFillAlpha(0.05)

        canvas.drawImage(
            MANDALA,
            60,
            150,
            width=470,
            height=470,
            mask="auto"
        )

        canvas.restoreState()

# =========================================================
# WATERMARK
# =========================================================

def add_watermark(canvas):

    canvas.saveState()

    canvas.setFont(BASE_FONT, 60)
    canvas.setFillGray(0.9, 0.25)

    canvas.rotate(45)

    canvas.drawCentredString(
        300,
        100,
        "BASIC VERSION"
    )

    canvas.restoreState()

# =========================================================
# SECTION BANNER
# =========================================================

def render_section_banner(elements, title):

    banner = Table([[title]], colWidths=[460])

    banner.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), PRIMARY),
        ("TEXTCOLOR", (0,0), (-1,-1), colors.white),
        ("FONTNAME", (0,0), (-1,-1), BASE_FONT),
        ("FONTSIZE", (0,0), (-1,-1), 14),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ]))

    elements.append(banner)
    elements.append(Spacer(1,20))

# =========================================================
# KPI CARDS
# =========================================================

def render_kpi_cards(elements, metrics, styles):

    cards = []

    for k, v in metrics.items():

        title = k.replace("_", " ").title()

        card = Table(
            [
                [Paragraph(title, styles["BodyText"])],
                [Paragraph(f"<b>{v}</b>", styles["Title"])]
            ],
            colWidths=[120]
        )

        card.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), LIGHT_BOX),
            ("BOX", (0,0), (-1,-1), 0.4, colors.grey),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ]))

        cards.append(card)

    rows = [cards[i:i+3] for i in range(0, len(cards), 3)]

    table = Table(rows, colWidths=[160,160,160])

    elements.append(table)
    elements.append(Spacer(1,20))

# =========================================================
# INSIGHT CARD
# =========================================================

def render_insight_card(elements, title, text, styles):

    text = safe_text(text)

    card = Table(
        [
            [Paragraph(f"<b>{title}</b>", styles["BodyText"])],
            [Paragraph(text, styles["BodyText"])]
        ],
        colWidths=[460]
    )

    card.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), LIGHT_BOX),
        ("BOX", (0,0), (-1,-1), 0.4, colors.grey),
    ]))

    elements.append(card)
    elements.append(Spacer(1,14))

# =========================================================
# DEITY RENDER
# =========================================================

def render_deity(elements, deity_name):

    if not deity_name:
        return

    name = deity_name.split()[0].lower()

    path = os.path.join(DEITIES, f"{name}.png")

    if os.path.exists(path):

        elements.append(
            Image(
                path,
                width=120,
                height=120,
                hAlign="CENTER"
            )
        )

        elements.append(Spacer(1,20))

# =========================================================
# COVER PAGE
# =========================================================

def render_cover_page(elements, plan_tier, styles):

    cover = KRISHNA if plan_tier == "enterprise" else GANESHA

    if os.path.exists(LOGO):

        elements.append(Image(LOGO, width=160, height=70))
        elements.append(Spacer(1,30))

    elements.append(Paragraph("Life Signify NumAI", styles["Title"]))
    elements.append(Spacer(1,10))

    elements.append(
        Paragraph("Strategic Life Intelligence Report", styles["Heading2"])
    )

    elements.append(Spacer(1,35))

    if os.path.exists(cover):

        elements.append(
            Image(
                cover,
                width=260,
                height=260,
                hAlign="CENTER"
            )
        )

    elements.append(Spacer(1,40))

    elements.append(
        Paragraph(f"{plan_tier.upper()} Intelligence Report", styles["BodyText"])
    )

    elements.append(PageBreak())

# =========================================================
# MAIN PDF ENGINE
# =========================================================

def generate_report_pdf(report):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=80,
        bottomMargin=40
    )

    elements = []

    styles = getSampleStyleSheet()

    styles["BodyText"].fontName = BASE_FONT
    styles["Heading2"].fontName = BASE_FONT
    styles["Title"].fontName = BASE_FONT

    content = report.content or {}
    meta = content.get("meta", {})
    plan = meta.get("plan_tier", "basic")

    render_cover_page(elements, plan, styles)

    # Executive Summary
    executive = content.get("executive_brief")

    if executive:

        render_section_banner(elements, "Executive Intelligence Summary")

        for k, v in executive.items():

            render_insight_card(
                elements,
                k.replace("_", " ").title(),
                v,
                styles
            )

        elements.append(PageBreak())

    # Metrics
    metrics = content.get("core_metrics")

    if metrics:

        render_section_banner(elements, "Intelligence Metrics Dashboard")

        render_kpi_cards(elements, metrics, styles)

        radar = content.get("radar_chart_data")

        if radar:
            elements.append(generate_radar_chart(radar))

        elements.append(PageBreak())

    # Numerology
    render_section_banner(elements, "Core Numerology Architecture")

    if os.path.exists(YANTRA):
        elements.append(Image(YANTRA, width=100, height=100, hAlign="CENTER"))
        elements.append(Spacer(1,15))

    elements.append(render_core_numbers_table(content.get("numerology_core", {})))

    elements.append(PageBreak())

    # Lo Shu
    render_section_banner(elements, "Lo Shu Energy Grid")

    elements.append(
        render_loshu_grid(
            content.get("numerology_core", {}).get("loshu_grid", {})
        )
    )

    elements.append(PageBreak())

    # Behavioral Analysis
    analysis = content.get("analysis_sections")

    if analysis:

        render_section_banner(elements, "Behavioral Intelligence Analysis")

        for k, v in analysis.items():
            render_insight_card(elements, k.replace("_"," ").title(), v, styles)

        elements.append(PageBreak())

    # Business Intelligence
    business = content.get("business_block")

    if business:

        render_section_banner(elements, "Business Intelligence")

        for k, v in business.items():
            render_insight_card(elements, k.replace("_"," ").title(), v, styles)

        elements.append(PageBreak())

    # Strategic Guidance
    strategy = content.get("strategic_guidance")

    if strategy:

        render_section_banner(elements, "Strategic Guidance")

        for k, v in strategy.items():
            render_insight_card(elements, k.replace("_"," ").title(), v, styles)

        elements.append(PageBreak())

    # Growth Blueprint
    blueprint = content.get("growth_blueprint")

    if blueprint:

        render_section_banner(elements, "Growth Blueprint")

        for k, v in blueprint.items():
            render_insight_card(elements, k.replace("_"," ").title(), v, styles)

        elements.append(PageBreak())

    # Compatibility
    compatibility = content.get("compatibility_block")

    if compatibility:

        render_section_banner(elements, "Compatibility Intelligence")

        for k, v in compatibility.items():
            render_insight_card(elements, k.replace("_"," ").title(), v, styles)

        elements.append(PageBreak())

    # Lifestyle Remedies
    lifestyle = content.get("lifestyle_remedies")

    if lifestyle:

        render_section_banner(elements, "Lifestyle Alignment")

        for k, v in lifestyle.items():
            render_insight_card(elements, k.replace("_"," ").title(), v, styles)

        elements.append(PageBreak())

    # Mobile Remedies
    mobile = content.get("mobile_remedies")

    if mobile:

        render_section_banner(elements, "Mobile Energy Alignment")

        for k, v in mobile.items():
            render_insight_card(elements, k.replace("_"," ").title(), v, styles)

        elements.append(PageBreak())

    # Vedic Remedies
    vedic = content.get("vedic_remedies")

    if vedic:

        render_section_banner(elements, "Vedic Remedies")

        deity = vedic.get("deity")

        if deity:
            render_deity(elements, deity)

        for k, v in vedic.items():
            render_insight_card(elements, k.replace("_"," ").title(), v, styles)

        elements.append(PageBreak())

    # Archetype
    archetype = content.get("numerology_archetype")

    if archetype:

        render_section_banner(elements, "Numerology Archetype")

        for k, v in archetype.items():
            render_insight_card(elements, k.replace("_"," ").title(), v, styles)

        elements.append(PageBreak())

    # Build PDF

    if plan == "basic":

        doc.build(
            elements,
            onFirstPage=lambda c,d:(draw_background(c),add_header_footer(c,d),add_watermark(c)),
            onLaterPages=lambda c,d:(draw_background(c),add_header_footer(c,d),add_watermark(c))
        )

    else:

        doc.build(
            elements,
            onFirstPage=lambda c,d:(draw_background(c),add_header_footer(c,d)),
            onLaterPages=lambda c,d:(draw_background(c),add_header_footer(c,d))
        )

    buffer.seek(0)

    return buffer