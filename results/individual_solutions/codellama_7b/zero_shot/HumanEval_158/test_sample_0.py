"""
Test for AI Generated Solution
Task ID: HumanEval/158
Model: codellama:7b
"""

def find_max(words):
    max_length = -1
    result = ""
    for word in words:
        if len(set(word)) > max_length:
            max_length = len(set(word))
            result = word
    return result

# Test case 1:
assert find_max(["name", "of", "string"]) == "string"
# Test case 2:
assert find_max(["name", "enam", "game"]) == "enam"
# Test case 3:
assert find_max(["aaaaaaa", "bb", "cc"]) == "aaaaaaa"

def check(candidate):

    # Check some simple cases
    assert (candidate(["name", "of", "string"]) == "string"), "t1"
    assert (candidate(["name", "enam", "game"]) == "enam"), 't2'
    assert (candidate(["aaaaaaa", "bb", "cc"]) == "aaaaaaa"), 't3'
    assert (candidate(["abc", "cba"]) == "abc"), 't4'
    assert (candidate(["play", "this", "game", "of","footbott"]) == "footbott"), 't5'
    assert (candidate(["we", "are", "gonna", "rock"]) == "gonna"), 't6'
    assert (candidate(["we", "are", "a", "mad", "nation"]) == "nation"), 't7'
    assert (candidate(["this", "is", "a", "prrk"]) == "this"), 't8'

    # Check some edge cases that are easy to work out by hand.
    assert (candidate(["b"]) == "b"), 't9'
    assert (candidate(["play", "play", "play"]) == "play"), 't10'

