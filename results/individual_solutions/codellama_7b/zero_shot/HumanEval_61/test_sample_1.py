"""
Test for AI Generated Solution
Task ID: HumanEval/61
Model: codellama:7b
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



METADATA = {}


def check(candidate):
    assert candidate("()")
    assert candidate("(()())")
    assert candidate("()()(()())()")
    assert candidate("()()((()()())())(()()(()))")
    assert not candidate("((()())))")
    assert not candidate(")(()")
    assert not candidate("(")
    assert not candidate("((((")
    assert not candidate(")")
    assert not candidate("(()")
    assert not candidate("()()(()())())(()")
    assert not candidate("()()(()())()))()")

