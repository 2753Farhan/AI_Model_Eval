"""
AI Generated Solution
Task ID: HumanEval/11
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.108882
"""

def string_xor(a, b):
    result = []
    for i, j in zip(a, b):
        if i == j:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)