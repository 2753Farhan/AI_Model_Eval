"""
Test for AI Generated Solution
Task ID: HumanEval/70
Model: codellama:7b
"""

def strange_sort_list(my_list):
    """
    Sort a list in a strange order.

    Args:
        my_list (list): List of integers to be sorted.

    Returns:
        list: Sorted list in the strange order.
    """
    if not my_list:
        return []

    # Sort the list first
    my_list.sort()

    # Create a new list to store the sorted values
    sorted_list = []

    # Append the minimum value
    sorted_list.append(my_list[0])

    # Append the maximum of the remaining integers
    sorted_list.append(max(my_list[1:]))

    # Append the minimum of the remaining integers
    sorted_list.append(min(my_list[1:]))

    # Return the sorted list
    return sorted_list

def check(candidate):

    # Check some simple cases
    assert candidate([1, 2, 3, 4]) == [1, 4, 2, 3]
    assert candidate([5, 6, 7, 8, 9]) == [5, 9, 6, 8, 7]
    assert candidate([1, 2, 3, 4, 5]) == [1, 5, 2, 4, 3]
    assert candidate([5, 6, 7, 8, 9, 1]) == [1, 9, 5, 8, 6, 7]
    assert candidate([5, 5, 5, 5]) == [5, 5, 5, 5]
    assert candidate([]) == []
    assert candidate([1,2,3,4,5,6,7,8]) == [1, 8, 2, 7, 3, 6, 4, 5]
    assert candidate([0,2,2,2,5,5,-5,-5]) == [-5, 5, -5, 5, 0, 2, 2, 2]
    assert candidate([111111]) == [111111]

    # Check some edge cases that are easy to work out by hand.
    assert True

