"""
Test for AI Generated Solution
Task ID: HumanEval/49
Model: codellama:7b
"""

def modp(n, p):
    return pow(2, n, p)



METADATA = {}


def check(candidate):
    assert candidate(3, 5) == 3
    assert candidate(1101, 101) == 2
    assert candidate(0, 101) == 1
    assert candidate(3, 11) == 8
    assert candidate(100, 101) == 1
    assert candidate(30, 5) == 4
    assert candidate(31, 5) == 3

