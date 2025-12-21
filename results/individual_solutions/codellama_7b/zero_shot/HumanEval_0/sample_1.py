"""
AI Generated Solution
Task ID: HumanEval/0
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2025-12-21T18:43:57.648793
"""

def has_close_elements(numbers, threshold):
    for i in range(len(numbers)-1):
        for j in range(i+1, len(numbers)):
            if abs(numbers[j]-numbers[i]) < threshold:
                return True
    return False