"""
AI Generated Solution
Task ID: HumanEval/107
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.274059
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