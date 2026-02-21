"""
AI Generated Solution
Task ID: HumanEval/52
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.190869
"""

def below_threshold(my_list, threshold):
    for num in my_list:
        if num > threshold:
            return False
    return True