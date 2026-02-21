"""
AI Generated Solution
Task ID: HumanEval/57
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.200476
"""

def is_monotonic(my_list):
    if len(my_list) <= 1:
        return True
    else:
        for i in range(len(my_list)-1):
            if my_list[i+1] < my_list[i]:
                return False
        return True