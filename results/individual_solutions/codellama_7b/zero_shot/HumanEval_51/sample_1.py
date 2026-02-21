"""
AI Generated Solution
Task ID: HumanEval/51
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.189868
"""

def remove_vowels(text):
    vowels = ['a', 'e', 'i', 'o', 'u']
    return ''.join([char for char in text if char.lower() not in vowels])