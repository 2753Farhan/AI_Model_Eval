"""
Test for AI Generated Solution
Task ID: HumanEval/131
Model: codellama:7b
"""

def digits(n):
    product = 1
    while n > 0:
        digit = n % 10
        if digit % 2 == 1:
            product *= digit
        n //= 10
    return product

assert digits(1) == 1
assert digits(4) == 0
assert digits(235) == 15

def check(candidate):

    # Check some simple cases
    assert candidate(5) == 5
    assert candidate(54) == 5
    assert candidate(120) ==1
    assert candidate(5014) == 5
    assert candidate(98765) == 315
    assert candidate(5576543) == 2625

    # Check some edge cases that are easy to work out by hand.
    assert candidate(2468) == 0

