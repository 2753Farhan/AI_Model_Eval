"""
Test for AI Generated Solution
Task ID: HumanEval/39
Model: codellama:7b
"""

def prime_fib(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a+b
        if is_prime(a) == False:
            return prime_fib(i+1)
    return a

def is_prime(n):
    if n == 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True



METADATA = {}


def check(candidate):
    assert candidate(1) == 2
    assert candidate(2) == 3
    assert candidate(3) == 5
    assert candidate(4) == 13
    assert candidate(5) == 89
    assert candidate(6) == 233
    assert candidate(7) == 1597
    assert candidate(8) == 28657
    assert candidate(9) == 514229
    assert candidate(10) == 433494437

