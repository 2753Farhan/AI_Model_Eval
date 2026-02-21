"""
Test for AI Generated Solution
Task ID: HumanEval/41
Model: codellama:7b
"""

def car_race_collision(n):
    # Initialize a list to store the positions of the cars
    positions = [0] * (2 * n)

    # Initialize the speeds of the cars
    speeds = [1] * n + [-1] * n

    # Initialize the number of collisions to 0
    collisions = 0

    # Loop through each position and speed combination
    for i in range(2 * n):
        # Update the positions of the cars
        for j in range(n):
            positions[i + j] += speeds[j]

        # Check for collisions
        for j in range(n - 1):
            if positions[i + j] * positions[i + j + 1] < 0:
                collisions += 1

    # Return the number of collisions
    return collisions



METADATA = {}


def check(candidate):
    assert candidate(2) == 4
    assert candidate(3) == 9
    assert candidate(4) == 16
    assert candidate(8) == 64
    assert candidate(10) == 100

