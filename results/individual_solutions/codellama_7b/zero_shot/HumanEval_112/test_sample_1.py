"""
Test for AI Generated Solution
Task ID: HumanEval/112
Model: codellama:7b
"""

def reverse_delete(s, c):
    # Remove all characters in s that are present in c
    for i in range(len(s) - 1, -1, -1):
        if s[i] in c:
            s = s[:i] + s[i+1:]

    # Check if the result string is a palindrome
    return (s, s == s[::-1])

def check(candidate):

    assert candidate("abcde","ae") == ('bcd',False)
    assert candidate("abcdef", "b") == ('acdef',False)
    assert candidate("abcdedcba","ab") == ('cdedc',True)
    assert candidate("dwik","w") == ('dik',False)
    assert candidate("a","a") == ('',True)
    assert candidate("abcdedcba","") == ('abcdedcba',True)
    assert candidate("abcdedcba","v") == ('abcdedcba',True)
    assert candidate("vabba","v") == ('abba',True)
    assert candidate("mamma", "mia") == ("", True)
