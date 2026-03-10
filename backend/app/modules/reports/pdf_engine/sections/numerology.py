from reportlab.lib.colors import HexColor
from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle


def build_numerology(elements, renderer, styles, data):
    core = data.get("numerology_core", {})

    pythagorean = core.get("pythagorean", {})
    chaldean = core.get("chaldean", {})
    mobile = core.get("mobile_analysis", {})

    elements.append(renderer.section_banner("मूल अंक संरचना | Core Numerology Architecture"))

    rows = [
        ["जीवन पथ | Life Path", pythagorean.get("life_path_number", "N/A"), "जीवन की दिशा, natural movement, और core journey का संकेत"],
        ["भाग्यांक | Destiny", pythagorean.get("destiny_number", "N/A"), "Outer-world execution, achievement style, और role expression का संकेत"],
        ["अभिव्यक्ति | Expression", pythagorean.get("expression_number", "N/A"), "Communication, talent expression, और visible identity pattern"],
        ["नामांक | Name Number", chaldean.get("name_number", "N/A"), "Social vibration, identity impact, और public impression"],
        ["मोबाइल कंपन | Mobile Vibration", mobile.get("mobile_vibration", "N/A"), "Daily communication signal और device energy alignment"],
    ]

    table_rows = [
        [
            Paragraph("अंक | Number", styles["TableHeader"]),
            Paragraph("मान | Value", styles["TableHeader"]),
            Paragraph("अर्थ | Interpretation", styles["TableHeader"]),
        ]
    ]
    for label, value, interpretation in rows:
        table_rows.append(
            [
                Paragraph(str(label), styles["BodyText"]),
                Paragraph(str(value), styles["BodyText"]),
                Paragraph(str(interpretation), styles["BodyText"]),
            ]
        )

    table = Table(table_rows, colWidths=renderer.proportional_widths(1.35, 0.9, 3.85), repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1b2f4b")),
                ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                ("FONTNAME", (0, 0), (-1, 0), styles["TableHeader"].fontName),
                ("GRID", (0, 0), (-1, -1), 0.6, HexColor("#d1d8e0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elements.append(table)
    elements.append(Spacer(1, 8))

    compatibility_summary = mobile.get("compatibility_summary") or (
        "Core numbers आपकी identity और execution pattern को दिखाते हैं, जबकि mobile vibration daily communication tone को influence करता है।"
    )
    elements.append(renderer.insight_box("सार व्याख्या | Interpretation Summary", compatibility_summary, tone="neutral"))

    elements.append(PageBreak())
