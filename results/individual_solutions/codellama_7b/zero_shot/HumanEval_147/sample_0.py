"""
AI Generated Solution
Task ID: HumanEval/147
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.329158
"""

def get_max_triples(n):
    count = 0
    for i in range(1, n):
        for j in range(i + 1, n):
            if (i * i - i + 1) + (j * j - j + 1) in range(3 * k + 1) for k in range(1, n)):
                count += 1
    return count