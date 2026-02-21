"""
AI Generated Solution
Task ID: HumanEval/111
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.279059
"""

def histogram(test):
    """Given a string representing a space separated lowercase letters, return a dictionary
    of the letter with the most repetition and containing the corresponding count.
    If several letters have the same occurrence, return all of them.
    
    Example:
    histogram('a b c') == {'a': 1, 'b': 1, 'c': 1}
    histogram('a b b a') == {'a': 2, 'b': 2}
    histogram('a b c a b') == {'a': 2, 'b': 2}
    histogram('b b b b a') == {'b': 4}
    histogram('') == {}

    """
    # split the string into individual letters
    letters = test.split()
    # create an empty dictionary to store the counts
    count_dict = {}
    # loop through each letter and increment the count
    for letter in letters:
        if letter not in count_dict:
            count_dict[letter] = 1
        else:
            count_dict[letter] += 1
    # sort the dictionary by value in descending order
    sorted_dict = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
    # get the most frequent letter
    most_frequent = sorted_dict[0][0]
    # if there are multiple letters with the same frequency, return all of them
    if len(sorted_dict) > 1 and sorted_dict[0][1] == sorted_dict[1][1]:
        return {letter: count_dict[letter] for letter in sorted_dict}
    else:
        return {most_frequent: count_dict[most_frequent]}