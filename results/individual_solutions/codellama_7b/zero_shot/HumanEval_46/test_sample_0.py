"""
Test for AI Generated Solution
Task ID: HumanEval/46
Model: codellama:7b
"""

def fib4(n):
    if n <= 3:
        return 0
    else:
        return fib4(n-1) + fib4(n-2) + fib4(n-3) + fib4(n-4)



METADATA = {}


def check(candidate):
    assert candidate(5) == 4
    assert candidate(8) == 28
    assert candidate(10) == 104
    assert candidate(12) == 386

