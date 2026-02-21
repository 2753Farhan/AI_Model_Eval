"""
AI Generated Solution
Task ID: HumanEval/123
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.294080
"""

def get_odd_collatz(n):
    if n <= 0:
        return []

    sequence = [n]
    while sequence[-1] != 1:
        if sequence[-1] % 2 == 0:
            sequence.append(sequence[-1] // 2)
        else:
            sequence.append(3 * sequence[-1] + 1)

    return [x for x in sequence if x % 2 != 0]