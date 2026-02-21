"""
AI Generated Solution
Task ID: HumanEval/38
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.167847
"""

def decode_cyclic(s):
    # split the input string into groups of 3 characters
    groups = [s[i:i+3] for i in range(0, len(s), 3)]
    # join the elements of each group in reverse order
    decoded_str = "".join([group[::-1] for group in groups])
    return decoded_str