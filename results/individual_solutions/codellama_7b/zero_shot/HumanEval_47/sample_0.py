"""
AI Generated Solution
Task ID: HumanEval/47
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.181359
"""

def median(my_list):
    sorted_list = sorted(my_list)
    length = len(sorted_list)
    if length % 2 == 0:
        middle = length // 2
        return (sorted_list[middle - 1] + sorted_list[middle]) / 2
    else:
        middle = length // 2
        return sorted_list[middle]