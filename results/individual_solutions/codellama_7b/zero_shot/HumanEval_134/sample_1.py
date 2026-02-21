"""
AI Generated Solution
Task ID: HumanEval/134
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.311128
"""

def check_if_last_char_is_a_letter(txt):
    if txt == "":
        return False
    else:
        last_char = txt[-1]
        if last_char.isalpha() and last_char not in " ":
            return True
        else:
            return False