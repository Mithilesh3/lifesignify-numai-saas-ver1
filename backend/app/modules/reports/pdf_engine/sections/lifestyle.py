from reportlab.platypus import PageBreak, Spacer


def build_lifestyle(elements, renderer, styles, data):
    life = data.get("lifestyle_remedies", {})
    daily_alignment = data.get("daily_energy_alignment", {})

    if not life and not daily_alignment:
        return

    elements.append(renderer.section_banner("जीवन संतुलन मार्गदर्शन | Lifestyle Alignment"))

    if life:
        elements.append(renderer.insight_box("रंग संतुलन | Color Alignment", life.get("color_alignment", "Environment में balancing tones रखें।"), tone="info"))
        elements.append(Spacer(1, 8))

        habits = [
            life.get("daily_routine", "Daily consistency build करें।"),
            life.get("meditation", "हर दिन mindful reset practice करें।"),
            life.get("bracelet_suggestion", "Habit identity को reinforce करने के लिए symbolic anchors use करें।"),
            life.get("habit_recommendation", "ऐसा repeatable ritual बनाएं जो आपकी weakest area को support करे।"),
        ]
        elements.append(renderer.bullet_block("दैनिक आदतें | Daily Habits", habits))
        elements.append(Spacer(1, 8))

    if daily_alignment:
        alignment_points = [
            daily_alignment.get("morning", "Morning sunlight exposure लें।"),
            daily_alignment.get("breathing", "Short breathing routine करें।"),
            daily_alignment.get("focus_routine", "Focused work block से पहले clear intention set करें।"),
            daily_alignment.get("evening_reset", "Evening reset के साथ दिन close करें।"),
        ]
        elements.append(renderer.bullet_block("संतुलन रूटीन | Alignment Routine", alignment_points))
        elements.append(Spacer(1, 8))

    environment = "Environment, rhythm और routine को align रखने से numerology guidance practical daily action में convert होती है।"
    elements.append(renderer.insight_box("पर्यावरण संतुलन | Environment Alignment", environment, tone="neutral"))

    elements.append(PageBreak())
