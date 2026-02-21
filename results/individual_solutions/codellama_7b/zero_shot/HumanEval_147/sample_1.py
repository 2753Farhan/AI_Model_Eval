"""
AI Generated Solution
Task ID: HumanEval/147
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.330159
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