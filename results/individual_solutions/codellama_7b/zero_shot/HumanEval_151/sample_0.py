"""
AI Generated Solution
Task ID: HumanEval/151
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.335690
"""

def double_the_difference(my_list):
    if not my_list:
        return 0
    difference = 0
    for num in my_list:
        if num % 2 != 0 and num > 0:
            difference += num ** 2
    return difference * 2