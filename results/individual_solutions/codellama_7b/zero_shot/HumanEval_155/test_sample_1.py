"""
Test for AI Generated Solution
Task ID: HumanEval/155
Model: codellama:7b
"""

def even_odd_count(n):
    count = 0
    for digit in str(abs(n)):
        if int(digit) % 2 == 0:
            count += 1
        else:
            count += 1
    return (count, len(str(abs(n))) - count)

def check(candidate):

    # Check some simple cases
    assert candidate(7) == (0, 1)
    assert candidate(-78) == (1, 1)
    assert candidate(3452) == (2, 2)
    assert candidate(346211) == (3, 3)
    assert candidate(-345821) == (3, 3)
    assert candidate(-2) == (1, 0)
    assert candidate(-45347) == (2, 3)
    assert candidate(0) == (1, 0)


    # Check some edge cases that are easy to work out by hand.
    assert True

