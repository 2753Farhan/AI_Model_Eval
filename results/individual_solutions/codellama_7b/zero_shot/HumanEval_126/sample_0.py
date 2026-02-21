"""
AI Generated Solution
Task ID: HumanEval/126
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.298621
"""

def is_sorted(lst):
    # Check if list has more than one duplicate of the same number
    if len(lst) != len(set(lst)):
        return False

    # Sort the list and check if it's ascending
    sorted_list = sorted(lst)
    for i in range(len(sorted_list) - 1):
        if sorted_list[i] > sorted_list[i + 1]:
            return False
    return True

# Test case 1:
print(is_sorted([5]))  # True
# Test case 2:
print(is_sorted([1, 2, 3, 4, 5]))  # True
# Test case 3:
print(is_sorted([1, 3, 2, 4, 5]))  # False
# Test case 4:
print(is_sorted([1, 2, 3, 4, 5, 6]))  # True
# Test case 5:
print(is_sorted([1, 2, 3, 4, 5, 6, 7]))  # True
# Test case 6:
print(is_sorted([1, 3, 2, 4, 5, 6, 7]))  # False
# Test case 7:
print(is_sorted([1, 2, 2, 3, 3, 4]))  # True
# Test case 8:
print(is_sorted([1, 2, 2, 2, 3, 4]))  # False