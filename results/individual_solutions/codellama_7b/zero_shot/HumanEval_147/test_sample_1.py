"""
Test for AI Generated Solution
Task ID: HumanEval/147
Model: codellama:7b
"""

def get_max_triples(n):
    a = []
    for i in range(1, n+1):
        a.append(i*i - i + 1)
    count = 0
    for i in range(1, n-1):
        for j in range(i+1, n):
            if a[i] + a[j] % 3 == 0:
                count += 1
    return count

def check(candidate):

    assert candidate(5) == 1
    assert candidate(6) == 4
    assert candidate(10) == 36
    assert candidate(100) == 53361
