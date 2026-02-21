"""
Test for AI Generated Solution
Task ID: HumanEval/50
Model: codellama:7b
"""

def decode_shift(s):
    return "".join([chr(((ord(ch) - 5 + 26) % 26) + ord("a")) for ch in s])



METADATA = {}


def check(candidate):
    from random import randint, choice
    import copy
    import string

    letters = string.ascii_lowercase
    for _ in range(100):
        str = ''.join(choice(letters) for i in range(randint(10, 20)))
        encoded_str = encode_shift(str)
        assert candidate(copy.deepcopy(encoded_str)) == str

