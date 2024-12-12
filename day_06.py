import enum
import time

from util.grid_utils import Direction


def position_is_on_grid(position: tuple, grid_width: int, grid_height: int):
    return 0 <= position[0] < grid_width and 0 <= position[1] < grid_height


def perform_guard_walk(obstacle_positions: set, guard_start_position: tuple, guard_start_direction: Direction,
                       grid_width: int, grid_height: int) -> tuple:
    """Returns a tuple of (loop, visited_set)."""
    visited_set = set()
    current_guard_position = guard_start_position
    current_guard_direction = guard_start_direction
    while position_is_on_grid(current_guard_position, grid_width, grid_height):
        next_guard_position = (current_guard_position[0] + current_guard_direction.value.x,
                               current_guard_position[1] + current_guard_direction.value.y)
        if next_guard_position in obstacle_positions:
            current_guard_direction = current_guard_direction.turn_90_degrees()
        else:
            if (next_guard_position, current_guard_direction) in visited_set:
                visited_set.add((next_guard_position, current_guard_direction))
                return True, set([position for position, _ in visited_set])
            visited_set.add((next_guard_position, current_guard_direction))
            current_guard_position = next_guard_position
    return False, set([position for position, _ in visited_set])


def part_1(obstacle_positions: set, guard_start_position: tuple, guard_start_direction: Direction,
           grid_width: int, grid_height: int):
    _, visited_set = perform_guard_walk(obstacle_positions, guard_start_position, guard_start_direction,
                                        grid_width, grid_height)
    print('Visited positions:', len(visited_set))
    return visited_set


def part_2(obstacle_positions: set, potential_obstacle_positions: [tuple], guard_start_position: tuple,
           guard_start_direction: Direction, grid_width: int, grid_height: int):
    # For each position on real guard's path, start a new search similar to Part 1, except add an obstacle at that
    # position. Run the search with each of those theoretical obstacles. If the (position, direction) at any point in
    # the search is in the visited_set, then it is a loop, so count it.
    valid_obstacle_positions = set()
    for potential_obstacle_position in potential_obstacle_positions:
        obstacle_positions.add(potential_obstacle_position)
        loop, visited_set = perform_guard_walk(obstacle_positions, guard_start_position, guard_start_direction,
                                               grid_width, grid_height)
        if loop:
            valid_obstacle_positions.add(potential_obstacle_position)
        obstacle_positions.remove(potential_obstacle_position)
    print('Valid obstacle positions:', len(valid_obstacle_positions))


if __name__ == '__main__':
    with (open('inputs/day_6.txt', 'r') as file):
        INPUT = file.read().split('\n')
    GRID_WIDTH = len(INPUT[0])
    GRID_HEIGHT = len(INPUT)

    obstacles = set()
    guard_start = None
    guard_direction = Direction.UP
    for y, row in enumerate(INPUT):
        if '^' in row:
            guard_start = (row.index('^'), y)
        for x, char in enumerate(row):
            if char == '#':
                obstacles.add((x, y))

    start_time = time.time()
    print('----- PART 1 -----')
    visited = part_1(obstacles, guard_start, guard_direction, GRID_WIDTH, GRID_HEIGHT)
    print('\nExecution time:', time.time() - start_time)

    start_time = time.time()
    print('\n----- PART 2 -----')
    part_2(obstacles, visited, guard_start, guard_direction, GRID_WIDTH, GRID_HEIGHT)
    print('\nExecution time:', time.time() - start_time)
