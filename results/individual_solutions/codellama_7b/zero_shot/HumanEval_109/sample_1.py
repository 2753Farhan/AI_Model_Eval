"""
AI Generated Solution
Task ID: HumanEval/109
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.277059
"""


def move_one_ball(arr):
    # Check if the input array is empty
    if not arr:
        return True

    # Sort the array in non-decreasing order
    arr.sort()

    # Check if the array is already sorted
    if arr == list(range(min(arr), max(arr) + 1)):
        return True

    # Initialize a variable to keep track of the number of right shift operations
    count = 0

    # Loop through the array and check for duplicates
    for i in range(len(arr) - 1):
        if arr[i] == arr[i + 1]:
            count += 1

    # If there are no duplicates, return True
    if count == 0:
        return True

    # Otherwise, return False
    return False