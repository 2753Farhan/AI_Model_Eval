"""
AI Generated Solution
Task ID: HumanEval/116
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.285568
"""

def sort_array(arr):
    # create a list of tuples containing the binary representation of each element and its decimal value
    data = [(bin(x)[2:], x) for x in arr]
    # sort the list based on the number of ones in the binary representation
    data.sort(key=lambda x: (x[0].count('1'), x[1]))
    # return the decimal value of each tuple
    return [x[1] for x in data]