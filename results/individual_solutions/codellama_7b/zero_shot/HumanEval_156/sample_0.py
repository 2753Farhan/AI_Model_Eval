"""
AI Generated Solution
Task ID: HumanEval/156
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.342669
"""

def int_to_mini_roman(number):
    if not 0 < number <= 1000:
        raise ValueError("Number must be between 1 and 1000")
    roman_numeral = ""
    for digit in str(number):
        roman_numeral += MINI_ROMAN_NUMERALS[int(digit)]
    return roman_numeral.lower()

MINI_ROMAN_NUMERALS = ["", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix"]