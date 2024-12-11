import time


def position_is_on_grid(position: (int, int), grid_width: int, grid_height: int):
    return 0 <= position[0] < grid_width and 0 <= position[1] < grid_height


def adjacent_cells(x: int, y: int) -> [(int, int)]:
    return [position for position in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            if position_is_on_grid(position, GRID_WIDTH, GRID_HEIGHT)]


def part_1(grid: [[int]], trailhead_positions: [(int, int)]):
    total_score = 0
    for trailhead in trailhead_positions:
        reachable_peaks = set()
        to_explore = set()
        to_explore.add(trailhead)
        while to_explore:
            current_position = to_explore.pop()
            current_height = grid[current_position[1]][current_position[0]]
            for adjacent_position in adjacent_cells(current_position[0], current_position[1]):
                adjacent_height = grid[adjacent_position[1]][adjacent_position[0]]
                if adjacent_height == current_height + 1:
                    if adjacent_height == 9:
                        reachable_peaks.add(adjacent_position)
                    else:
                        to_explore.add(adjacent_position)
        total_score += len(reachable_peaks)
    print(total_score)


def part_2(grid: [[int]], trailhead_positions: [(int, int)]):
    total_valid_trails = 0
    for trailhead in trailhead_positions:
        to_explore = [trailhead]
        while to_explore:
            current_position = to_explore.pop()
            current_height = grid[current_position[1]][current_position[0]]
            for adjacent_position in adjacent_cells(current_position[0], current_position[1]):
                adjacent_height = grid[adjacent_position[1]][adjacent_position[0]]
                if adjacent_height == current_height + 1:
                    if adjacent_height == 9:
                        total_valid_trails += 1
                    else:
                        to_explore.append(adjacent_position)
    print(total_valid_trails)


if __name__ == '__main__':
    with (open('inputs/day_10.txt', 'r') as file):
        INPUT = file.read().split('\n')
    GRID_WIDTH = len(INPUT[0])
    GRID_HEIGHT = len(INPUT)
    GRID = [list(map(int, list(row))) for row in INPUT]

    TRAILHEAD_POSITIONS = []
    for y, row in enumerate(GRID):
        for x, cell in enumerate(row):
            if cell == 0:
                TRAILHEAD_POSITIONS.append((x, y))

    start_time = time.time()
    print('----- PART 1 -----')
    part_1(GRID, TRAILHEAD_POSITIONS)
    print('\nExecution time:', time.time() - start_time)

    start_time = time.time()
    print('\n----- PART 2 -----')
    part_2(GRID, TRAILHEAD_POSITIONS)
    print('\nExecution time:', time.time() - start_time)
