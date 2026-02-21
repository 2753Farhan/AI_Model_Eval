"""
AI Generated Solution
Task ID: HumanEval/104
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.269548
"""

def unique_digits(x):
    result = []
    for num in x:
        if all([digit % 2 != 0 for digit in str(num)]):
            result.append(num)
    return sorted(result)