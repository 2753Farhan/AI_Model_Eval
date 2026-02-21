"""
Test for AI Generated Solution
Task ID: HumanEval/112
Model: codellama:7b
"""

def reverse_delete(s, c):
    # Build a set of characters to remove from the string
    chars_to_remove = set(c)

    # Create a new string with all the characters not in chars_to_remove
    new_string = ''.join(ch for ch in s if ch not in chars_to_remove)

    # Check if the new string is a palindrome
    return (new_string, new_string == new_string[::-1])

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
