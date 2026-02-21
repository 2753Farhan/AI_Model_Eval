"""
AI Generated Solution
Task ID: HumanEval/109
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.276059
"""

def move_one_ball(arr):
    # Check if the input array is empty
    if not arr:
        return True

    # Sort the array in non-decreasing order
    arr.sort()

    # Check if the array is sorted in non-decreasing order
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False

    return True


# Test cases
print(move_one_ball([3, 4, 5, 1, 2]))  # True
print(move_one_ball([3, 5, 4, 1, 2]))  # False
print(move_one_ball([1, 2, 3, 4, 5]))  # True
print(move_one_ball([5, 4, 3, 2, 1]))  # False
print(move_one_ball([1]))  # True
print(move_one_ball([]))  # True
