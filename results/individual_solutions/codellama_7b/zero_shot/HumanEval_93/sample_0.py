"""
AI Generated Solution
Task ID: HumanEval/93
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.256039
"""

def encode(message):
    # Create a new string with the encoded message
    encoded_message = ""

    # Loop through each character in the message
    for char in message:
        # Check if the character is a letter (a-z or A-Z)
        if char.isalpha():
            # If it is a letter, check if it is a vowel
            if char.lower() in "aeiou":
                # If it is a vowel, get the index of the character in the alphabet
                index = ord(char) - ord("a")
                # Add 2 to the index to get the position of the letter that should replace the vowel
                replacement_index = index + 2
                # Get the character at the replacement index
                replacement_char = chr(ord("a") + replacement_index)
                # Replace the vowel with the new character
                encoded_message += replacement_char
            else:
                # If it is not a vowel, just uppercase or lowercase it based on the original case
                if char.isupper():
                    encoded_message += char.lower()
                else:
                    encoded_message += char.upper()
        else:
            # If the character is not a letter, just add it to the encoded message as is
            encoded_message += char

    return encoded_message