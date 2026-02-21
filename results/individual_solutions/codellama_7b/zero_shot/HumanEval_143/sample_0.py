"""
AI Generated Solution
Task ID: HumanEval/143
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.324158
"""

def words_in_sentence(sentence):
    # Split the sentence into a list of words
    words = sentence.split()

    # Create an empty string to store the prime words
    prime_words = ""

    # Loop through each word in the list
    for word in words:
        # Check if the length of the word is a prime number
        if is_prime(len(word)):
            # If it is, add it to the prime_words string
            prime_words += word + " "

    return prime_words.strip()


def is_prime(n):
    # Check if n is greater than 1
    if n > 1:
        # Loop through all numbers between 2 and the square root of n
        for i in range(2, int(n ** 0.5) + 1):
            # If n is divisible by i, it is not prime
            if n % i == 0:
                return False
        # If we make it to the end of the loop, n is prime
        return True
    # If n is less than or equal to 1, it is not prime
    return False