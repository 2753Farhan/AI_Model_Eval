"""
AI Generated Solution
Task ID: HumanEval/33
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.158329
"""

def sort_third(my_list):
    sorted_list = []
    for i in range(len(my_list)):
        if i % 3 == 0:
            sorted_list.append(my_list[i])
    sorted_list.sort()
    return sorted_list