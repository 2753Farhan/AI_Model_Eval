"""
Test for AI Generated Solution
Task ID: HumanEval/156
Model: codellama:7b
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

def check(candidate):

    # Check some simple cases
    assert candidate(19) == 'xix'
    assert candidate(152) == 'clii'
    assert candidate(251) == 'ccli'
    assert candidate(426) == 'cdxxvi'
    assert candidate(500) == 'd'
    assert candidate(1) == 'i'
    assert candidate(4) == 'iv'
    assert candidate(43) == 'xliii'
    assert candidate(90) == 'xc'
    assert candidate(94) == 'xciv'
    assert candidate(532) == 'dxxxii'
    assert candidate(900) == 'cm'
    assert candidate(994) == 'cmxciv'
    assert candidate(1000) == 'm'

    # Check some edge cases that are easy to work out by hand.
    assert True

