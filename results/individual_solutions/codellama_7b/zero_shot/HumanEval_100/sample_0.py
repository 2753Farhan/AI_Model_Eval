"""
AI Generated Solution
Task ID: HumanEval/100
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.265566
"""

def make_a_pile(n):
    levels = []
    current_level = n
    while current_level > 0:
        levels.append(current_level)
        if current_level % 2 == 0:
            current_level = int(current_level / 2)
        else:
            current_level = int((current_level + 1) / 2)
    return levels