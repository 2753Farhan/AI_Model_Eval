"""
AI Generated Solution
Task ID: HumanEval/87
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.246526
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