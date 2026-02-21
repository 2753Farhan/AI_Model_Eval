"""
AI Generated Solution
Task ID: HumanEval/151
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.335690
"""

def double_the_difference(lst):
    # Check if the list is empty
    if len(lst) == 0:
        return 0
    
    # Find the difference between the maximum and minimum elements of the list
    max_elem = max(lst)
    min_elem = min(lst)
    diff = max_elem - min_elem
    
    # Return the sum of squares of the odd numbers in the list
    return sum([x**2 for x in lst if x % 2 != 0]) * 2 + diff**2
