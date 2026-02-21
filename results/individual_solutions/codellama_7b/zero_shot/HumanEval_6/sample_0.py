"""
AI Generated Solution
Task ID: HumanEval/6
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.092220
"""


def parse_nested_parens(paren_string):
    # Initialize a list to store the results
    levels = []

    # Iterate through each group of parentheses in the string
    for group in paren_string.split():
        # Keep track of the current level of nesting
        level = 0

        # Iterate through each character in the group
        for char in group:
            # If the character is an opening parenthesis, increase the level of nesting
            if char == '(':
                level += 1
            # If the character is a closing parenthesis, decrease the level of nesting
            elif char == ')':
                level -= 1

        # Add the maximum level of nesting to the list of levels
        levels.append(max(level, 0))

    return levels