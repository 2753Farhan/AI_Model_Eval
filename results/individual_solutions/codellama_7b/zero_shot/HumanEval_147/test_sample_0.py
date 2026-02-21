"""
Test for AI Generated Solution
Task ID: HumanEval/147
Model: codellama:7b
"""

def get_max_triples(n):
    count = 0
    for i in range(1, n):
        for j in range(i + 1, n):
            if (i * i - i + 1) + (j * j - j + 1) in range(3 * k + 1) for k in range(1, n)):
                count += 1
    return count

def check(candidate):

    assert candidate(5) == 1
    assert candidate(6) == 4
    assert candidate(10) == 36
    assert candidate(100) == 53361
