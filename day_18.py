import time

from util.grid_utils import Grid, Vector2D


def part_1(grid: Grid, falling_byte_coords: list[Vector2D]):
    for i in range(1024):
        grid.put(*falling_byte_coords[i], '#')
    print(grid)
    start = Vector2D(0, 0)
    end = Vector2D(70, 70)

    queue = [(start, 0)]
    visited = set()
    while queue:
        position, steps_from_start = queue.pop(0)
        if position in visited:
            continue
        if position == end:
            print(steps_from_start)
            break
        visited.add(position)
        for adjacent in grid.adjacent_positions(*position):
            if adjacent not in visited and grid.get(*adjacent) != '#':
                queue.append((adjacent, steps_from_start + 1))


def part_2(grid: Grid, falling_byte_coords: list[Vector2D]):
    for i in range(1024):
        grid.put(*falling_byte_coords[i], '#')
    start = Vector2D(0, 0)
    end = Vector2D(70, 70)

    for i in range(1024, len(falling_byte_coords)):
        print(f'Iteration {i}')
        grid.put(*falling_byte_coords[i], '#')
        queue = [(start, 0)]
        visited = set()
        while queue:
            position, steps_from_start = queue.pop(0)
            if position in visited:
                continue
            if position == end:
                print(steps_from_start)
                break
            visited.add(position)
            for adjacent in grid.adjacent_positions(*position):
                if adjacent not in visited and grid.get(*adjacent) != '#':
                    queue.append((adjacent, steps_from_start + 1))


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
