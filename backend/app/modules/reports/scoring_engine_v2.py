def generate_score_summary_v2(flat_data):

    base_score = 60

    # More aggressive weighting
    financial = flat_data.get("savings_ratio", 50)
    stress = flat_data.get("stress_level", 50)

    life_stability_index = base_score + (financial * 0.2) - (stress * 0.3)

    emotional_regulation_index = 70 - flat_data.get("anxiety", 20)

    financial_discipline_index = 50 + (financial * 0.4)

    decision_clarity_score = 60 - flat_data.get("decision_confusion", 20)

    dharma_alignment_score = 75

    karma_pressure_index = 100 - life_stability_index

    return {
        "life_stability_index": int(max(0, min(100, life_stability_index))),
        "emotional_regulation_index": int(max(0, min(100, emotional_regulation_index))),
        "financial_discipline_index": int(max(0, min(100, financial_discipline_index))),
        "decision_clarity_score": int(max(0, min(100, decision_clarity_score))),
        "dharma_alignment_score": dharma_alignment_score,
        "karma_pressure_index": int(max(0, min(100, karma_pressure_index))),
    }
