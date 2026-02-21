"""
AI Generated Solution
Task ID: HumanEval/96
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.259038
"""

def count_up_to(n):
    if n < 0:
        return []
    prime_numbers = []
    for i in range(2, n+1):
        if i > 1:
            for j in range(2, int(i**0.5) + 1):
                if i % j == 0:
                    break
            else:
                prime_numbers.append(i)
    return prime_numbers

# Test case 1:
assert count_up_to(5) == [2,3]
# Test case 2:
assert count_up_to(11) == [2,3,5,7]
# Test case 3:
assert count_up_to(0) == []
# Test case 4:
assert count_up_to(20) == [2,3,5,7,11,13,17,19]
# Test case 5:
assert count_up_to(1) == []
# Test case 6:
assert count_up_to(18) == [2,3,5,7,11,13,17]