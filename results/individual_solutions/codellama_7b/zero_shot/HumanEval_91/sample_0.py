"""
AI Generated Solution
Task ID: HumanEval/91
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.253041
"""

def is_bored(S):
    count = 0
    for s in S.split('.'):
        if s.startswith('I'):
            count += 1
    return count