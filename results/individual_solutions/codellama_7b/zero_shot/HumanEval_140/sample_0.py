"""
AI Generated Solution
Task ID: HumanEval/140
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.319640
"""

def fix_spaces(text):
    text = text.replace('  ', '-')
    text = text.replace(' ', '_')
    return text