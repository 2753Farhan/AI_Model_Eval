"""
Test for AI Generated Solution
Task ID: HumanEval/118
Model: codellama:7b
"""

def get_closest_vowel(word):
    vowels = ['a', 'e', 'i', 'o', 'u']
    for i in range(len(word)-1, -1, -1):
        if word[i] in vowels:
            if i < len(word)-1 and word[i+1] not in vowels:
                return word[i]
            elif i > 0 and word[i-1] not in vowels:
                return word[i]
    return ''


# Test cases:
print(get_closest_vowel("yogurt")) # u
print(get_closest_vowel("FULL")) # U
print(get_closest_vowel("quick")) # ""
print(get_closest_vowel("ab")) # ""

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

