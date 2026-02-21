"""
AI Generated Solution
Task ID: HumanEval/78
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.233016
"""

def hex_key(num):
    count = 0
    for char in num:
        if ord(char) > 47 and ord(char) < 58 or ord(char) > 64 and ord(char) < 71:
            count += 1
    return count