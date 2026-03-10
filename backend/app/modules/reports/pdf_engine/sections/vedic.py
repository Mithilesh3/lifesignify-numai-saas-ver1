import re

from reportlab.platypus import Image, PageBreak, Spacer

from ..assets import DEITIES


DEITY_MAP = {
    "budh": "budh",
    "mercury": "budh",
    "surya": "surya",
    "sun": "surya",
    "chandra": "chandra",
    "moon": "chandra",
    "mangal": "mangal",
    "mars": "mangal",
    "guru": "guru",
    "jupiter": "guru",
    "shukra": "shukra",
    "venus": "shukra",
    "shani": "shani",
    "saturn": "shani",
    "rahu": "rahu",
    "ketu": "ketu",
}


def _deity_key(raw_name):
    cleaned = re.sub(r"[^a-zA-Z ]", " ", (raw_name or "").lower())
    parts = [part for part in cleaned.split() if part]
    for part in parts:
        if part in DEITY_MAP:
            return DEITY_MAP[part]
    return "budh"


def build_vedic(elements, renderer, styles, data):
    remedy = data.get("vedic_remedies")

    if not remedy:
        return

    elements.append(renderer.section_banner("Dynamic Vedic Remedies"))

    deity_name = remedy.get("deity", "Budh (Mercury)")
    key = _deity_key(deity_name)
    deity_path = DEITIES / f"{key}.png"

    if deity_path.exists():
        img = Image(str(deity_path), width=96, height=96)
        img.hAlign = "CENTER"
        elements.append(img)
        elements.append(Spacer(1, 8))

    elements.append(renderer.insight_box("Planetary Alignment", remedy.get("planetary_alignment", deity_name), tone="neutral"))
    elements.append(Spacer(1, 8))

    mantra = remedy.get("mantra_sanskrit", "")
    pronunciation = remedy.get("mantra_pronunciation", "")
    practice = remedy.get("practice_guideline", "")
    donation = remedy.get("recommended_donation", "")
    purpose = remedy.get("purpose", "Remedy ka purpose energy ko grounded aur disciplined direction dena hai.")

    elements.append(renderer.insight_box("Mantra", f"<b>{mantra}</b><br/>{pronunciation}", tone="info"))
    elements.append(Spacer(1, 8))
    elements.append(renderer.insight_box("Practice", practice, tone="neutral"))
    elements.append(Spacer(1, 8))
    elements.append(renderer.insight_box("Donation", donation, tone="success"))
    elements.append(Spacer(1, 8))
    elements.append(renderer.insight_box("Purpose", purpose, tone="neutral"))

    elements.append(PageBreak())
