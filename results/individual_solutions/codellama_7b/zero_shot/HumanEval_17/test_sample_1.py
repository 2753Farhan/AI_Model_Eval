"""
Test for AI Generated Solution
Task ID: HumanEval/17
Model: codellama:7b
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



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('') == []
    assert candidate('o o o o') == [4, 4, 4, 4]
    assert candidate('.| .| .| .|') == [1, 1, 1, 1]
    assert candidate('o| o| .| .| o o o o') == [2, 2, 1, 1, 4, 4, 4, 4]
    assert candidate('o| .| o| .| o o| o o|') == [2, 1, 2, 1, 4, 2, 4, 2]
