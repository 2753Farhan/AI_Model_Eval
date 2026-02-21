"""
AI Generated Solution
Task ID: HumanEval/105
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.272059
"""

def by_length(arr):
    # Sort the array
    sorted_arr = sorted(arr)

    # Reverse the sorted array
    reversed_arr = sorted_arr[::-1]

    # Replace each digit with its corresponding name
    name_arr = []
    for num in reversed_arr:
        if num >= 1 and num <= 9:
            name_arr.append(num_to_name(num))
        else:
            name_arr.append(str(num))

    return name_arr

def num_to_name(num):
    if num == 1:
        return "One"
    elif num == 2:
        return "Two"
    elif num == 3:
        return "Three"
    elif num == 4:
        return "Four"
    elif num == 5:
        return "Five"
    elif num == 6:
        return "Six"
    elif num == 7:
        return "Seven"
    elif num == 8:
        return "Eight"
    elif num == 9:
        return "Nine"
    else:
        return str(num)