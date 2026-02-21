"""
AI Generated Solution
Task ID: HumanEval/156
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.342669
"""

def int_to_mini_roman(number):
    if number < 1 or number > 1000:
        raise ValueError("Number must be between 1 and 1000")

    roman_numerals = ['m', 'cm', 'd', 'cd', 'c', 'xc', 'l', 'xl', 'x', 'ix', 'v', 'iv', 'i']
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]

    roman_numeral = ''
    for i in range(len(values)):
        while number >= values[i]:
            number -= values[i]
            roman_numeral += roman_numerals[i]

    return roman_numeral


# Test cases:
print(int_to_mini_roman(19))  # xix
print(int_to_mini_roman(152))  # clxxii
print(int_to_mini_roman(426))  # cdxxvi
print(int_to_mini_roman(1000))  # m