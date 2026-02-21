"""
AI Generated Solution
Task ID: HumanEval/107
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.274059
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