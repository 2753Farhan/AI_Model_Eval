"""
Test for AI Generated Solution
Task ID: HumanEval/6
Model: codellama:7b
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



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('(()()) ((())) () ((())()())') == [2, 3, 1, 3]
    assert candidate('() (()) ((())) (((())))') == [1, 2, 3, 4]
    assert candidate('(()(())((())))') == [4]
