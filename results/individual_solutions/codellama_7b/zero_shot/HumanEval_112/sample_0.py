"""
AI Generated Solution
Task ID: HumanEval/112
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.280058
"""

def reverse_delete(s, c):
    # Build a set of characters to remove from the string
    chars_to_remove = set(c)

    # Create a new string with all the characters not in chars_to_remove
    new_string = ''.join(ch for ch in s if ch not in chars_to_remove)

    # Check if the new string is a palindrome
    return (new_string, new_string == new_string[::-1])