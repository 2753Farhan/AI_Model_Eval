"""
AI Generated Solution
Task ID: HumanEval/40
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.169848
"""

def triples_sum_to_zero(my_list):
    for i in range(len(my_list)):
        for j in range(i+1, len(my_list)):
            for k in range(j+1, len(my_list)):
                if my_list[i] + my_list[j] + my_list[k] == 0:
                    return True
    return False