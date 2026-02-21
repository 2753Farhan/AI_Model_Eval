"""
AI Generated Solution
Task ID: HumanEval/128
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.300619
"""

def prod_signs(arr):
    if not arr:
        return None
    product = 1
    for num in arr:
        sign = 1 if num > 0 else -1 if num < 0 else 0
        product *= sign
    return sum([abs(num) for num in arr]) * product