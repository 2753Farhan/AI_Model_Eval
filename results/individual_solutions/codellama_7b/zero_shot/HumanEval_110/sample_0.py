"""
AI Generated Solution
Task ID: HumanEval/110
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.277059
"""

def exchange(lst1, lst2):
    # Check if both lists are empty
    if not lst1 and not lst2:
        return "NO"

    # Create a set of even numbers from lst1
    even_nums = set(n for n in lst1 if n % 2 == 0)

    # Loop through lst2 and try to find a match in even_nums
    for num in lst2:
        if num in even_nums:
            # If a match is found, remove the number from even_nums
            even_nums.remove(num)
            # If even_nums is empty, return "YES"
            if not even_nums:
                return "YES"
        else:
            # If no match is found, return "NO"
            return "NO"

    # If we reach this point, it means that we did not find a match in lst2
    # for any of the numbers in even_nums, so return "NO"
    return "NO"


# Test cases:
print(exchange([1, 2, 3, 4], [1, 2, 3, 4]))  # Should print "YES"
print(exchange([1, 2, 3, 4], [1, 5, 3, 4]))  # Should print "NO"
print(exchange([], []))  # Should print "NO"
print(exchange([1, 3, 5], [2, 4, 6]))  # Should print "NO"