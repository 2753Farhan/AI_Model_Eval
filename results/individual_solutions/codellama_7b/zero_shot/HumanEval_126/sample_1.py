"""
AI Generated Solution
Task ID: HumanEval/126
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.299619
"""

def is_sorted(my_list):
    if len(my_list) == 0:
        return True
    else:
        for i in range(len(my_list) - 1):
            if my_list[i] > my_list[i + 1]:
                return False
        return True