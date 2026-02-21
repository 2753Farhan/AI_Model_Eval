"""
AI Generated Solution
Task ID: HumanEval/67
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.216984
"""

def fruit_distribution(s, n):
    apples = int(s.split("and")[0].strip(" ").split(" ")[0])
    oranges = int(s.split("and")[1].strip(" ").split(" ")[0])
    return n - apples - oranges

# Test case 1:
assert fruit_distribution("5 apples and 6 oranges", 19) == 8
# Test case 2:
assert fruit_distribution("0 apples and 1 oranges", 3) == 2
# Test case 3:
assert fruit_distribution("2 apples and 3 oranges", 100) == 95
# Test case 4:
assert fruit_distribution("100 apples and 1 oranges", 120) == 19