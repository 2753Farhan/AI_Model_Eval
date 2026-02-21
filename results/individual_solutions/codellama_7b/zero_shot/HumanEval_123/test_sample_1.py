"""
Test for AI Generated Solution
Task ID: HumanEval/123
Model: codellama:7b
"""

def get_odd_collatz(n):
    if n <= 0:
        return []
    else:
        seq = [n]
        while seq[-1] != 1:
            if seq[-1] % 2 == 0:
                seq.append(seq[-1] // 2)
            else:
                seq.append(3 * seq[-1] + 1)
        return [x for x in seq if x % 2 != 0]

def check(candidate):

    # Check some simple cases
    assert candidate(14) == [1, 5, 7, 11, 13, 17]
    assert candidate(5) == [1, 5]
    assert candidate(12) == [1, 3, 5], "This prints if this assert fails 1 (good for debugging!)"

    # Check some edge cases that are easy to work out by hand.
    assert candidate(1) == [1], "This prints if this assert fails 2 (also good for debugging!)"

