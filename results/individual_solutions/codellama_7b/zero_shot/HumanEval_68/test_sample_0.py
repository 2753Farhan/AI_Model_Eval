"""
Test for AI Generated Solution
Task ID: HumanEval/68
Model: codellama:7b
"""

def pluck(nodes):
    smallest_even_value = float('inf')
    smallest_index = -1
    for i, node in enumerate(nodes):
        if node % 2 == 0 and node < smallest_even_value:
            smallest_even_value = node
            smallest_index = i
    return [smallest_even_value, smallest_index] if smallest_index != -1 else []

def check(candidate):

    # Check some simple cases
    assert True, "This prints if this assert fails 1 (good for debugging!)"
    assert candidate([4,2,3]) == [2, 1], "Error"
    assert candidate([1,2,3]) == [2, 1], "Error"
    assert candidate([]) == [], "Error"
    assert candidate([5, 0, 3, 0, 4, 2]) == [0, 1], "Error"

    # Check some edge cases that are easy to work out by hand.
    assert True, "This prints if this assert fails 2 (also good for debugging!)"
    assert candidate([1, 2, 3, 0, 5, 3]) == [0, 3], "Error"
    assert candidate([5, 4, 8, 4 ,8]) == [4, 1], "Error"
    assert candidate([7, 6, 7, 1]) == [6, 1], "Error"
    assert candidate([7, 9, 7, 1]) == [], "Error"

