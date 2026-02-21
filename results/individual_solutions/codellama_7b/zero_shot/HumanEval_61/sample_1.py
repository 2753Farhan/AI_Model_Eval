"""
AI Generated Solution
Task ID: HumanEval/61
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.208984
"""

def correct_bracketing(brackets):
    stack = []
    for char in brackets:
        if char == "(":
            stack.append(char)
        elif char == ")":
            if not stack or stack.pop() != ")":
                return False
    return not stack