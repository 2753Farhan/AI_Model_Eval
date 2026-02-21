"""
AI Generated Solution
Task ID: HumanEval/114
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.282569
"""

def minSubArraySum(nums):
    """
    Given an array of integers nums, find the minimum sum of any non-empty sub-array
    of nums.
    Example
    minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
    minSubArraySum([-1, -2, -3]) == -6
    """
    # Initialize the minimum sum to infinity
    min_sum = float('inf')
    # Initialize the sum to 0
    current_sum = 0
    # Loop through the array
    for i in range(len(nums)):
        # Add the current element to the sum
        current_sum += nums[i]
        # If the sum is less than the minimum sum, update it
        if current_sum < min_sum:
            min_sum = current_sum
        # If the sum is greater than 0 (i.e., it's negative), set it to 0
        elif current_sum > 0:
            current_sum = 0
    # Return the minimum sum
    return min_sum