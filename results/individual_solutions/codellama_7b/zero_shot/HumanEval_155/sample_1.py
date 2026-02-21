"""
AI Generated Solution
Task ID: HumanEval/155
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.341669
"""

def even_odd_count(n):
    count = 0
    for digit in str(abs(n)):
        if int(digit) % 2 == 0:
            count += 1
        else:
            count += 1
    return (count, len(str(abs(n))) - count)