"""
AI Generated Solution
Task ID: HumanEval/50
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.187866
"""

def decode_shift(s):
    return "".join([chr(((ord(ch) - 5 + 26) % 26) + ord("a")) for ch in s])