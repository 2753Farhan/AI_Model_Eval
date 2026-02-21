"""
Test for AI Generated Solution
Task ID: HumanEval/144
Model: codellama:7b
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

def check(candidate):

    # Check some simple cases
    assert candidate("1/5", "5/1") == True, 'test1'
    assert candidate("1/6", "2/1") == False, 'test2'
    assert candidate("5/1", "3/1") == True, 'test3'
    assert candidate("7/10", "10/2") == False, 'test4'
    assert candidate("2/10", "50/10") == True, 'test5'
    assert candidate("7/2", "4/2") == True, 'test6'
    assert candidate("11/6", "6/1") == True, 'test7'
    assert candidate("2/3", "5/2") == False, 'test8'
    assert candidate("5/2", "3/5") == False, 'test9'
    assert candidate("2/4", "8/4") == True, 'test10'


    # Check some edge cases that are easy to work out by hand.
    assert candidate("2/4", "4/2") == True, 'test11'
    assert candidate("1/5", "5/1") == True, 'test12'
    assert candidate("1/5", "1/5") == False, 'test13'

