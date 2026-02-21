"""
Test for AI Generated Solution
Task ID: HumanEval/143
Model: codellama:7b
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

def check(candidate):

    # Check some simple cases
    assert candidate("This is a test") == "is"
    assert candidate("lets go for swimming") == "go for"
    assert candidate("there is no place available here") == "there is no place"
    assert candidate("Hi I am Hussein") == "Hi am Hussein"
    assert candidate("go for it") == "go for it"

    # Check some edge cases that are easy to work out by hand.
    assert candidate("here") == ""
    assert candidate("here is") == "is"

