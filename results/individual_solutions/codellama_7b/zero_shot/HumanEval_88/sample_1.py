"""
AI Generated Solution
Task ID: HumanEval/88
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.248525
"""

def sort_array(array):
    # Sort the array in ascending order if the sum is odd, otherwise sort it in descending order
    sum_of_indices = sum(array)
    if sum_of_indices % 2 == 1:
        return sorted(array)
    else:
        return sorted(array, reverse=True)