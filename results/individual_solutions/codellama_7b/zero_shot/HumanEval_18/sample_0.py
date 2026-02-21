"""
AI Generated Solution
Task ID: HumanEval/18
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.123388
"""

def how_many_times(string, substring):
    count = 0
    for i in range(len(string)):
        if string[i:].startswith(substring):
            count += 1
    return count