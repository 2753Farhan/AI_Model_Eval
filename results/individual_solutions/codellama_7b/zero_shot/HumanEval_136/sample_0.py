"""
AI Generated Solution
Task ID: HumanEval/136
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.314646
"""

def largest_smallest_integers(my_list):
    largest_neg = None
    smallest_pos = None

    for num in my_list:
        if num < 0 and (largest_neg is None or num > largest_neg):
            largest_neg = num

        if num > 0 and (smallest_pos is None or num < smallest_pos):
            smallest_pos = num

    return (largest_neg, smallest_pos)