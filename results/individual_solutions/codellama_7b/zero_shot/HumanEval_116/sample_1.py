"""
AI Generated Solution
Task ID: HumanEval/116
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.285568
"""

def sort_array(arr):
    return sorted(arr, key=lambda x: (bin(x).count('1'), x))