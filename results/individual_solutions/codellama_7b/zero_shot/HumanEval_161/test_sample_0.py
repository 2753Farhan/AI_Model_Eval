"""
Test for AI Generated Solution
Task ID: HumanEval/161
Model: codellama:7b
"""

def solve(s):
    result = ""
    for i in range(len(s)):
        if s[i].isalpha():
            if s[i].islower():
                result += s[i].upper()
            else:
                result += s[i].lower()
        else:
            result += s[i]
    return result


def solve(s):
    return "".join([c.upper() if c.isalpha() and c.islower() else c for c in s])


def solve(s):
    result = ""
    for char in s:
        if char.isalpha():
            result += char.swapcase()
        else:
            result += char
    return result


def solve(s):
    return "".join(c.swapcase() if c.isalpha() else c for c in s)


def solve(s):
    result = ""
    for i, char in enumerate(s):
        if char.isalpha():
            result += char.swapcase()
        else:
            result += char
    return result


def solve(s):
    return "".join([c.swapcase() if c.isalpha() else c for c in s])


def solve(s):
    result = ""
    for i, char in enumerate(s):
        if char.isalpha():
            result += char.swapcase()
        else:
            result += char
    return result


def solve(s):
    return "".join([c.swapcase() if c.isalpha() else c for c in s])


def solve(s):
    result = ""
    for i, char in enumerate(s):
        if char.isalpha():
            result += char.swapcase()
        else:
            result += char
    return result


def solve(s):
    return "".join([c.swapcase() if c.isalpha() else c for c in s])


def solve(s):
    result = ""
    for i, char in enumerate(s):
        if char.isalpha():
            result += char.swapcase()
        else:
            result += char
    return result


def solve(s):
    return "".join([c.swapcase() if c.isalpha() else c for c in s])

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
