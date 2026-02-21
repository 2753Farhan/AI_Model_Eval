"""
AI Generated Solution
Task ID: HumanEval/104
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.271053
"""

def unique_digits(my_list):
    result = []
    for num in my_list:
        if all(digit % 2 != 0 for digit in str(num)):
            result.append(num)
    return sorted(result)