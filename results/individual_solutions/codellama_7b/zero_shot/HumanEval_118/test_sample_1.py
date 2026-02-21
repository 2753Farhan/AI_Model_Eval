"""
Test for AI Generated Solution
Task ID: HumanEval/118
Model: codellama:7b
"""

def get_closest_vowel(word):
    # Find the index of the last consonant in the word
    last_consonant_index = len(word) - 1
    while last_consonant_index >= 0 and word[last_consonant_index].islower():
        last_consonant_index -= 1

    # If there are no consonants in the word, return an empty string
    if last_consonant_index == -1:
        return ""

    # Find the index of the first vowel after the last consonant
    first_vowel_index = last_consonant_index + 1
    while first_vowel_index < len(word) and not word[first_vowel_index].islower():
        first_vowel_index += 1

    # If there are no vowels in the word, return an empty string
    if first_vowel_index == len(word):
        return ""

    # Return the vowel that is closest to the last consonant
    return word[first_vowel_index]

def check(candidate):

    # Check some simple cases
    assert candidate("yogurt") == "u"
    assert candidate("full") == "u"
    assert candidate("easy") == ""
    assert candidate("eAsy") == ""
    assert candidate("ali") == ""
    assert candidate("bad") == "a"
    assert candidate("most") == "o"
    assert candidate("ab") == ""
    assert candidate("ba") == ""
    assert candidate("quick") == ""
    assert candidate("anime") == "i"
    assert candidate("Asia") == ""
    assert candidate("Above") == "o"

    # Check some edge cases that are easy to work out by hand.
    assert True

