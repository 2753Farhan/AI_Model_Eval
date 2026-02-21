"""
Test for AI Generated Solution
Task ID: HumanEval/72
Model: codellama:7b
"""

def will_it_fly(q,w):
    if len(q) == 0:
        return False
    if q[0] != q[-1]:
        return False
    total = 0
    for i in range(len(q)):
        total += q[i]
    return total <= w and total == sum(q)

#or using built-in sum function:
def will_it_fly(q,w):
    if len(q) == 0:
        return False
    if q[0] != q[-1]:
        return False
    return sum(q) <= w and sum(q) == sum(q)

#or using built-in sum function and palindrome check:
def will_it_fly(q,w):
    return len(q) > 0 and q == q[::-1] and sum(q) <= w

def check(candidate):

    # Check some simple cases
    assert candidate([3, 2, 3], 9) is True
    assert candidate([1, 2], 5) is False
    assert candidate([3], 5) is True
    assert candidate([3, 2, 3], 1) is False


    # Check some edge cases that are easy to work out by hand.
    assert candidate([1, 2, 3], 6) is False
    assert candidate([5], 5) is True

