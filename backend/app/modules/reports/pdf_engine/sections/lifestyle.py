from reportlab.platypus import PageBreak, Spacer


def build_lifestyle(elements, renderer, styles, data):
    life = data.get("lifestyle_remedies", {})
    daily_alignment = data.get("daily_energy_alignment", {})

    if not life and not daily_alignment:
        return

    elements.append(renderer.section_banner("Daily Energy Alignment"))

    if life:
        elements.append(renderer.insight_box("Color Alignment", life.get("color_alignment", "Use balancing tones in your environment."), tone="info"))
        elements.append(Spacer(1, 8))

        habits = [
            life.get("daily_routine", "Build daily consistency."),
            life.get("meditation", "Practice mindful reset each day."),
            life.get("bracelet_suggestion", "Use symbolic anchors to reinforce habit identity."),
            life.get("habit_recommendation", "Ek repeatable ritual banayein jo aapki weakest area ko support kare."),
        ]
        elements.append(renderer.bullet_block("Daily Habits", habits))
        elements.append(Spacer(1, 8))

    if daily_alignment:
        alignment_points = [
            daily_alignment.get("morning", "Morning sunlight exposure lein."),
            daily_alignment.get("breathing", "Short breathing routine karein."),
            daily_alignment.get("focus_routine", "Focused work block se pehle clear intention set karein."),
            daily_alignment.get("evening_reset", "Evening reset ke saath din close karein."),
        ]
        elements.append(renderer.bullet_block("Alignment Routine", alignment_points))
        elements.append(Spacer(1, 8))

    environment = "Environment, rhythm aur routine ko align rakhne se numerology guidance practical daily action me convert hoti hai."
    elements.append(renderer.insight_box("Environment Alignment", environment, tone="neutral"))

    elements.append(PageBreak())
