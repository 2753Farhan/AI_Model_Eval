"""
AI Generated Solution
Task ID: HumanEval/119
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.290569
"""

def match_parens(lst):
    stack = []
    for char in lst:
        if char == "(":
            stack.append(char)
        else:
            if not stack:
                return "No"
            stack.pop()

    return "Yes" if not stack else "No"