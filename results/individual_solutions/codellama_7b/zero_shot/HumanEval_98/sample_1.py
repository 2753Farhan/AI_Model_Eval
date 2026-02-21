"""
AI Generated Solution
Task ID: HumanEval/98
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.263548
"""

def count_upper(s):
    count = 0
    for i in range(len(s)):
        if s[i].isupper() and i % 2 == 0:
            count += 1
    return count