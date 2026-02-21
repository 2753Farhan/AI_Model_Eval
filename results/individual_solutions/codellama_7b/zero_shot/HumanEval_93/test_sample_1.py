"""
Test for AI Generated Solution
Task ID: HumanEval/93
Model: codellama:7b
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

def check(candidate):

    # Check some simple cases
    assert candidate('TEST') == 'tgst', "This prints if this assert fails 1 (good for debugging!)"
    assert candidate('Mudasir') == 'mWDCSKR', "This prints if this assert fails 2 (good for debugging!)"
    assert candidate('YES') == 'ygs', "This prints if this assert fails 3 (good for debugging!)"
    
    # Check some edge cases that are easy to work out by hand.
    assert candidate('This is a message') == 'tHKS KS C MGSSCGG', "This prints if this assert fails 2 (also good for debugging!)"
    assert candidate("I DoNt KnOw WhAt tO WrItE") == 'k dQnT kNqW wHcT Tq wRkTg', "This prints if this assert fails 2 (also good for debugging!)"

