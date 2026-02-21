"""
AI Generated Solution
Task ID: HumanEval/121
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.293080
"""

def solution(my_list):
    # Check if the list is empty
    if not my_list:
        return 0

    # Initialize a variable to store the sum
    sum = 0

    # Iterate over the list and calculate the sum of the odd elements in even positions
    for i in range(len(my_list)):
        if i % 2 == 0 and my_list[i] % 2 != 0:
            sum += my_list[i]

    # Return the sum
    return sum