"""
AI Generated Solution
Task ID: HumanEval/115
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.283569
"""

def max_fill(grid, capacity):
    # Initialize variables
    n_rows = len(grid)
    n_cols = len(grid[0])
    filled_wells = []
    current_row = 0
    current_col = 0
    total_filled = 0
    total_emptied = 0
    steps = 0

    # Loop until all wells are filled or emptied
    while True:
        # If the current row is at the bottom of the grid, go to the next column
        if current_row == n_rows - 1:
            current_col += 1
            current_row = 0

        # If the current column is at the end of the grid, return the total number of steps
        if current_col == n_cols:
            return steps

        # If the current well is already filled or emptied, skip it
        if (current_row, current_col) in filled_wells or (current_row, current_col) in total_emptied:
            current_row += 1
            continue

        # If the capacity of the bucket is greater than the amount of water in the well, fill it
        if grid[current_row][current_col] <= capacity - total_filled:
            filled_wells.append((current_row, current_col))
            total_filled += grid[current_row][current_col]
            current_row += 1
        # Otherwise, empty the bucket at the current well and add it to the list of emptied wells
        else:
            total_emptied.append((current_row, current_col))
            current_row += 1

        # Increment the step counter
        steps += 1

# Test cases
grid = [[0,0,1,0], [0,1,0,0], [1,1,1,1]]
print(max_fill(grid, 1)) # Output: 6

grid = [[0,0,1,1], [0,0,0,0], [1,1,1,1], [0,1,1,1]]
print(max_fill(grid, 2)) # Output: 5

grid = [[0,0,0], [0,0,0]]
print(max_fill(grid, 5)) # Output: 0