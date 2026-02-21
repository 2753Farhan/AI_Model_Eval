"""
AI Generated Solution
Task ID: HumanEval/93
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.256039
"""

def encode(message):
    # Initialize an empty string to store the encoded message
    encoded_message = ""

    # Loop through each character in the message
    for char in message:
        # If the character is a letter...
        if char.isalpha():
            # ...convert it to uppercase
            char = char.upper()
            # Check if the character is a vowel
            if char in "AEIOU":
                # If it is, replace it with the letter that appears 2 places ahead of it in the alphabet
                char = chr((ord(char) + 2 - ord("A")) % 26 + ord("A"))
        # Add the encoded character to the encoded message
        encoded_message += char

    # Return the encoded message
    return encoded_message