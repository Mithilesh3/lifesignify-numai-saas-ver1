from reportlab.lib.colors import HexColor
from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle


def build_numerology(elements, renderer, styles, data):
    core = data.get("numerology_core", {})

    pythagorean = core.get("pythagorean", {})
    chaldean = core.get("chaldean", {})
    mobile = core.get("mobile_analysis", {})

    elements.append(renderer.section_banner("Core Numerology Architecture"))

    rows = [
        ["Life Path", pythagorean.get("life_path_number", "N/A"), "Life direction aur natural movement pattern"],
        ["Destiny", pythagorean.get("destiny_number", "N/A"), "Outer-world execution aur achievement style"],
        ["Expression", pythagorean.get("expression_number", "N/A"), "Communication aur talent expression pattern"],
        ["Name Number", chaldean.get("name_number", "N/A"), "Social vibration aur identity impact"],
        ["Mobile Vibration", mobile.get("mobile_vibration", "N/A"), "Daily communication signal aur device energy"],
    ]

    table_rows = [
        [
            Paragraph("<b>Number</b>", styles["BodyText"]),
            Paragraph("<b>Value</b>", styles["BodyText"]),
            Paragraph("<b>Interpretation</b>", styles["BodyText"]),
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

    table = Table(table_rows, colWidths=[100, 70, 300])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1b2f4b")),
                ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
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
        "Core numbers aapki identity aur execution ko dikhate hain, jabki mobile vibration daily communication pattern ko influence karta hai."
    )
    elements.append(renderer.insight_box("Interpretation Summary", compatibility_summary, tone="neutral"))

    elements.append(PageBreak())
