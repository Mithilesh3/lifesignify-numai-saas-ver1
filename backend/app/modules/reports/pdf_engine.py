from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np


# =====================================================
# FOOTER (Branding + Page Number)
# =====================================================
def add_footer(canvas, doc):
    page_num = canvas.getPageNumber()
    footer_text = f"Life Signify NumAI | Page {page_num}"
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(200 * mm, 10 * mm, footer_text)


# =====================================================
# WATERMARK (FREE USERS ONLY)
# =====================================================
def add_watermark(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 60)
    canvas.setFillGray(0.9, 0.3)
    canvas.rotate(45)
    canvas.drawCentredString(300, 100, "FREE VERSION")
    canvas.restoreState()


# =====================================================
# RADAR CHART GENERATOR (Investor Grade)
# =====================================================
def generate_radar_chart(radar_data):

    labels = list(radar_data.keys())
    values = list(radar_data.values())

    num_vars = len(labels)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    ax.set_ylim(0, 100)
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(
        [label.replace("_", " ").title() for label in labels],
        fontsize=9
    )

    ax.set_title("Life Performance Radar", size=14)

    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)

    return Image(buffer, width=4.5 * inch, height=4.5 * inch)


# =====================================================
# AI SUMMARY (Uses GPT if available, fallback safe)
# =====================================================
def get_ai_summary(content):

    ai_data = content.get("ai_narrative", {})
    ai_text = ai_data.get("ai_full_narrative")

    if ai_text:
        return ai_text

    # Fallback (if GPT fails)
    scores = content.get("executive_dashboard", {})
    stability = scores.get("life_stability_index", 50)
    financial = scores.get("financial_discipline_index", 50)

    return (
        f"This behavioral intelligence assessment indicates a life stability score of {stability}. "
        f"Financial discipline index is {financial}. Structured growth strategy is advised."
    )


# =====================================================
# MAIN PDF ENGINE
# =====================================================
def generate_report_pdf(report, is_premium=True):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    heading = styles["Heading1"]
    subheading = styles["Heading2"]
    normal = styles["BodyText"]

    content = report.content

    # =====================================================
    # COVER PAGE
    # =====================================================
    elements.append(Paragraph("Life Signify NumAI", heading))
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("Premium Behavioral Intelligence Report", subheading))
    elements.append(Spacer(1, 2 * inch))
    elements.append(Paragraph(f"Engine Version: {report.engine_version}", normal))
    elements.append(PageBreak())

    # =====================================================
    # AI SUMMARY PAGE
    # =====================================================
    elements.append(Paragraph("Executive AI Strategic Summary", subheading))
    elements.append(Spacer(1, 0.4 * inch))
    elements.append(Paragraph(get_ai_summary(content), normal))
    elements.append(PageBreak())

    # =====================================================
    # EXECUTIVE DASHBOARD
    # =====================================================
    elements.append(Paragraph("Executive Dashboard", subheading))
    elements.append(Spacer(1, 0.3 * inch))

    dashboard = content.get("executive_dashboard", {})
    data = [["Metric", "Score"]]

    for key, value in dashboard.items():
        data.append([key.replace("_", " ").title(), str(value)])

    table = Table(data, colWidths=[3.5 * inch, 1.5 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(PageBreak())

    # =====================================================
    # RADAR CHART
    # =====================================================
    radar_data = content.get("radar_chart_data", {})
    if radar_data:
        elements.append(Paragraph("Performance Radar Analysis", subheading))
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(generate_radar_chart(radar_data))
        elements.append(PageBreak())

    # =====================================================
    # ARCHETYPE
    # =====================================================
    elements.append(Paragraph("Archetype Intelligence", subheading))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph(content.get("archetype_hint", ""), normal))
    elements.append(Spacer(1, 0.5 * inch))

    # =====================================================
    # RISK ANALYSIS
    # =====================================================
    elements.append(Paragraph("Risk Analysis", subheading))
    elements.append(Spacer(1, 0.3 * inch))

    risk = content.get("risk_analysis", {})
    for key, value in risk.items():
        elements.append(
            Paragraph(f"{key.replace('_', ' ').title()}: {value}", normal)
        )

    elements.append(Spacer(1, 0.5 * inch))

    # =====================================================
    # REMEDY DIRECTION
    # =====================================================
    elements.append(Paragraph("Remedy Direction", subheading))
    elements.append(Spacer(1, 0.3 * inch))

    remedy = content.get("remedy_direction", {})
    for key, value in remedy.items():
        elements.append(
            Paragraph(f"{key.replace('_', ' ').title()}: {value}", normal)
        )

    # =====================================================
    # BUILD PDF (Premium vs Free Logic)
    # =====================================================
    if is_premium:
        doc.build(
            elements,
            onFirstPage=add_footer,
            onLaterPages=add_footer
        )
    else:
        doc.build(
            elements,
            onFirstPage=lambda c, d: (add_footer(c, d), add_watermark(c, d)),
            onLaterPages=lambda c, d: (add_footer(c, d), add_watermark(c, d))
        )

    buffer.seek(0)
    return buffer
