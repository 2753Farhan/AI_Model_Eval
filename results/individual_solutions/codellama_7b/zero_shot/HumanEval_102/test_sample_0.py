"""
Test for AI Generated Solution
Task ID: HumanEval/102
Model: codellama:7b
"""

def choose_num(x, y):
    for i in range(x, y+1):
        if i % 2 == 0:
            return i
    return -1

def check(candidate):

    # Check some simple cases
    assert candidate(12, 15) == 14
    assert candidate(13, 12) == -1
    assert candidate(33, 12354) == 12354
    assert candidate(5234, 5233) == -1
    assert candidate(6, 29) == 28
    assert candidate(27, 10) == -1

    # Check some edge cases that are easy to work out by hand.
    assert candidate(7, 7) == -1
    assert candidate(546, 546) == 546

