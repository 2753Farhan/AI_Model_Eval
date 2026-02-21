"""
AI Generated Solution
Task ID: HumanEval/145
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.327158
"""

def order_by_points(nums):
    """
    Sorts the given list of integers in ascending order according to the sum of their digits.
    If there are several items with similar sum of their digits, order them based on their index in original list.
    """
    return sorted(nums, key=lambda x: (x, len(str(x))-1))