"""
AI Generated Solution
Task ID: HumanEval/125
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.297614
"""

def split_words(txt):
    if txt.isspace():
        return list(filter(None, re.split('[^a-zA-Z0-9]+', txt)))
    else:
        return len([c for c in txt if ord(c) % 2 == 0])
