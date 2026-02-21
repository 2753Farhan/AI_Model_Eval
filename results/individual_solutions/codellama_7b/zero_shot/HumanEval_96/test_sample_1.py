"""
Test for AI Generated Solution
Task ID: HumanEval/96
Model: codellama:7b
"""

def count_up_to(n):
    if n < 0:
        return []
    prime_numbers = []
    for i in range(2, n+1):
        if all(i % num != 0 for num in range(2, int(i ** 0.5) + 1)):
            prime_numbers.append(i)
    return prime_numbers

def check(candidate):

    assert candidate(5) == [2,3]
    assert candidate(6) == [2,3,5]
    assert candidate(7) == [2,3,5]
    assert candidate(10) == [2,3,5,7]
    assert candidate(0) == []
    assert candidate(22) == [2,3,5,7,11,13,17,19]
    assert candidate(1) == []
    assert candidate(18) == [2,3,5,7,11,13,17]
    assert candidate(47) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
    assert candidate(101) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

