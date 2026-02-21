"""
Test for AI Generated Solution
Task ID: HumanEval/87
Model: codellama:7b
"""


def get_row(lst, x):
    # Initialize an empty list to store the coordinates
    coords = []

    # Iterate through the nested lists
    for i, row in enumerate(lst):
        # Find the first occurrence of the target value in the current row
        try:
            j = row.index(x)
        # If the value is not found, skip to the next row
        except ValueError:
            continue
        # Otherwise, add the coordinate to the list
        coords.append((i, j))

    # Sort the coordinates initially by rows in ascending order
    coords.sort(key=lambda x: x[0])

    # For each row, sort the coordinates by columns in descending order
    for i in range(len(coords)):
        coords[i] = (coords[i][0], len(lst[coords[i][0]]) - coords[i][1] - 1)

    return coords

# Test cases:
print(get_row([], 1)) # []
print(get_row([[], [1], [1, 2, 3]], 3)) # [(2, 2)]
print(get_row([
      [1,2,3,4,5,6],
      [1,2,3,4,1,6],
      [1,2,3,4,5,1]
    ], 1)) # [(0, 0), (1, 4), (1, 0), (2, 5), (2, 0)]

def check(candidate):

    # Check some simple cases
    assert candidate([
        [1,2,3,4,5,6],
        [1,2,3,4,1,6],
        [1,2,3,4,5,1]
    ], 1) == [(0, 0), (1, 4), (1, 0), (2, 5), (2, 0)]
    assert candidate([
        [1,2,3,4,5,6],
        [1,2,3,4,5,6],
        [1,2,3,4,5,6],
        [1,2,3,4,5,6],
        [1,2,3,4,5,6],
        [1,2,3,4,5,6]
    ], 2) == [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]
    assert candidate([
        [1,2,3,4,5,6],
        [1,2,3,4,5,6],
        [1,1,3,4,5,6],
        [1,2,1,4,5,6],
        [1,2,3,1,5,6],
        [1,2,3,4,1,6],
        [1,2,3,4,5,1]
    ], 1) == [(0, 0), (1, 0), (2, 1), (2, 0), (3, 2), (3, 0), (4, 3), (4, 0), (5, 4), (5, 0), (6, 5), (6, 0)]
    assert candidate([], 1) == []
    assert candidate([[1]], 2) == []
    assert candidate([[], [1], [1, 2, 3]], 3) == [(2, 2)]

    # Check some edge cases that are easy to work out by hand.
    assert True

