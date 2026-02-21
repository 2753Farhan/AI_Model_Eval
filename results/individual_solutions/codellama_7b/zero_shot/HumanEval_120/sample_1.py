"""
AI Generated Solution
Task ID: HumanEval/120
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.290569
"""

def maximum(arr, k):
    # Sort the array in descending order
    arr.sort(reverse=True)

    # Return the top k elements of the sorted array
    return arr[:k]