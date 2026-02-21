"""
AI Generated Solution
Task ID: HumanEval/43
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.174847
"""

def pairs_sum_to_zero(my_list):
    for i in range(len(my_list)):
        for j in range(i+1, len(my_list)):
            if my_list[i] + my_list[j] == 0:
                return True
    return False