"""
AI Generated Solution
Task ID: HumanEval/64
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.212985
"""

def vowels_count(s):
    count = 0
    for c in s:
        if c.lower() in 'aeiouy':
            count += 1
    return count