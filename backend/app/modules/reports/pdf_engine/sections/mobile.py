from reportlab.platypus import PageBreak, Spacer


def build_mobile(elements, renderer, styles, data):
    mobile_analysis = data.get("numerology_core", {}).get("mobile_analysis", {})
    mobile = data.get("mobile_remedies", {})

    if not mobile_analysis and not mobile:
        return

    elements.append(renderer.section_banner("Mobile Number Intelligence"))

    vibration = mobile_analysis.get("mobile_vibration", "N/A")
    status = str(mobile_analysis.get("compatibility_status", "neutral")).title()
    summary = mobile_analysis.get(
        "compatibility_summary",
        "Mobile vibration aapke day-to-day communication aur response pattern par subtle effect daalta hai.",
    )
    correction = mobile_analysis.get(
        "correction_suggestion",
        mobile.get("number_energy_hint", "Agar optimize karna ho to supportive ending energies consider ki ja sakti hain."),
    )

    elements.append(renderer.insight_box("Mobile Vibration", f"Vibration: {vibration} | Alignment: {status}", tone="info"))
    elements.append(Spacer(1, 8))
    elements.append(renderer.insight_box("Compatibility Insight", summary, tone="neutral"))
    elements.append(Spacer(1, 8))
    elements.append(renderer.insight_box("Correction Suggestion", correction, tone="success"))
    elements.append(Spacer(1, 8))

    usage = mobile.get("mobile_usage_timing", "Heavy decisions raat me avoid karein aur high-focus tasks morning me rakhein.")
    focus = mobile.get("whatsapp_dp", "Digital identity ko simple aur clear rakhein.")
    environment = mobile.get("charging_direction", "Phone charging spot ko stable aur clutter-free rakhein.")

    elements.append(renderer.bullet_block("Daily Digital Alignment", [usage, focus, environment]))

    elements.append(PageBreak())
