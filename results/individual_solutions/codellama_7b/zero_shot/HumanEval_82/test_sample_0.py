"""
Test for AI Generated Solution
Task ID: HumanEval/82
Model: codellama:7b
"""

def prime_length(string):
    string_length = len(string)
    if is_prime(string_length):
        return True
    else:
        return False

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Test the function with a few examples
print(prime_length('Hello')) # should be True
print(prime_length('abcdcba')) # should be True
print(prime_length('kittens')) # should be True
print(prime_length('orange')) # should be False

def check(candidate):

    # Check some simple cases
    assert candidate('Hello') == True
    assert candidate('abcdcba') == True
    assert candidate('kittens') == True
    assert candidate('orange') == False
    assert candidate('wow') == True
    assert candidate('world') == True
    assert candidate('MadaM') == True
    assert candidate('Wow') == True
    assert candidate('') == False
    assert candidate('HI') == True
    assert candidate('go') == True
    assert candidate('gogo') == False
    assert candidate('aaaaaaaaaaaaaaa') == False

    # Check some edge cases that are easy to work out by hand.
    assert candidate('Madam') == True
    assert candidate('M') == False
    assert candidate('0') == False

