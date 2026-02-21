"""
AI Generated Solution
Task ID: HumanEval/108
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.276059
"""

def count_nums(arr):
    count = 0
    for num in arr:
        if num > 0 or (num < 0 and num % 10 > 0):
            count += 1
    return count