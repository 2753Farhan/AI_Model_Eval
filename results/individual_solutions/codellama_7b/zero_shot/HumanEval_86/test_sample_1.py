"""
Test for AI Generated Solution
Task ID: HumanEval/86
Model: codellama:7b
"""

def anti_shuffle(s):
    # Split the string into a list of words using split()
    words = s.split()
    
    # Iterate through the words and sort them alphabetically
    for i in range(len(words)):
        words[i] = ''.join(sorted(words[i]))
    
    # Join the sorted words back into a string
    return ' '.join(words)

def check(candidate):

    # Check some simple cases
    assert candidate('Hi') == 'Hi'
    assert candidate('hello') == 'ehllo'
    assert candidate('number') == 'bemnru'
    assert candidate('abcd') == 'abcd'
    assert candidate('Hello World!!!') == 'Hello !!!Wdlor'
    assert candidate('') == ''
    assert candidate('Hi. My name is Mister Robot. How are you?') == '.Hi My aemn is Meirst .Rboot How aer ?ouy'
    # Check some edge cases that are easy to work out by hand.
    assert True

