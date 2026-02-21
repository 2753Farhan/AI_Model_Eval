"""
AI Generated Solution
Task ID: HumanEval/47
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.182359
"""

def median(my_list):
    sorted_list = sorted(my_list)
    length = len(sorted_list)
    if length % 2 == 0:
        # even number of elements
        median1 = sorted_list[length // 2]
        median2 = sorted_list[length // 2 - 1]
        return (median1 + median2) / 2
    else:
        # odd number of elements
        return sorted_list[length // 2]