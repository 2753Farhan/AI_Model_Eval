"""
Test for AI Generated Solution
Task ID: HumanEval/38
Model: codellama:7b
"""

def decode_cyclic(s):
    # split the input string into groups of 3 characters
    groups = [s[i:i+3] for i in range(0, len(s), 3)]
    # join the elements of each group in reverse order
    decoded_str = "".join([group[::-1] for group in groups])
    return decoded_str



METADATA = {}


def check(candidate):
    from random import randint, choice
    import string

    letters = string.ascii_lowercase
    for _ in range(100):
        str = ''.join(choice(letters) for i in range(randint(10, 20)))
        encoded_str = encode_cyclic(str)
        assert candidate(encoded_str) == str

