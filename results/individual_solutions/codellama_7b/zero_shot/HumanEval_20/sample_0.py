"""
AI Generated Solution
Task ID: HumanEval/20
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.128897
"""

def find_closest_elements(numbers):
    # Check if the input list has two or more elements
    if len(numbers) < 2:
        raise ValueError("Input list must have at least two elements")

    # Initialize variables for the closest elements
    closest_elements = (None, None)
    min_diff = float("inf")

    # Iterate over the elements in the list
    for i in range(len(numbers) - 1):
        for j in range(i + 1, len(numbers)):
            # Calculate the difference between the current element and the other element
            diff = abs(numbers[j] - numbers[i])

            # If the difference is less than the current minimum difference, update the closest elements
            if diff < min_diff:
                min_diff = diff
                closest_elements = (numbers[i], numbers[j])

    # Return the closest elements in order
    return closest_elements