"""
AI Generated Solution
Task ID: HumanEval/57
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.201467
"""

def monotonic(my_list):
    if len(my_list) <= 1:
        return True
    elif my_list[0] < my_list[-1]:
        for i in range(len(my_list) - 1):
            if my_list[i] > my_list[i + 1]:
                return False
    else:
        for i in range(len(my_list) - 1):
            if my_list[i] < my_list[i + 1]:
                return False
    return True