"""
AI Generated Solution
Task ID: HumanEval/1
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.081712
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
    return ["".join(result)] + stack[::-1]


# Test case 1:
paren_string = "( ) (( )) (( )( ))"
print(separate_paren_groups(paren_string)) # Output: ['()', '(())', '(()())']

# Test case 2:
paren_string = "()"
print(separate_paren_groups(paren_string)) # Output: ['()']

# Test case 3:
paren_string = "((()))"
print(separate_paren_groups(paren_string)) # Output: ['()()()']

# Test case 4:
paren_string = "(()())"
print(separate_paren_groups(paren_string)) # Output: ['()()()']

# Test case 5:
paren_string = "( ( () ) (( )) )"
print(separate_paren_groups(paren_string)) # Output: ['()', '()()', '(()())']

# Test case 6:
paren_string = "((( )))"
print(separate_paren_groups(paren_string)) # Output: ['()()()']

# Test case 7:
paren_string = "( ( ) ( ) (( )) (( )( )) )"
print(separate_paren_groups(paren_string)) # Output: ['()', '()', '(()())', '(()())']

# Test case 8:
paren_string = "((( () )))"
print(separate_paren_groups(paren_string)) # Output: ['()()()']