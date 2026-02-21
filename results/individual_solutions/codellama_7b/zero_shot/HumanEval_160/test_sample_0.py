"""
Test for AI Generated Solution
Task ID: HumanEval/160
Model: codellama:7b
"""

def do_algebra(operator, operand):
    # Validate input
    if len(operator) != len(operand) - 1:
        raise ValueError("Invalid input")
    for op in operator:
        if op not in ["+", "-", "*", "//", "**"]:
            raise ValueError("Invalid operator")
    for num in operand:
        if num < 0:
            raise ValueError("Invalid operand")

    # Evaluate expression
    result = operand[0]
    for i in range(len(operator)):
        if operator[i] == "+":
            result += operand[i+1]
        elif operator[i] == "-":
            result -= operand[i+1]
        elif operator[i] == "*":
            result *= operand[i+1]
        elif operator[i] == "//":
            result //= operand[i+1]
        elif operator[i] == "**":
            result **= operand[i+1]
    return result

def check(candidate):

    # Check some simple cases
    assert candidate(['**', '*', '+'], [2, 3, 4, 5]) == 37
    assert candidate(['+', '*', '-'], [2, 3, 4, 5]) == 9
    assert candidate(['//', '*'], [7, 3, 4]) == 8, "This prints if this assert fails 1 (good for debugging!)"

    # Check some edge cases that are easy to work out by hand.
    assert True, "This prints if this assert fails 2 (also good for debugging!)"

