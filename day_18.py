import time
from typing import Optional

from util.grid_utils import Grid, Vector2D


def length_of_shortest_path(grid: Grid, start: Vector2D, end: Vector2D) -> Optional[int]:
    queue = [(start, 0)]
    visited = set()
    while queue:
        position, steps_from_start = queue.pop(0)
        if position in visited:
            continue
        if position == end:
            return steps_from_start
        visited.add(position)
        for adjacent in grid.adjacent_positions(*position):
            if adjacent not in visited and grid.get(*adjacent) != '#':
                queue.append((adjacent, steps_from_start + 1))


def part_1(grid: Grid, falling_byte_coords: list[Vector2D]):
    for i in range(1024):
        grid.put(*falling_byte_coords[i], '#')
    start = Vector2D(0, 0)
    end = Vector2D(70, 70)
    print(length_of_shortest_path(grid, start, end))


def part_2(grid: Grid, falling_byte_coords: list[Vector2D]):
    for i in range(1024):
        grid.put(*falling_byte_coords[i], '#')
    start = Vector2D(0, 0)
    end = Vector2D(70, 70)

    low = 1024
    high = len(falling_byte_coords)
    while low < high:
        mid = (low + high) // 2
        grid = Grid([['.' for _ in range(71)] for _ in range(71)])
        for i in range(mid):
            grid.put(*falling_byte_coords[i], '#')

        if not length_of_shortest_path(grid, start, end):
            high = mid
        else:
            low = mid + 1
    print(falling_byte_coords[low - 1])


if __name__ == '__main__':
    with (open('inputs/day_18.txt', 'r') as file):
        INPUT = file.read()
    FALLING_BYTE_COORDS = [Vector2D(*map(int, coord.split(','))) for coord in INPUT.split('\n')]
    GRID = Grid([['.' for _ in range(71)] for _ in range(71)])
    start_time = time.time()
    print('----- PART 1 -----')
    part_1(GRID, FALLING_BYTE_COORDS)
    print('\nExecution time:', time.time() - start_time)

    print('\n----- PART 2 -----')
    part_2(GRID, FALLING_BYTE_COORDS)
    print('\nExecution time:', time.time() - start_time)
