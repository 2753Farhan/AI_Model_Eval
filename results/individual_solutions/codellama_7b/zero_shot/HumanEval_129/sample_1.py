"""
AI Generated Solution
Task ID: HumanEval/129
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.304129
"""

def minPath(grid, k):
    # Initialize the distance array with infinite distance
    distance = [[float('inf') for _ in range(len(grid[0]))] for _ in range(len(grid))]

    # Initialize the previous array with -1
    previous = [[-1 for _ in range(len(grid[0]))] for _ in range(len(grid))]

    # Initialize the queue with the starting node
    queue = [(0, 0)]

    # Loop until the queue is empty
    while queue:
        # Dequeue the node from the queue
        node = queue.pop(0)

        # Check if the node has not been visited before and if it is within the boundaries of the grid
        if node not in distance and 0 <= node[0] < len(grid) and 0 <= node[1] < len(grid[0]):
            # Get the current row and column from the node
            row, col = node

            # Loop through all the neighbors of the current node
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == j == 0:
                        continue

                    # Get the next row and column
                    next_row = row + i
                    next_col = col + j

                    # Check if the next node is within the boundaries of the grid
                    if 0 <= next_row < len(grid) and 0 <= next_col < len(grid[0]):
                        # Calculate the distance to the next node
                        distance_to_next = distance[row][col] + abs(grid[next_row][next_col] - grid[row][col])

                        # Check if the distance to the next node is less than the current distance
                        if distance_to_next < distance[next_row][next_col]:
                            # Update the distance and previous arrays
                            distance[next_row][next_col] = distance_to_next
                            previous[next_row][next_col] = node

                            # Add the next node to the queue
                            queue.append((next_row, next_col))

    # Initialize the path with the starting node
    path = [(0, 0)]

    # Loop until the destination node is reached
    while previous[path[-1][0]][path[-1][1]] != -1:
        # Add the next node to the path
        node = previous[path[-1][0]][path[-1][1]]
        path.append(node)

    # Return the path
    return path