"""
AI Generated Solution
Task ID: HumanEval/84
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.242524
"""

def solve(N):
    # Convert the integer to a binary string
    bin_str = bin(N)[2:]
    
    # Initialize the sum of digits to 0
    sum_digits = 0
    
    # Iterate over the binary string and calculate the sum of digits
    for digit in bin_str:
        sum_digits += int(digit)
    
    # Return the sum of digits as a string in binary
    return str(sum_digits)
    

# Test case 1:
print(solve(1000)) # "1"
# Test case 2:
print(solve(150)) # "110"
# Test case 3:
print(solve(147)) # "1100"