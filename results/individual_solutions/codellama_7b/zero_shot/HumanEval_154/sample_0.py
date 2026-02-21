"""
AI Generated Solution
Task ID: HumanEval/154
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.339671
"""

def cycpattern_check(word1, word2):
    # Check if word2 is a substring of word1
    if word2 in word1:
        return True

    # Check if any rotations of word2 are substrings of word1
    for i in range(len(word2)):
        rotation = word2[i:] + word2[:i]
        if rotation in word1:
            return True

    return False