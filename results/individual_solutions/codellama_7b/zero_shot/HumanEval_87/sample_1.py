"""
AI Generated Solution
Task ID: HumanEval/87
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.247526
"""

def get_row(lst, x):
    result = []
    for i, row in enumerate(lst):
        for j, col in enumerate(row):
            if col == x:
                result.append((i, j))
    return sorted(result, key=lambda k: (k[0], -k[1]))