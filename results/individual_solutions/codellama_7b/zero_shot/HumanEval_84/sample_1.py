"""
AI Generated Solution
Task ID: HumanEval/84
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.242524
"""

def solve(n):
    # Convert the integer to a binary string
    bin_str = bin(n)[2:]
    # Initialize the sum variable
    sum = 0
    # Iterate through the binary string and calculate the sum of its digits
    for i in range(len(bin_str)):
        sum += int(bin_str[i])
    # Return the sum as a string in binary format
    return bin(sum)[2:]