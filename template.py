import time


def part_1(puzzle_input: str):
    pass


def part_2(puzzle_input: str):
    pass


if __name__ == '__main__':
    with (open('inputs/day_<day number here>.txt', 'r') as file):
        INPUT = file.read()
    start_time = time.time()
    print('----- PART 1 -----')
    part_1(INPUT)
    print('\nExecution time:', time.time() - start_time)

    print('\n----- PART 2 -----')
    part_2(INPUT)
    print('\nExecution time:', time.time() - start_time)
