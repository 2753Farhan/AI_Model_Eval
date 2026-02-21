"""
Test for AI Generated Solution
Task ID: HumanEval/51
Model: codellama:7b
"""

def remove_vowels(text):
    vowels = ['a', 'e', 'i', 'o', 'u']
    return ''.join([char for char in text if char.lower() not in vowels])



METADATA = {}


def check(candidate):
    assert candidate('') == ''
    assert candidate("abcdef\nghijklm") == 'bcdf\nghjklm'
    assert candidate('fedcba') == 'fdcb'
    assert candidate('eeeee') == ''
    assert candidate('acBAA') == 'cB'
    assert candidate('EcBOO') == 'cB'
    assert candidate('ybcd') == 'ybcd'

