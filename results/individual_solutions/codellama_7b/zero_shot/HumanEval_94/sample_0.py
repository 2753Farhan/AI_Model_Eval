"""
AI Generated Solution
Task ID: HumanEval/94
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.257038
"""

def largest_prime_sum(my_list):
    # find the largest prime number in the list
    largest_prime = max([x for x in my_list if is_prime(x)], default=0)

    # return the sum of its digits
    if largest_prime == 0:
        return 0
    else:
        return sum(str(largest_prime))

def is_prime(n):
    if n == 1 or n == 0:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True