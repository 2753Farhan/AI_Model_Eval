"""
AI Generated Solution
Task ID: HumanEval/36
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.164329
"""

def fizz_buzz(n):
    count = 0
    for i in range(1, n+1):
        if i % 11 == 0 or i % 13 == 0:
            if '7' in str(i):
                count += 1
    return count