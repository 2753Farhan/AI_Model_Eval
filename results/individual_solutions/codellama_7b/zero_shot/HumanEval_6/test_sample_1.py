"""
Test for AI Generated Solution
Task ID: HumanEval/6
Model: codellama:7b
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



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('(()()) ((())) () ((())()())') == [2, 3, 1, 3]
    assert candidate('() (()) ((())) (((())))') == [1, 2, 3, 4]
    assert candidate('(()(())((())))') == [4]
