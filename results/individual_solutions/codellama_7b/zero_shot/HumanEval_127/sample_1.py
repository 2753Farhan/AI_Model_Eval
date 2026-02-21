"""
AI Generated Solution
Task ID: HumanEval/127
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.300619
"""

def intersection(interval1, interval2):
    if not (interval1[0] <= interval2[1] and interval2[0] <= interval1[1]):
        return "NO"

    start = max(interval1[0], interval2[0])
    end = min(interval1[1], interval2[1])

    if start > end:
        return "NO"

    prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

    for prime in prime_numbers:
        if start < end and (end - start) == prime:
            return "YES"

    return "NO"