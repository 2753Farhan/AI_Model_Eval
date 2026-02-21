"""
AI Generated Solution
Task ID: HumanEval/82
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.238012
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