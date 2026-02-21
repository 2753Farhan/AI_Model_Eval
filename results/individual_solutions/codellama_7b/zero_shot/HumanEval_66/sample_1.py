"""
AI Generated Solution
Task ID: HumanEval/66
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.215984
"""

def digitSum(s):
    sum = 0
    for c in s:
        if c.isupper():
            sum += ord(c)
    return sum