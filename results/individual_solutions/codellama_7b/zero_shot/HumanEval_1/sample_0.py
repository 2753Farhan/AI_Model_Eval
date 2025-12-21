"""
AI Generated Solution
Task ID: HumanEval/1
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2025-12-21T18:43:57.648793
"""

def separate_paren_groups(paren_string):
    stack = []
    result = []
    for char in paren_string:
        if char == "(":
            stack.append(char)
        elif char == ")":
            top = stack.pop()
            while top != "(":
                result.append(top)
                top = stack.pop()
    return ["".join(result)] + [")" + x for x in result[::-1]]