"""
AI Generated Solution
Task ID: HumanEval/117
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.287569
"""

def select_words(s, n):
    words = []
    for word in s.split():
        if len([c for c in word if c.isalpha() and not c.lower() in 'aeiou']) == n:
            words.append(word)
    return words


# Test case 1:
assert select_words("Mary had a little lamb", 4) == ["little"]
# Test case 2:
assert select_words("Mary had a little lamb", 3) == ["Mary", "lamb"]
# Test case 3:
assert select_words("simple white space", 2) == []
# Test case 4:
assert select_words("Hello world", 4) == ["world"]
# Test case 5:
assert select_words("Uncle sam", 3) == ["Uncle"]