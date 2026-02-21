"""
AI Generated Solution
Task ID: HumanEval/50
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.187359
"""

def decode_shift(s: str):
  """
  takes as input string encoded with encode_shift function. Returns decoded string.
  """
  return "".join([chr(((ord(ch) - 5 + 26) % 26) + ord("a")) for ch in s])