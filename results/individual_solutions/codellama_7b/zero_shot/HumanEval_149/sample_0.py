"""
AI Generated Solution
Task ID: HumanEval/149
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.332159
"""

def sorted_list_sum(lst):
    result = []
    for word in lst:
        if len(word) % 2 == 0:
            result.append(word)
    return sorted(result)