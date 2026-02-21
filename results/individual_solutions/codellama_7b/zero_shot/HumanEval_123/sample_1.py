"""
AI Generated Solution
Task ID: HumanEval/123
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.295081
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