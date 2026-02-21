"""
AI Generated Solution
Task ID: HumanEval/77
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.231017
"""

def iscube(a):
    for i in range(1, a+1):
        if pow(i, 3) == abs(a):
            return True
    return False