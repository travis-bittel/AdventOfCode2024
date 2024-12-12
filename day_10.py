import time

from util.grid_utils import Grid


def part_1(grid: Grid, trailhead_positions: [(int, int)]):
    total_score = 0
    for trailhead in trailhead_positions:
        reachable_peaks = set()
        to_explore = set()
        to_explore.add(trailhead)
        while to_explore:
            current_position = to_explore.pop()
            current_height = grid.get(*current_position)
            for adjacent_position in grid.adjacent_positions(*current_position):
                adjacent_height = grid.get(*adjacent_position)
                if adjacent_height == current_height + 1:
                    if adjacent_height == 9:
                        reachable_peaks.add(adjacent_position)
                    else:
                        to_explore.add(adjacent_position)
        total_score += len(reachable_peaks)
    print(total_score)


def part_2(grid: Grid, trailhead_positions: [(int, int)]):
    total_valid_trails = 0
    for trailhead in trailhead_positions:
        to_explore = [trailhead]
        while to_explore:
            current_position = to_explore.pop()
            current_height = grid.get(*current_position)
            for adjacent_position in grid.adjacent_positions(*current_position):
                adjacent_height = grid.get(*adjacent_position)
                if adjacent_height == current_height + 1:
                    if adjacent_height == 9:
                        total_valid_trails += 1
                    else:
                        to_explore.append(adjacent_position)
    print(total_valid_trails)


if __name__ == '__main__':
    GRID = Grid.from_file('inputs/day_10.txt', transform=int)

    TRAILHEAD_POSITIONS = []
    for position in GRID.all_positions():
        if GRID.get(*position) == 0:
            TRAILHEAD_POSITIONS.append(position)
    print(TRAILHEAD_POSITIONS)
    start_time = time.time()
    print('----- PART 1 -----')
    part_1(GRID, TRAILHEAD_POSITIONS)
    print('\nExecution time:', time.time() - start_time)

    start_time = time.time()
    print('\n----- PART 2 -----')
    part_2(GRID, TRAILHEAD_POSITIONS)
    print('\nExecution time:', time.time() - start_time)
