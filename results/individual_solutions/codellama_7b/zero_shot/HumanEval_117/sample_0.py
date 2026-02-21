"""
AI Generated Solution
Task ID: HumanEval/117
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.286587
"""

def select_words(s, n):
    words = []
    for word in s.split():
        if len([c for c in word if c.isalpha() and not c.islower()]) == n:
            words.append(word)
    return words