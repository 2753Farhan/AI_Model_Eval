"""
AI Generated Solution
Task ID: HumanEval/145
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.327158
"""

def order_by_points(nums):
    """
    Sorts the given list of integers in ascending order according to the sum of their digits.
    If there are several items with similar sum of their digits, order them based on their index in original list.
    :param nums: List of integers
    :return: Sorted list of integers
    """
    # Create a list of tuples containing the number and its digit sum
    tuple_list = [(num, sum(map(int, str(num)))) for num in nums]
    # Sort the list based on the digit sum
    sorted_list = sorted(tuple_list, key=lambda x: x[1])
    # Return the sorted list of integers
    return [x[0] for x in sorted_list]