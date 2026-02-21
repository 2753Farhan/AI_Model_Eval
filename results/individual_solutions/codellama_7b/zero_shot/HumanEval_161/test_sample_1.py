"""
Test for AI Generated Solution
Task ID: HumanEval/161
Model: codellama:7b
"""


def solve(s):
    result = ""
    
    # Check if the string contains any letters
    if any(char.isalpha() for char in s):
        # If it does, reverse the case of each letter
        for char in s:
            if char.isalpha():
                result += char.upper() if char.islower() else char.lower()
            else:
                result += char
    else:
        # If it doesn't, just reverse the string
        result = s[::-1]
    
    return result

def check(candidate):

    # Check some simple cases
    assert candidate("AsDf") == "aSdF"
    assert candidate("1234") == "4321"
    assert candidate("ab") == "AB"
    assert candidate("#a@C") == "#A@c"
    assert candidate("#AsdfW^45") == "#aSDFw^45"
    assert candidate("#6@2") == "2@6#"

    # Check some edge cases that are easy to work out by hand.
    assert candidate("#$a^D") == "#$A^d"
    assert candidate("#ccc") == "#CCC"

    # Don't remove this line:
