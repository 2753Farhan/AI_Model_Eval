"""
Test for AI Generated Solution
Task ID: HumanEval/70
Model: codellama:7b
"""

def strange_sort_list(my_list):
    """
    Given a list of integers, return a list in a strange order.
    The strange order is when you start with the minimum value,
    then maximum of the remaining integers, then minimum and so on.
    """
    if not my_list:
        return []

    # Sort the list in ascending order
    my_list.sort()

    # Create a new list to store the sorted values
    sorted_list = []

    # Append the minimum value to the new list
    sorted_list.append(my_list[0])

    # Remove the minimum value from the original list
    my_list.remove(my_list[0])

    # Loop through the remaining values in the list
    for i in range(len(my_list)):
        # Append the maximum value to the new list
        sorted_list.append(max(my_list))

        # Remove the maximum value from the original list
        my_list.remove(max(my_list))

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

