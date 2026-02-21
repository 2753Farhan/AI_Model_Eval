"""
AI Generated Solution
Task ID: HumanEval/70
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.221493
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