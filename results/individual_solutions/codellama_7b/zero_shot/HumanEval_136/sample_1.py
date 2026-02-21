"""
AI Generated Solution
Task ID: HumanEval/136
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.314646
"""

def largest_smallest_integers(lst):
    smallest_positive = None
    largest_negative = None

    for i in lst:
        if i > 0 and (smallest_positive is None or i < smallest_positive):
            smallest_positive = i
        elif i < 0 and (largest_negative is None or i > largest_negative):
            largest_negative = i

    return (largest_negative, smallest_positive)