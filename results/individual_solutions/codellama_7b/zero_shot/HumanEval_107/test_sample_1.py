"""
Test for AI Generated Solution
Task ID: HumanEval/107
Model: codellama:7b
"""

def even_odd_palindrome(n):
    # Initialize variables to store the count of even and odd palindromes
    count_even = 0
    count_odd = 0

    # Loop through all numbers from 1 to n
    for num in range(1, n+1):
        # Check if the number is a palindrome
        if str(num) == str(num)[::-1]:
            # Increment the count of even palindromes if the number is even
            if num % 2 == 0:
                count_even += 1
            # Increment the count of odd palindromes if the number is odd
            else:
                count_odd += 1

    # Return the count of even and odd palindromes
    return (count_even, count_odd)

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

