"""
AI Generated Solution
Task ID: HumanEval/65
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.214984
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
