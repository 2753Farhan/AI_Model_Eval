"""
AI Generated Solution
Task ID: HumanEval/122
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.294080
"""

def add_elements(arr, k):
    # Initialize a variable to store the sum
    sum = 0

    # Iterate over the first k elements of the array
    for i in range(k):
        # If the element is less than or equal to 10, include it in the sum
        if arr[i] <= 10:
            sum += arr[i]

    # Return the sum
    return sum