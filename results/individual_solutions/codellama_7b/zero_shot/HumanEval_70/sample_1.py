"""
AI Generated Solution
Task ID: HumanEval/70
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.222492
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