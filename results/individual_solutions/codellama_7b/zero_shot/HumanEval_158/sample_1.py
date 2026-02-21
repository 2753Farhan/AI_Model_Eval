"""
AI Generated Solution
Task ID: HumanEval/158
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.345179
"""

def find_max(words):
    unique_chars = {}
    max_unique_chars = 0
    max_word = ""
    for word in words:
        current_unique_chars = len(set(word))
        if current_unique_chars > max_unique_chars:
            max_unique_chars = current_unique_chars
            max_word = word
    return max_word
