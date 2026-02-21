"""
AI Generated Solution
Task ID: HumanEval/71
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.223496
"""

def triangle_area(a, b, c):
    if a + b <= c or b + c <= a or a + c <= b:
        return -1
    else:
        s = (a + b + c) / 2
        return round(math.sqrt(s * (s - a) * (s - b) * (s - c)), 2)
