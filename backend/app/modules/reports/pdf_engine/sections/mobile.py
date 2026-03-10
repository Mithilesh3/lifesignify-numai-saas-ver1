from reportlab.platypus import PageBreak, Spacer


def build_mobile(elements, renderer, styles, data):
    mobile_analysis = data.get("numerology_core", {}).get("mobile_analysis", {})
    mobile = data.get("mobile_remedies", {})

    if not mobile_analysis and not mobile:
        return

    elements.append(renderer.section_banner("मोबाइल नंबर ऊर्जा विश्लेषण | Mobile Number Energy Analysis"))

    vibration = mobile_analysis.get("mobile_vibration", "N/A")
    status = str(mobile_analysis.get("compatibility_status", "neutral")).title()
    summary = mobile_analysis.get(
        "compatibility_summary",
        "Mobile vibration आपके day-to-day communication और response pattern पर subtle effect डालता है।",
    )
    correction = mobile_analysis.get(
        "correction_suggestion",
        mobile.get("number_energy_hint", "अगर optimize करना हो तो supportive ending energies consider की जा सकती हैं।"),
    )

    elements.append(renderer.insight_box("मोबाइल कंपन | Mobile Vibration", f"Vibration: {vibration} | Alignment: {status}", tone="info"))
    elements.append(Spacer(1, 8))
    elements.append(renderer.insight_box("अनुकूलता संकेत | Compatibility Insight", summary, tone="neutral"))
    elements.append(Spacer(1, 8))
    elements.append(renderer.insight_box("सुधार सुझाव | Correction Suggestion", correction, tone="success"))
    elements.append(Spacer(1, 8))

    usage = mobile.get("mobile_usage_timing", "Heavy decisions रात में avoid करें और high-focus tasks morning में रखें।")
    focus = mobile.get("whatsapp_dp", "Digital identity को simple और clear रखें।")
    environment = mobile.get("charging_direction", "Phone charging spot को stable और clutter-free रखें।")

    elements.append(renderer.bullet_block("दैनिक डिजिटल संतुलन | Daily Digital Alignment", [usage, focus, environment]))

    elements.append(PageBreak())
