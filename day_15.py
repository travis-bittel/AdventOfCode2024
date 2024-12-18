import time
from copy import deepcopy

from util.grid_utils import Grid, Vector2D


def can_push_obstacles(grid: Grid, new_position: Vector2D, direction: Vector2D) -> (bool, Vector2D):
    i = 0
    while True:
        position_to_check = new_position + direction * i
        if grid.get(*position_to_check) == 'O':
            i += 1
            continue
        if grid.get(*position_to_check) == '.':
            return True, position_to_check
        if grid.get(*position_to_check) == '#':
            return False, None


def push_box(grid: Grid, box_halves: (Vector2D, Vector2D), direction: Vector2D) -> bool:
    new_box_positions = [box_halves[0] + direction, box_halves[1] + direction]

    if direction == Vector2D(0, -1) or direction == Vector2D(0, 1):
        positions_to_check = new_box_positions
    elif direction == Vector2D(-1, 0):
        positions_to_check = [new_box_positions[0]]
    else:
        positions_to_check = [new_box_positions[1]]
    if all([grid.get(*position) == '.' for position in positions_to_check]):
        grid.put(*box_halves[0], '.')
        grid.put(*box_halves[1], '.')
        grid.put(*new_box_positions[0], '[')
        grid.put(*new_box_positions[1], ']')
    elif any([grid.get(*position) == '#' for position in positions_to_check]):
        return False
    else:
        for position in positions_to_check:
            if grid.get(*position) == '[':
                next_box_positions = (position, position + Vector2D(1, 0))
                break
            elif grid.get(*position) == ']':
                next_box_positions = (position + Vector2D(-1, 0), position)
                break
        if push_box(grid, next_box_positions, direction):
            grid.put(*box_halves[0], '.')
            grid.put(*box_halves[1], '.')
            grid.put(*new_box_positions[0], '[')
            grid.put(*new_box_positions[1], ']')
        else:
            return False
    return True


def move_guard(grid: Grid, current_position: Vector2D, direction: Vector2D) -> Vector2D:
    new_position = current_position + direction
    new_cell = grid.get(*new_position)
    if new_cell == '#':
        return current_position
    elif new_cell == '.':
        grid.put(*current_position, '.')
        grid.put(*new_position, '@')
    elif new_cell == 'O' or new_cell == '[' or new_cell == ']':
        if new_cell == 'O':
            can_push, new_obstacle_position = can_push_obstacles(grid, new_position, direction)
            if can_push:
                grid.put(*current_position, '.')
                grid.put(*new_position, '@')
                grid.put(*new_obstacle_position, 'O')
            else:
                return current_position
        else:
            if new_cell == '[':
                box_halves = (new_position, new_position + Vector2D(1, 0))
            else:
                box_halves = (new_position + Vector2D(-1, 0), new_position)
            if push_box(grid, box_halves, direction):
                grid.put(*current_position, '.')
                grid.put(*new_position, '@')
            else:
                return current_position
    return new_position


def part_1(grid: Grid, guard_start_position: Vector2D, moves: [Vector2D]):
    guard_position = guard_start_position
    for move in moves:
        guard_position = move_guard(grid, guard_position, move)
    print(grid)
    print(sum([box_position.x + box_position.y * 100 for box_position in grid.find_all('O')]))


def part_2(grid: Grid, guard_start_position: Vector2D, moves: [Vector2D]):
    # < 1529886
    # > 1522058
    left_halves = grid.find_all('[')
    box_positions = [(left_half, left_half + Vector2D(1, 0)) for left_half in left_halves]
    walls = grid.find_all('#')
    guard_position = guard_start_position
    for i, move in enumerate(moves):
        print(f'Move {i}: {move}')
        guard_position, box_positions = move_guard_new(box_positions, walls, guard_position, move)
        #debug_print_grid(box_positions, guard_position)

    debug_print_grid(box_positions, guard_position)

    print(sum([left_half.x + left_half.y * 100 for left_half, right_half in box_positions]))


def debug_mode(grid: Grid, guard_start_position: Vector2D, moves: [Vector2D]):
    left_halves = grid.find_all('[')
    box_positions = [(left_half, left_half + Vector2D(1, 0)) for left_half in left_halves]
    walls = grid.find_all('#')
    guard_position = guard_start_position
    while True:
        debug_print_grid(box_positions, guard_position)
        move = arrow_to_direction(input('Enter move: '))
        guard_position = move_guard_new(box_positions, walls, guard_position, move)


def debug_print_grid(box_positions: [(Vector2D, Vector2D)], guard_position: Vector2D):
    with (open('inputs/day_15.txt', 'r') as file):
        input = file.read()
    input = input.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')
    grid = Grid.from_text(input.split('\n\n')[0])
    for position in grid.all_positions():
        if grid.get(*position) != '#':
            grid.put(*position, '.')
    grid.put(*guard_position, '@')
    for box_position in box_positions:
        try:
            grid.put(*box_position[0], '[')
            grid.put(*box_position[1], ']')
        except:
            pass
    print(grid)


def move_guard_new(box_positions: [(Vector2D, Vector2D)], walls: [Vector2D],
                   current_position: Vector2D, direction: Vector2D) -> (Vector2D, [Vector2D]):
    new_position = current_position + direction
    if new_position in walls:
        return current_position, box_positions
    for box_position in box_positions:
        if new_position in box_position:
            snapshot = deepcopy(box_positions)
            success = move_box_new(box_positions, walls, box_position, direction)
            if success:
                return new_position, box_positions
            else:
                return current_position, snapshot
    return new_position, box_positions


def move_box_new(box_positions: [(Vector2D, Vector2D)], walls: [Vector2D],
                 box_to_move: (Vector2D, Vector2D), direction: Vector2D) -> bool:
    new_box_locations = [box_to_move[0] + direction, box_to_move[1] + direction]
    if any([location in walls for location in new_box_locations]):
        return False
    for location in new_box_locations:
        for box_position in box_positions:
            if box_position != box_to_move:
                if location in box_position:
                    if not move_box_new(box_positions, walls, box_position, direction):
                        return False
    box_positions.remove(box_to_move)
    box_positions.append(new_box_locations)
    return True


def arrow_to_direction(arrow: str) -> Vector2D:
    if arrow == '^':
        return Vector2D(0, -1)
    elif arrow == 'v':
        return Vector2D(0, 1)
    elif arrow == '<':
        return Vector2D(-1, 0)
    elif arrow == '>':
        return Vector2D(1, 0)


def process_input(puzzle_input: str) -> (Grid, Vector2D, [Vector2D]):
    grid, moves = puzzle_input.split('\n\n')
    grid = Grid.from_text(grid)
    moves = [arrow_to_direction(move) for move in moves.replace('\n', '')]
    guard_start_position = grid.find('@')
    return grid, guard_start_position, moves


if __name__ == '__main__':
    with (open('inputs/day_15.txt', 'r') as file):
        INPUT = file.read()

    start_time = time.time()
    print('----- PART 1 -----')
    part_1(*process_input(INPUT))
    print('\nExecution time:', time.time() - start_time)

    INPUT = INPUT.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')

    start_time = time.time()
    print('\n----- PART 2 -----')
    #debug_mode(*process_input(INPUT))
    part_2(*process_input(INPUT))
    print('\nExecution time:', time.time() - start_time)
