import time


def input_as_2d_array(puzzle_input: str) -> list:
    return [list(row) for row in puzzle_input.split()]


def part_1(puzzle_input: str):
    input_array = input_as_2d_array(puzzle_input)
    number_of_xmas = 0

    puzzle_width = len(input_array[0])
    puzzle_height = len(input_array)

    # Left to right
    for y in range(puzzle_height):
        row = input_array[y]
        for x in range(puzzle_width):
            if x + 3 < len(row) and row[x:x + 4] == ['X', 'M', 'A', 'S']:
                number_of_xmas += 1

    # Right to left
    for y in range(puzzle_height):
        row = input_array[y]
        for x in range(puzzle_width):
            if x - 3 >= 0 and row[x - 4:x] == ['S', 'A', 'M', 'X']:
                number_of_xmas += 1

    # Top to bottom
    for y in range(puzzle_height):
        for x in range(puzzle_width):
            if y + 3 < puzzle_height and input_array[y][x] == 'X' \
                    and input_array[y + 1][x] == 'M' \
                    and input_array[y + 2][x] == 'A' \
                    and input_array[y + 3][x] == 'S':
                number_of_xmas += 1

    # Bottom to top
    for y in range(puzzle_height):
        for x in range(puzzle_width):
            if y - 3 >= 0 and input_array[y][x] == 'X' \
                    and input_array[y - 1][x] == 'M' \
                    and input_array[y - 2][x] == 'A' \
                    and input_array[y - 3][x] == 'S':
                number_of_xmas += 1

    # Diagonal top left to bottom right
    for y in range(puzzle_height):
        for x in range(puzzle_width):
            if y + 3 < puzzle_height and x + 3 < puzzle_width and input_array[y][x] == 'X' \
                    and input_array[y + 1][x + 1] == 'M' \
                    and input_array[y + 2][x + 2] == 'A' \
                    and input_array[y + 3][x + 3] == 'S':
                number_of_xmas += 1

    # Diagonal bottom right to top left
    for y in range(puzzle_height):
        for x in range(puzzle_width):
            if y - 3 >= 0 and x - 3 >= 0 and input_array[y][x] == 'X' \
                    and input_array[y - 1][x - 1] == 'M' \
                    and input_array[y - 2][x - 2] == 'A' \
                    and input_array[y - 3][x - 3] == 'S':
                number_of_xmas += 1

    # Diagonal top right to bottom left
    for y in range(puzzle_height):
        for x in range(puzzle_width):
            if y + 3 < puzzle_height and x - 3 >= 0 and input_array[y][x] == 'X' \
                    and input_array[y + 1][x - 1] == 'M' \
                    and input_array[y + 2][x - 2] == 'A' \
                    and input_array[y + 3][x - 3] == 'S':
                number_of_xmas += 1

    # Diagonal bottom left to top right
    for y in range(puzzle_height):
        for x in range(puzzle_width):
            if y - 3 >= 0 and x + 3 < puzzle_width and input_array[y][x] == 'X' \
                    and input_array[y - 1][x + 1] == 'M' \
                    and input_array[y - 2][x + 2] == 'A' \
                    and input_array[y - 3][x + 3] == 'S':
                number_of_xmas += 1

    print(number_of_xmas)


def part_2(puzzle_input: str):
    input_array = input_as_2d_array(puzzle_input)
    number_of_xmas = 0

    puzzle_width = len(input_array[0])
    puzzle_height = len(input_array)
    # For each 3x3 section of the puzzle
    for y in range(puzzle_height - 2):
        for x in range(puzzle_width - 2):
            # Must have A in the middle
            if input_array[y + 1][x + 1] == 'A':
                # Top left to bottom right and bottom left to top right are both MAS or SAM
                if (input_array[y][x] == 'M' and input_array[y + 2][x + 2] == 'S'
                    or input_array[y][x] == 'S' and input_array[y + 2][x + 2] == 'M')\
                        and (input_array[y][x + 2] == 'M' and input_array[y + 2][x] == 'S'
                             or input_array[y][x + 2] == 'S' and input_array[y + 2][x] == 'M'):
                    number_of_xmas += 1
    print(number_of_xmas)


if __name__ == '__main__':
    with (open('inputs/day_4.txt', 'r') as file):
        INPUT = file.read()

    start_time = time.time()
    print('----- PART 1 -----')
    part_1(INPUT)
    print('\nExecution time:', time.time() - start_time)

    start_time = time.time()
    print('\n----- PART 2 -----')
    part_2(INPUT)
    print('\nExecution time:', time.time() - start_time)
