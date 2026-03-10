from reportlab.platypus import PageBreak, Spacer, Table, TableStyle

from ..assets import CHAKRA_ICON


def _shadow_traits(arch, metrics):
    stated_shadow = arch.get("shadow_traits") or arch.get("shadow")
    if stated_shadow:
        return stated_shadow

    behavior = arch.get("behavior_style", "adaptive")
    emotional = int(metrics.get("emotional_regulation_index", 50) or 50)
    finance = int(metrics.get("financial_discipline_index", 50) or 50)

    pressure_note = ""
    if emotional < 55:
        pressure_note += " Pressure में emotional reactivity decision quality को compress कर सकती है।"
    if finance < 55:
        pressure_note += " Explicit control rhythm के बिना financial execution drift कर सकता है।"

    return (
        f"{behavior.lower()} pattern possibility पर ज़्यादा और operating discipline पर कम ध्यान दे सकता है।"
        f"{pressure_note}"
    )


def _growth_path(arch, strategy):
    anchor = arch.get("core_archetype", "Adaptive Explorer")
    mid_term = strategy.get("mid_term", "Expansion से पहले structure install करें।")
    return (
        f"{anchor} के लिए growth path यह है कि पहले repeatable systems codify करें, फिर creative bets को phases में scale करें। "
        f"Execution focus: {mid_term}"
    )


def build_archetype(elements, renderer, styles, data):
    arch = data.get("numerology_archetype", {})

    if not arch:
        return

    elements.append(renderer.section_banner("मूल व्यक्तित्व प्रतिरूप | Archetype Intelligence"))

    title = arch.get("archetype_name", "Strategic Archetype")
    description = arch.get("description", "")
    elements.append(
        renderer.icon_block(
            CHAKRA_ICON,
            "मूल प्रतिरूप | Archetype Signature",
            f"<b>{title}</b><br/>{description}",
        )
    )
    elements.append(Spacer(1, 8))

    leadership_traits = "<br/>".join(
        [
            f"- Core Archetype: {arch.get('core_archetype', 'Adaptive')}",
            f"- Leadership Traits: {arch.get('behavior_style', 'Strategic and adaptive')}",
            "- Strength Pattern: uncertainty के बीच strategic direction",
        ]
    )

    shadow_traits = _shadow_traits(arch, data.get("core_metrics", {}))
    growth_path = _growth_path(arch, data.get("strategic_guidance", {}))

    cards = Table(
        [
            [renderer.insight_box("नेतृत्व संकेत | Leadership Traits", leadership_traits, tone="success")],
            [renderer.insight_box("छाया पक्ष | Shadow Traits", shadow_traits, tone="risk")],
            [renderer.insight_box("विकास पथ | Archetype Growth Path", growth_path, tone="neutral")],
        ],
        colWidths=[renderer.full_width],
    )
    cards.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )

    elements.append(cards)
    elements.append(PageBreak())
