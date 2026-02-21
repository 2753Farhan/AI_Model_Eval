"""
Test for AI Generated Solution
Task ID: HumanEval/45
Model: codellama:7b
"""

def triangle_area(a, h):
    return (a * h) / 2



METADATA = {}


def check(candidate):
    assert candidate(5, 3) == 7.5
    assert candidate(2, 2) == 2.0
    assert candidate(10, 8) == 40.0

