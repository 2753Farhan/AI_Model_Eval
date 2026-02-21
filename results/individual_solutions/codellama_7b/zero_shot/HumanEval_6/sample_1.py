"""
AI Generated Solution
Task ID: HumanEval/6
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.093727
"""

def parse_nested_parens(paren_string):
    stack = []
    result = []
    for char in paren_string:
        if char == "(":
            stack.append(char)
        elif char == ")":
            stack.pop()
        if not stack:
            result.append(len(stack))
    return result