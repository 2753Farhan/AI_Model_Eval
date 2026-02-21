"""
Test for AI Generated Solution
Task ID: HumanEval/122
Model: codellama:7b
"""

def add_elements(arr, k):
    # Initialize a variable to store the sum
    sum = 0

    # Iterate over the first k elements of the array
    for i in range(k):
        # If the element is less than or equal to 10, include it in the sum
        if arr[i] <= 10:
            sum += arr[i]

    # Return the sum
    return sum

def check(candidate):

    # Check some simple cases
    assert candidate([1,-2,-3,41,57,76,87,88,99], 3) == -4
    assert candidate([111,121,3,4000,5,6], 2) == 0
    assert candidate([11,21,3,90,5,6,7,8,9], 4) == 125
    assert candidate([111,21,3,4000,5,6,7,8,9], 4) == 24, "This prints if this assert fails 1 (good for debugging!)"

    # Check some edge cases that are easy to work out by hand.
    assert candidate([1], 1) == 1, "This prints if this assert fails 2 (also good for debugging!)"

