"""
AI Generated Solution
Task ID: HumanEval/103
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.268548
"""

def rounded_avg(n, m):
    if n > m:
        return -1
    total = 0
    for i in range(n, m+1):
        total += i
    average = total / (m-n+1)
    return "0b" + bin(round(average)).lstrip("0b")