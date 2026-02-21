"""
AI Generated Solution
Task ID: HumanEval/12
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.110889
"""

def longest(strings):
    if not strings:
        return None
    return max(strings, key=len)


# Test cases:
print(longest([]) == None)  # True
print(longest(['a', 'b', 'c']) == 'a')  # True
print(longest(['a', 'bb', 'ccc']) == 'ccc')  # True