"""
AI Generated Solution
Task ID: HumanEval/41
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.170847
"""

def car_race_collision(n):
    """
    n: an integer representing the number of cars driving on the road

    Returns:
    int, the number of collisions that occur between the two sets of cars
    """

    # Initialize a list to store the positions of the cars
    positions = [0] * (2 * n)

    # Initialize variables to keep track of the collisions
    left_to_right_collisions = 0
    right_to_left_collisions = 0

    # Loop through each position on the road
    for i in range(len(positions)):
        # Check if there are any collisions between the two sets of cars
        if positions[i] == n:
            left_to_right_collisions += 1
        elif positions[i] == 2 * n - 1:
            right_to_left_collisions += 1

        # Update the position of each car
        for j in range(n):
            if positions[i] == 2 * j + 1:
                positions[i] = 2 * (j + 1) + 1
            elif positions[i] == 2 * j + 2:
                positions[i] = 2 * j + 2

    # Return the total number of collisions
    return left_to_right_collisions + right_to_left_collisions


def main():
    print(car_race_collision(int(input("Enter the value of n: "))))


if __name__ == "__main__":
    main()