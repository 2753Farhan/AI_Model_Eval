"""
AI Generated Solution
Task ID: HumanEval/38
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.166845
"""

def decode_cyclic(s):
    # split the string into groups of 3 characters
    groups = [s[i:i+3] for i in range(0, len(s), 3)]
    # reverse each group
    groups = [group[::-1] for group in groups]
    # join the reversed groups back into a string
    return "".join(groups)