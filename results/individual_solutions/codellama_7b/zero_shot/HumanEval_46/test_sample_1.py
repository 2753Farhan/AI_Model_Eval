"""
Test for AI Generated Solution
Task ID: HumanEval/46
Model: codellama:7b
"""

def fib4(n: int):
    if n <= 3:
        return 0
    else:
        a, b, c = 0, 2, 0
        for i in range(n-3):
            a, b, c = b, c, a+b+c
        return a+b+c



METADATA = {}


def check(candidate):
    assert candidate(5) == 4
    assert candidate(8) == 28
    assert candidate(10) == 104
    assert candidate(12) == 386

