"""
Test for AI Generated Solution
Task ID: HumanEval/109
Model: codellama:7b
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


def check(candidate):

    # Check some simple cases
    assert candidate([3, 4, 5, 1, 2])==True, "This prints if this assert fails 1 (good for debugging!)"
    assert candidate([3, 5, 10, 1, 2])==True
    assert candidate([4, 3, 1, 2])==False
    # Check some edge cases that are easy to work out by hand.
    assert candidate([3, 5, 4, 1, 2])==False, "This prints if this assert fails 2 (also good for debugging!)"
    assert candidate([])==True
