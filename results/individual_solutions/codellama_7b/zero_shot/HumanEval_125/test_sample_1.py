"""
Test for AI Generated Solution
Task ID: HumanEval/125
Model: codellama:7b
"""

def split_words(txt):
    if txt.isspace():
        return list(filter(None, re.split('[^a-zA-Z0-9]+', txt)))
    else:
        return len([c for c in txt if ord(c) % 2 == 0])


def check(candidate):

    assert candidate("Hello world!") == ["Hello","world!"]
    assert candidate("Hello,world!") == ["Hello","world!"]
    assert candidate("Hello world,!") == ["Hello","world,!"]
    assert candidate("Hello,Hello,world !") == ["Hello,Hello,world","!"]
    assert candidate("abcdef") == 3
    assert candidate("aaabb") == 2
    assert candidate("aaaBb") == 1
    assert candidate("") == 0
