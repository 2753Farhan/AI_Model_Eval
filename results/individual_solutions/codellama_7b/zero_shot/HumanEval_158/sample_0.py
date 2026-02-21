"""
AI Generated Solution
Task ID: HumanEval/158
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.344173
"""

def find_max(words):
    max_length = -1
    result = ""
    for word in words:
        if len(set(word)) > max_length:
            max_length = len(set(word))
            result = word
    return result

# Test case 1:
assert find_max(["name", "of", "string"]) == "string"
# Test case 2:
assert find_max(["name", "enam", "game"]) == "enam"
# Test case 3:
assert find_max(["aaaaaaa", "bb", "cc"]) == "aaaaaaa"