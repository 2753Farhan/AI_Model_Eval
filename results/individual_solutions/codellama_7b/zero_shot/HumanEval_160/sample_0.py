"""
AI Generated Solution
Task ID: HumanEval/160
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.347179
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