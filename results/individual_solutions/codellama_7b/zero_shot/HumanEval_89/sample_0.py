"""
AI Generated Solution
Task ID: HumanEval/89
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.250032
"""

def encrypt(string):
    # Initialize an empty string to store the encrypted message
    encrypted_message = ""

    # Loop through each character in the input string
    for char in string:
        # Check if the character is a letter (i.e., not a space)
        if char.isalpha():
            # If so, encrypt the letter using the caesar cipher
            encrypted_char = chr((ord(char) - ord('a') + 2 * 26) % 26 + ord('a'))
        else:
            # If not a letter, add it to the encrypted message as is
            encrypted_char = char
        # Add the encrypted character to the end of the encrypted message
        encrypted_message += encrypted_char

    return encrypted_message

# Test the function with a sample input
print(encrypt("hello world"))