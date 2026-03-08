# modules/numerology/chaldean.py

from typing import Dict


# =====================================================
# CHALDEAN LETTER MAP (Commercial Indian Standard)
# =====================================================

CHALDEAN_MAP = {
    1: "AIJQY",
    2: "BKR",
    3: "CGLS",
    4: "DMT",
    5: "EHNX",
    6: "UVW",
    7: "OZ",
    8: "FP"
}


# =====================================================
# INTERNAL LETTER VALUE
# =====================================================

def _letter_value(letter: str) -> int:
    letter = letter.upper()
    for number, letters in CHALDEAN_MAP.items():
        if letter in letters:
            return number
    return 0


# =====================================================
# NAME NUMBER
# =====================================================

def calculate_name_number(name: str) -> int:
    if not name:
        return 0

    total = sum(_letter_value(ch) for ch in name if ch.isalpha())

    while total > 9 and total not in (11, 22):
        total = sum(int(d) for d in str(total))

    return total


# =====================================================
# PUBLIC CONTRACT FUNCTION
# =====================================================

def generate_chaldean_numbers(identity: dict) -> dict:
    """
    Standardized output for orchestration layer.
    """
    name = identity.get("full_name", "")
    number = calculate_name_number(name)

    return {
        "name_number": number,
        "system": "chaldean"
    }