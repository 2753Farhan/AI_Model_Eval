"""
AI Generated Solution
Task ID: HumanEval/102
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.267548
"""

def choose_num(x, y):
    for i in range(x, y+1):
        if i % 2 == 0:
            return i
    return -1