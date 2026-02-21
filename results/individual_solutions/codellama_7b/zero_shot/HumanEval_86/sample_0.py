"""
AI Generated Solution
Task ID: HumanEval/86
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.245525
"""

def anti_shuffle(s):
    words = s.split()
    ordered_words = []
    for word in words:
        ordered_word = "".join(sorted(word))
        ordered_words.append(ordered_word)
    return " ".join(ordered_words)