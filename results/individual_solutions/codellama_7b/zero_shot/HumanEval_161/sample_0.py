"""
AI Generated Solution
Task ID: HumanEval/161
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.349177
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