"""
AI Generated Solution
Task ID: HumanEval/105
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.271053
"""

def by_length(arr):
    result = []
    # Sort the array in ascending order
    sorted_arr = sorted(arr)
    # Reverse the sorted array
    reversed_arr = sorted_arr[::-1]
    # Loop through the reversed array and append the corresponding name to the result list
    for num in reversed_arr:
        if num >= 1 and num <= 9:
            result.append(str(num) + " " + {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"}.get(num))
        else:
            result.append(str(num))
    return result