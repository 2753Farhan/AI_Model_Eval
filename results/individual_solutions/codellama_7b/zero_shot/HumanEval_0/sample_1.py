"""
AI Generated Solution
Task ID: HumanEval/0
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.078711
"""

def has_close_elements(numbers, threshold):
    for i in range(len(numbers)-1):
        for j in range(i+1, len(numbers)):
            if abs(numbers[i]-numbers[j])<threshold:
                return True
    return False