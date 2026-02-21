"""
AI Generated Solution
Task ID: HumanEval/135
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.313658
"""

def can_arrange(arr):
    for i in range(len(arr) - 1):
        if arr[i] >= arr[i+1]:
            return -1
    return len(arr) - 1