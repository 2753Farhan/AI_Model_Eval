"""
AI Generated Solution
Task ID: HumanEval/97
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.261548
"""

def multiply(a, b):
    product = 0
    for i in range(len(str(a))):
        for j in range(len(str(b))):
            product += int(str(a)[i]) * int(str(b)[j])
    return product % 10


# Test cases:
print(multiply(148, 412)) # Should be 16
print(multiply(19, 28)) # Should be 72
print(multiply(2020, 1851)) # Should be 0
print(multiply(14,-15)) # Should be 20