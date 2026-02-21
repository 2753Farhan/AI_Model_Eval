"""
AI Generated Solution
Task ID: HumanEval/149
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.332159
"""

def sorted_list_sum(lst):
    # Filter out words with odd lengths and sort by length and alphabetical order
    return sorted(filter(lambda x: len(x) % 2 == 0, lst), key=lambda x: (len(x), x))