"""
AI Generated Solution
Task ID: HumanEval/110
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.278059
"""

def exchange(lst1, lst2):
    # Check if both lists are empty
    if not lst1 and not lst2:
        return "NO"

    # Create a set of even numbers from lst1
    even_nums = set(n for n in lst1 if n % 2 == 0)

    # Loop through lst2 and check if any number is divisible by 2
    for num in lst2:
        if num % 2 == 0:
            # If so, add it to the set of even numbers
            even_nums.add(num)

    # Check if the length of the set of even numbers is equal to the length of lst1
    if len(even_nums) == len(lst1):
        return "YES"
    else:
        return "NO"


# Test case 1:
assert exchange([1, 2, 3, 4], [1, 2, 3, 4]) == "YES"
# Test case 2:
assert exchange([1, 2, 3, 4], [1, 5, 3, 4]) == "NO"
# Test case 3:
assert exchange([2, 4, 6, 8], [1, 2, 3, 4]) == "YES"
# Test case 4:
assert exchange([1, 3, 5, 7], [2, 4, 6, 8]) == "NO"
# Test case 5:
assert exchange([2, 4, 6, 8], [2, 4, 6, 8]) == "YES"
# Test case 6:
assert exchange([1, 3, 5, 7], [1, 3, 5, 7]) == "YES"
# Test case 7:
assert exchange([2, 4, 6, 8], [1, 2, 3, 4]) == "YES"
# Test case 8:
assert exchange([1, 3, 5, 7], [2, 4, 6, 8]) == "NO"
# Test case 9:
assert exchange([2, 4, 6, 8], [2, 4, 6, 8]) == "YES"
# Test case 10:
assert exchange([1, 3, 5, 7], [1, 3, 5, 7]) == "YES"