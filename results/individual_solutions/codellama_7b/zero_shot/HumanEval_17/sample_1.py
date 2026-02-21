"""
AI Generated Solution
Task ID: HumanEval/17
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.122389
"""

def parse_music(music_string):
    notes = []
    for char in music_string:
        if char == 'o':
            notes.append(4)
        elif char == '|':
            notes.append(2)
        else:
            notes.append(1)
    return notes