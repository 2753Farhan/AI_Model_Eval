"""
Test for AI Generated Solution
Task ID: HumanEval/125
Model: codellama:7b
"""

def split_words(txt):
    # Check if the string contains any whitespaces
    if ' ' in txt or '\t' in txt:
        return txt.split()
    # If not, check if it contains any commas
    elif ',' in txt:
        return [word for word in txt.split(',') if word]
    # If not, return the number of lower-case letters with odd order in the alphabet
    else:
        count = 0
        for char in txt:
            if char.islower():
                count += (ord(char) - ord('a')) % 2 + 1
        return count


def check(candidate):

    assert candidate("Hello world!") == ["Hello","world!"]
    assert candidate("Hello,world!") == ["Hello","world!"]
    assert candidate("Hello world,!") == ["Hello","world,!"]
    assert candidate("Hello,Hello,world !") == ["Hello,Hello,world","!"]
    assert candidate("abcdef") == 3
    assert candidate("aaabb") == 2
    assert candidate("aaaBb") == 1
    assert candidate("") == 0
