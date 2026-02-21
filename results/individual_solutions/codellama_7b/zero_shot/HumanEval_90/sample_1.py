"""
AI Generated Solution
Task ID: HumanEval/90
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.252042
"""

def next_smallest(lst):
    if len(lst) < 2:
        return None
    sorted_lst = sorted(lst)
    for i in range(len(lst)):
        if sorted_lst[i+1] != sorted_lst[i]:
            return sorted_lst[i+1]
    return None