"""
AI Generated Solution
Task ID: HumanEval/113
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.281563
"""

def odd_count(my_list):
    return [len([c for c in s if int(c) % 2 == 1]) for s in my_list]