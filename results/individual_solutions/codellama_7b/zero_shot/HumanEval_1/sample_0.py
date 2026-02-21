"""
AI Generated Solution
Task ID: HumanEval/1
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.080711
"""

def separate_paren_groups(paren_string):
    stack = []
    result = []
    for char in paren_string:
        if char == "(":
            stack.append(char)
        elif char == ")":
            top = stack.pop()
            if top == "(":
                result.append("".join(stack[::-1]))
                stack = []
    return result