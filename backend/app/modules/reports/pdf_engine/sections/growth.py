from reportlab.platypus import PageBreak, Spacer, Table, TableStyle


def build_growth(elements, renderer, styles, data):
    growth = data.get("growth_blueprint", {})

    if not growth:
        return

    elements.append(renderer.section_banner("विकास खाका | Growth Blueprint"))

    cards = [
        renderer.insight_box("स्थिरीकरण | Stabilization", growth.get("phase_1", "Core systems को stabilize करें।"), tone="neutral"),
        renderer.insight_box("संतुलन | Alignment", growth.get("phase_2", "Execution को strategy के साथ align करें।"), tone="info"),
        renderer.insight_box("विस्तार | Expansion", growth.get("phase_3", "Governance के साथ scale करें।"), tone="success"),
    ]

    grid = Table([cards], colWidths=renderer.three_col_widths)
    grid.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )

    elements.append(grid)
    elements.append(Spacer(1, 8))

    elements.append(renderer.insight_box("क्रियान्वयन नोट | Execution Note", "अगले phase में तभी जाएं जब current metrics stabilize हो जाएं।", tone="neutral"))

    elements.append(PageBreak())

