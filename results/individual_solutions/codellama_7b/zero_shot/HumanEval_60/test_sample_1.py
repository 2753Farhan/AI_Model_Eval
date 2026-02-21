"""
Test for AI Generated Solution
Task ID: HumanEval/60
Model: codellama:7b
"""

def sum_to_n(n):
    return (n * (n + 1)) // 2



METADATA = {}


def check(candidate):
    assert candidate(1) == 1
    assert candidate(6) == 21
    assert candidate(11) == 66
    assert candidate(30) == 465
    assert candidate(100) == 5050

