"""
AI Generated Solution
Task ID: HumanEval/146
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.328158
"""

def specialFilter(nums):
    count = 0
    for num in nums:
        if num > 10 and (num % 10 == 1 or num % 10 == 3 or num % 10 == 5 or num % 10 == 7 or num % 10 == 9):
            count += 1
    return count

# Test cases:
print(specialFilter([15, -73, 14, -15])) # should be 1
print(specialFilter([33, -2, -3, 45, 21, 109])) # should be 2