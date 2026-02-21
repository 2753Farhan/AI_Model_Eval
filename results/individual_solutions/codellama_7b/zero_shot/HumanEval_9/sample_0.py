"""
AI Generated Solution
Task ID: HumanEval/9
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.101368
"""

def rolling_max(numbers):
    max_so_far = numbers[0]
    max_ending_here = numbers[0]
    result = []
    for i in range(len(numbers)):
        max_ending_here = max(max_ending_here, numbers[i])
        result.append(max_ending_here)
        if max_so_far < max_ending_here:
            max_so_far = max_ending_here
    return result