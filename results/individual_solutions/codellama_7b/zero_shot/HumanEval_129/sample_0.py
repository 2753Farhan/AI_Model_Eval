"""
AI Generated Solution
Task ID: HumanEval/129
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.303129
"""

def minPath(grid, k):
    # Initialize the distance array with infinite distance
    distances = [[float("inf") for _ in range(len(grid[0]))] for _ in range(len(grid))]

    # Initialize the previous array with -1 values
    previous = [[-1 for _ in range(len(grid[0]))] for _ in range(len(grid))]

    # Initialize the distance and previous values for the starting cell
    distances[0][0] = 0
    previous[0][0] = -1

    # Loop through each cell in the grid
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            # If the current cell is not the starting cell
            if i != 0 or j != 0:
                # Calculate the distance to the previous cell
                distance = 1 + min(distances[i-1][j], distances[i][j-1], distances[i-1][j-1])

                # If the distance is less than the current distance, update it
                if distance < distances[i][j]:
                    distances[i][j] = distance
                    previous[i][j] = previous[i-1][j-1] if distances[i-1][j-1] < distances[i-1][j] else previous[i-1][j]

    # Find the shortest path
    path = []
    cell = (len(grid) - 1, len(grid[0]) - 1)
    while cell != (-1, -1):
        path.append(grid[cell[0]][cell[1]])
        cell = (previous[cell[0]][cell[1]], cell[1]) if previous[cell[0]][cell[1]] != -1 else (cell[0], previous[cell[0]][cell[1]])

    # Reverse the path and return it
    return list(reversed(path))