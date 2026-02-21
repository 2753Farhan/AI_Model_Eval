"""
AI Generated Solution
Task ID: HumanEval/152
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.337669
"""

def compare(scores, guesses):
    return [abs(score - guess) for score, guess in zip(scores, guesses)]