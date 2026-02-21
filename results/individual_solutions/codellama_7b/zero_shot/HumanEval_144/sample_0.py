"""
AI Generated Solution
Task ID: HumanEval/144
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.325158
"""

def simplify(x, n):
    # convert the strings to fractions
    x_frac = Fraction.from_string(x)
    n_frac = Fraction.from_string(n)

    # multiply the fractions and check if the result is an integer
    result = x_frac * n_frac
    return result.numerator == result.denominator

# test the function with some examples
print(simplify("1/5", "5/1"))  # should be True
print(simplify("1/6", "2/1"))   # should be False
print(simplify("7/10", "10/2")) # should be False

# note: you may need to import the Fraction class from the math module for this solution to work