import time
from collections import defaultdict
from itertools import combinations

from util.grid_utils import Vector2D, Grid


def part_1(grid: Grid, antenna_positions: dict[str, list[Vector2D]]):
    antinodes = []
    for antenna, positions in antenna_positions.items():
        antenna_pairs = combinations(positions, 2)
        for pair in antenna_pairs:
            vector = pair[1] - pair[0]
            antinodes.append(pair[0] - vector)
            antinodes.append(pair[1] + vector)
    print(len(set([antinode for antinode in antinodes if grid.position_is_on_grid(*antinode)])))


def part_2(grid: Grid, antenna_positions: dict[str, list[Vector2D]]):
    antinodes = []
    for antenna, positions in antenna_positions.items():
        antenna_pairs = combinations(positions, 2)
        for pair in antenna_pairs:
            vector = pair[1] - pair[0]
            i = 0
            while grid.position_is_on_grid(*(pair[0] - vector * i)):
                antinodes.append(pair[0] - vector * i)
                i += 1
            i = 0
            while grid.position_is_on_grid(*(pair[1] + vector * i)):
                antinodes.append(pair[1] + vector * i)
                i += 1
    print(len(set([antinode for antinode in antinodes if grid.position_is_on_grid(*antinode)])))


if __name__ == '__main__':
    GRID = Grid.from_file('inputs/day_8.txt')

    ANTENNA_POSITIONS = defaultdict(list)
    for position in GRID.all_positions():
        if GRID.get(*position) != '.':
            ANTENNA_POSITIONS[GRID.get(*position)].append(position)

    start_time = time.time()
    print('----- PART 1 -----')
    part_1(GRID, ANTENNA_POSITIONS)
    print('\nExecution time:', time.time() - start_time)

    start_time = time.time()
    print('\n----- PART 2 -----')
    part_2(GRID, ANTENNA_POSITIONS)
    print('\nExecution time:', time.time() - start_time)
