"""
AI Generated Solution
Task ID: HumanEval/9
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.102365
"""

def rolling_max(numbers):
    max_val = []
    for i in range(len(numbers)):
        curr_max = max(numbers[:i+1])
        max_val.append(curr_max)
    return max_val