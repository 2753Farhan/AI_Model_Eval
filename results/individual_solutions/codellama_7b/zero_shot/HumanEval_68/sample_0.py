"""
AI Generated Solution
Task ID: HumanEval/68
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.218487
"""

def pluck(nodes):
    smallest_even_value = float('inf')
    smallest_index = -1
    for i, node in enumerate(nodes):
        if node % 2 == 0 and node < smallest_even_value:
            smallest_even_value = node
            smallest_index = i
    return [smallest_even_value, smallest_index] if smallest_index != -1 else []