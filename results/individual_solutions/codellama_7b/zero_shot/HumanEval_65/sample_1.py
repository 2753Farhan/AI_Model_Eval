"""
AI Generated Solution
Task ID: HumanEval/65
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.214984
"""

def circular_shift(x, shift):
    if shift > len(str(x)):
        return str(x)[::-1]
    else:
        return str(x)[shift:] + str(x)[:shift]