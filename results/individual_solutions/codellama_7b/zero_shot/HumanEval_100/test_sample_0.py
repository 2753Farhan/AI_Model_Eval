"""
Test for AI Generated Solution
Task ID: HumanEval/100
Model: codellama:7b
"""

def make_a_pile(n):
    levels = []
    current_level = n
    while current_level > 0:
        levels.append(current_level)
        if current_level % 2 == 0:
            current_level = int(current_level / 2)
        else:
            current_level = int((current_level + 1) / 2)
    return levels

def check(candidate):

    # Check some simple cases
    assert candidate(3) == [3, 5, 7], "Test 3"
    assert candidate(4) == [4,6,8,10], "Test 4"
    assert candidate(5) == [5, 7, 9, 11, 13]
    assert candidate(6) == [6, 8, 10, 12, 14, 16]
    assert candidate(8) == [8, 10, 12, 14, 16, 18, 20, 22]

    # Check some edge cases that are easy to work out by hand.
    assert True, "This prints if this assert fails 2 (also good for debugging!)"

