import heapq
import time
from collections import defaultdict

from util.grid_utils import Grid, Vector2D, Direction


def shortest_paths(grid: Grid, start: Vector2D, end: Vector2D) -> list[tuple[list[Vector2D, Direction], int]]:
    to_explore = []
    heapq.heappush(to_explore, (0, (start, Direction.RIGHT), []))

    lowest_cost_to_state = defaultdict(lambda: float('inf'))
    lowest_cost_to_state[(start, Direction.RIGHT)] = 0

    lowest_cost_paths = []
    while to_explore:
        current_cost, current_state, current_path = heapq.heappop(to_explore)
        current_position, current_direction = current_state

        current_path = current_path + [(current_position, current_direction)]

        if current_position == end:
            lowest_cost_paths.append((current_path, current_cost))

        movement_options = [
            (current_direction, 0),
            (current_direction.turn_90_degrees(), 1000),
            (current_direction.turn_90_degrees().turn_90_degrees(), 2000),
            (current_direction.turn_90_degrees().turn_90_degrees().turn_90_degrees(), 1000)
        ]

        for movement_option in movement_options:
            new_direction, new_cost = movement_option
            new_position = current_position + new_direction.value
            if grid.get(*new_position) == '#':
                continue
            new_state = (new_position, new_direction)
            cost_to_new_state = current_cost + new_cost + 1
            if cost_to_new_state <= lowest_cost_to_state[new_state]:
                lowest_cost_to_state[new_state] = cost_to_new_state
                heapq.heappush(to_explore, (cost_to_new_state, new_state, current_path))
    # We can sometimes get paths which are not actually tied for shortest and the simplest fix is just to filter them
    minimum_cost = min(lowest_cost_paths, key=lambda x: x[1])[1]
    lowest_cost_paths = [(path, cost) for path, cost in lowest_cost_paths if cost == minimum_cost]
    return lowest_cost_paths


def part_1(grid: Grid, start: Vector2D, end: Vector2D):
    paths = shortest_paths(grid, start, end)
    states, cost = paths[0]
    print(cost)


def part_2(grid: Grid, start: Vector2D, end: Vector2D):
    paths = [path for path, cost in shortest_paths(grid, start, end)]
    tiles_visited_by_shortest_paths = set()
    for path in paths:
        for state in path:
            position = state[0]
            tiles_visited_by_shortest_paths.add(position)
    print(debug_output(grid, paths))
    print(len(tiles_visited_by_shortest_paths))


def debug_output(grid: Grid, paths: list[tuple[list[Vector2D, Direction], int]]):
    for path in paths:
        for state in path:
            position = state[0]
            grid.put(*position, 'O')
    return repr(grid)


if __name__ == '__main__':
    GRID = Grid.from_file('inputs/day_16.txt')
    START = GRID.find('S')
    END = GRID.find('E')

    start_time = time.time()
    print('----- PART 1 -----')
    part_1(GRID, START, END)
    print('\nExecution time:', time.time() - start_time)

    start_time = time.time()
    print('\n----- PART 2 -----')
    part_2(GRID, START, END)
    print('\nExecution time:', time.time() - start_time)
