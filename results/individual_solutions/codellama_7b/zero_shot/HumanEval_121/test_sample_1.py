"""
Test for AI Generated Solution
Task ID: HumanEval/121
Model: codellama:7b
"""

def solution(my_list):
    # Check if the list is empty
    if not my_list:
        return 0

    # Initialize a variable to store the sum
    sum = 0

    # Iterate over the list and calculate the sum of the odd elements in even positions
    for i in range(len(my_list)):
        if i % 2 == 0 and my_list[i] % 2 != 0:
            sum += my_list[i]

    # Return the sum
    return sum

def check(candidate):

    # Check some simple cases
    assert candidate([5, 8, 7, 1])    == 12
    assert candidate([3, 3, 3, 3, 3]) == 9
    assert candidate([30, 13, 24, 321]) == 0
    assert candidate([5, 9]) == 5
    assert candidate([2, 4, 8]) == 0
    assert candidate([30, 13, 23, 32]) == 23
    assert candidate([3, 13, 2, 9]) == 3

    # Check some edge cases that are easy to work out by hand.

