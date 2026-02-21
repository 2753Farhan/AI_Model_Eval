"""
AI Generated Solution
Task ID: HumanEval/137
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.316646
"""

def compare_one(a, b):
    # Convert both variables to floats if they are not already
    a = float(a)
    b = float(b)

    # Check if the values are equal
    if a == b:
        return None

    # Return the larger value
    if a > b:
        return a
    else:
        return b