"""
AI Generated Solution
Task ID: HumanEval/161
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.350190
"""


def solve(s):
    result = ""
    
    # Check if the string contains any letters
    if any(char.isalpha() for char in s):
        # If it does, reverse the case of each letter
        for char in s:
            if char.isalpha():
                result += char.upper() if char.islower() else char.lower()
            else:
                result += char
    else:
        # If it doesn't, just reverse the string
        result = s[::-1]
    
    return result