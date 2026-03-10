from reportlab.platypus import PageBreak, Spacer

from ..blocks.radar_chart import radar_chart


def _pick(metrics, key, default=0):
    value = metrics.get(key, default)
    try:
        return int(value)
    except Exception:
        return default


def build_metrics(elements, renderer, styles, data):
    metrics = data.get("core_metrics", {})

    if not metrics:
        return

    elements.append(renderer.section_banner("मुख्य जीवन संकेतक | Intelligence Metrics"))

    confidence = _pick(metrics, "confidence_score")
    karma_pressure = _pick(metrics, "karma_pressure_index")
    life_stability = _pick(metrics, "life_stability_index")
    dharma_alignment = _pick(metrics, "dharma_alignment_score")
    emotional_regulation = _pick(metrics, "emotional_regulation_index")
    financial_discipline = _pick(metrics, "financial_discipline_index")

    metric_pairs = [
        ("विश्वास स्कोर | Confidence Score", confidence),
        ("कर्म दबाव | Karma Pressure Index", karma_pressure),
        ("जीवन स्थिरता | Life Stability", life_stability),
        ("धर्म संतुलन | Dharma Alignment", dharma_alignment),
        ("भावनात्मक संतुलन | Emotional Regulation", emotional_regulation),
        ("वित्तीय अनुशासन | Financial Discipline", financial_discipline),
    ]

    elements.append(renderer.metric_grid(metric_pairs))
    elements.append(Spacer(1, 8))

    radar_data = data.get("radar_chart_data") or {
        "Life Stability": life_stability,
        "Decision Clarity": confidence,
        "Dharma Alignment": dharma_alignment,
        "Emotional Regulation": emotional_regulation,
        "Financial Discipline": financial_discipline,
    }
    elements.append(radar_chart(radar_data, styles, renderer.full_width))
    elements.append(Spacer(1, 8))

    risk_band = metrics.get("risk_band", "Not classified")
    low_data_note = ""
    if confidence <= 25:
        low_data_note = (
            "<br/>व्यवहारिक और financial intake सीमित होने की वजह से कुछ indices neutral baseline पर हैं, "
            "इसलिए इन scores को directional संकेत की तरह पढ़ें।"
        )
    explanation = (
        f"Risk Band: <b>{risk_band}</b><br/>"
        f"Confidence {confidence}, Karma Pressure {karma_pressure}, Life Stability {life_stability}, "
        f"Dharma Alignment {dharma_alignment}, Emotional Regulation {emotional_regulation}, "
        f"Financial Discipline {financial_discipline}.{low_data_note}"
    )
    elements.append(renderer.insight_box("संकेतक व्याख्या | Metric Interpretation", explanation, tone="neutral"))

    elements.append(PageBreak())
