"""
AI Generated Solution
Task ID: HumanEval/89
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.250032
"""

def encrypt(string):
    # Initialize an empty string to store the encrypted message
    encrypted_message = ""

    # Iterate through each character in the input string
    for char in string:
        # Check if the character is uppercase
        if char.isupper():
            # Shift the character up by two multiplied by two places in the alphabet
            encrypted_message += chr((ord(char) - ord('A') + 2 * 2) % 26 + ord('A'))
        # Check if the character is lowercase
        elif char.islower():
            # Shift the character down by two multiplied by two places in the alphabet
            encrypted_message += chr((ord(char) - ord('a') + 2 * 2) % 26 + ord('a'))
        # If the character is a space, add it to the encrypted message as is
        elif char == " ":
            encrypted_message += " "
    return encrypted_message