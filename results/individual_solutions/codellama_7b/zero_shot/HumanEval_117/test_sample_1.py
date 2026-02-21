"""
Test for AI Generated Solution
Task ID: HumanEval/117
Model: codellama:7b
"""

def select_words(s, n):
    words = []
    for word in s.split():
        if len([c for c in word if c.isalpha() and not c.lower() in 'aeiou']) == n:
            words.append(word)
    return words


# Test case 1:
assert select_words("Mary had a little lamb", 4) == ["little"]
# Test case 2:
assert select_words("Mary had a little lamb", 3) == ["Mary", "lamb"]
# Test case 3:
assert select_words("simple white space", 2) == []
# Test case 4:
assert select_words("Hello world", 4) == ["world"]
# Test case 5:
assert select_words("Uncle sam", 3) == ["Uncle"]

def check(candidate):

    # Check some simple cases
    assert candidate("Mary had a little lamb", 4) == ["little"], "First test error: " + str(candidate("Mary had a little lamb", 4))      
    assert candidate("Mary had a little lamb", 3) == ["Mary", "lamb"], "Second test error: " + str(candidate("Mary had a little lamb", 3))  
    assert candidate("simple white space", 2) == [], "Third test error: " + str(candidate("simple white space", 2))      
    assert candidate("Hello world", 4) == ["world"], "Fourth test error: " + str(candidate("Hello world", 4))  
    assert candidate("Uncle sam", 3) == ["Uncle"], "Fifth test error: " + str(candidate("Uncle sam", 3))


    # Check some edge cases that are easy to work out by hand.
    assert candidate("", 4) == [], "1st edge test error: " + str(candidate("", 4))
    assert candidate("a b c d e f", 1) == ["b", "c", "d", "f"], "2nd edge test error: " + str(candidate("a b c d e f", 1))

