"""
Test for AI Generated Solution
Task ID: HumanEval/65
Model: codellama:7b
"""


def circular_shift(x, shift):
    # Get the number of digits in x
    num_digits = len(str(x))

    # Check if the shift is greater than the number of digits
    if shift > num_digits:
        # If so, return the reversed digits
        return "".join(reversed(str(x)))
    else:
        # If not, circularly shift the digits by the specified amount
        return "".join([str(x)[shift:] + str(x)[:shift]])


def check(candidate):

    # Check some simple cases
    assert candidate(100, 2) == "001"
    assert candidate(12, 2) == "12"
    assert candidate(97, 8) == "79"
    assert candidate(12, 1) == "21", "This prints if this assert fails 1 (good for debugging!)"

    # Check some edge cases that are easy to work out by hand.
    assert candidate(11, 101) == "11", "This prints if this assert fails 2 (also good for debugging!)"

