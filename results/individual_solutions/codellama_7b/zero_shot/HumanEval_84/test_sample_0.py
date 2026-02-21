"""
Test for AI Generated Solution
Task ID: HumanEval/84
Model: codellama:7b
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

def check(candidate):

    # Check some simple cases
    assert True, "This prints if this assert fails 1 (good for debugging!)"
    assert candidate(1000) == "1", "Error"
    assert candidate(150) == "110", "Error"
    assert candidate(147) == "1100", "Error"

    # Check some edge cases that are easy to work out by hand.
    assert True, "This prints if this assert fails 2 (also good for debugging!)"
    assert candidate(333) == "1001", "Error"
    assert candidate(963) == "10010", "Error"

