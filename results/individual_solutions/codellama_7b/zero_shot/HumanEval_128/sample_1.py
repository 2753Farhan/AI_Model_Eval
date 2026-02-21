"""
AI Generated Solution
Task ID: HumanEval/128
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.302123
"""

def prod_signs(arr):
    if not arr:
        return None
    product = 1
    for num in arr:
        sign = 1 if num > 0 else -1 if num < 0 else 0
        product *= sign
    return product * sum(abs(num) for num in arr)