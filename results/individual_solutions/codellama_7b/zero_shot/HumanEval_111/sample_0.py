"""
AI Generated Solution
Task ID: HumanEval/111
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.279059
"""

def histogram(test):
    letter_count = {}
    for letter in test:
        if letter not in letter_count:
            letter_count[letter] = 1
        else:
            letter_count[letter] += 1
    max_occurence = max([value for value in letter_count.values()])
    result = {key: value for key, value in letter_count.items() if value == max_occurence}
    return result

test = "a b c"
print(histogram(test)) # Output: {'a': 1, 'b': 1, 'c': 1}

test = "a b b a"
print(histogram(test)) # Output: {'a': 2, 'b': 2}

test = "a b c a b"
print(histogram(test)) # Output: {'a': 2, 'b': 2}

test = "b b b b a"
print(histogram(test)) # Output: {'b': 4}

test = ""
print(histogram(test)) # Output: {}