"""
Test for AI Generated Solution
Task ID: HumanEval/107
Model: codellama:7b
"""

def even_odd_palindrome(n):
    # Initialize a list to store all the palindromes
    palindromes = []

    # Iterate from 1 to n
    for i in range(1, n+1):
        # Check if the number is a palindrome
        if str(i) == str(i)[::-1]:
            # If it is a palindrome, check if it is even or odd
            if i % 2 == 0:
                # If it is even, add it to the list of even palindromes
                palindromes.append(i)
            else:
                # If it is odd, add it to the list of odd palindromes
                palindromes.append(i)

    # Return the length of the lists of even and odd palindromes
    return len(palindromes[::2]), len(palindromes[1::2])

def check(candidate):

    # Check some simple cases
    assert candidate(123) == (8, 13)
    assert candidate(12) == (4, 6)
    assert candidate(3) == (1, 2)
    assert candidate(63) == (6, 8)
    assert candidate(25) == (5, 6)
    assert candidate(19) == (4, 6)
    assert candidate(9) == (4, 5), "This prints if this assert fails 1 (good for debugging!)"

    # Check some edge cases that are easy to work out by hand.
    assert candidate(1) == (0, 1), "This prints if this assert fails 2 (also good for debugging!)"

