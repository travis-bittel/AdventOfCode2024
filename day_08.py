import time
from itertools import combinations


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2D(self.x * other, self.y * other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


def position_is_on_grid(position: Vector2D, grid_width: int, grid_height: int):
    return 0 <= position.x < grid_width and 0 <= position.y < grid_height


def part_1(antenna_positions: dict[str, list[Vector2D]], grid_width: int, grid_height: int):
    antinodes = []
    for antenna, positions in antenna_positions.items():
        antenna_pairs = combinations(positions, 2)
        for pair in antenna_pairs:
            vector = pair[1] - pair[0]
            antinodes.append(pair[0] - vector)
            antinodes.append(pair[1] + vector)
    print(len(set([antinode for antinode in antinodes if position_is_on_grid(antinode, grid_width, grid_height)])))


def part_2(antenna_positions: dict[str, list[Vector2D]], grid_width: int, grid_height: int):
    antinodes = []
    for antenna, positions in antenna_positions.items():
        antenna_pairs = combinations(positions, 2)
        for pair in antenna_pairs:
            vector = pair[1] - pair[0]
            i = 0
            while position_is_on_grid(pair[0] - vector * i, grid_width, grid_height):
                antinodes.append(pair[0] - vector * i)
                i += 1
            i = 0
            while position_is_on_grid(pair[1] + vector * i, grid_width, grid_height):
                antinodes.append(pair[1] + vector * i)
                i += 1
    print(len(set([antinode for antinode in antinodes if position_is_on_grid(antinode, grid_width, grid_height)])))


if __name__ == '__main__':
    with (open('inputs/day_8.txt', 'r') as file):
        INPUT = file.read().split('\n')
    GRID_WIDTH = len(INPUT[0])
    GRID_HEIGHT = len(INPUT)

    GRID = [list(row) for row in INPUT]

    ANTENNA_POSITIONS = {}
    for y, row in enumerate(GRID):
        for x, cell in enumerate(row):
            if cell != '.':
                if cell in ANTENNA_POSITIONS:
                    ANTENNA_POSITIONS[cell].append(Vector2D(x, y))
                else:
                    ANTENNA_POSITIONS[cell] = [Vector2D(x, y)]

    start_time = time.time()
    print('----- PART 1 -----')
    part_1(ANTENNA_POSITIONS, GRID_WIDTH, GRID_HEIGHT)
    print('\nExecution time:', time.time() - start_time)

    start_time = time.time()
    print('\n----- PART 2 -----')
    part_2(ANTENNA_POSITIONS, GRID_WIDTH, GRID_HEIGHT)
    print('\nExecution time:', time.time() - start_time)
