import time


def part_1(puzzle_input: str):
    a, b = zip(*[map(int, line.split()) for line in puzzle_input.strip().split('\n')])
    a = sorted(a)
    b = sorted(b)
    print(sum(abs(x - y) for x, y in zip(a, b)))


def part_2(puzzle_input: str):
    a, b = zip(*[map(int, line.split()) for line in puzzle_input.strip().split('\n')])
    b = {x: b.count(x) for x in b}
    print(sum(x * b.get(x, 0) for x in a))


if __name__ == '__main__':
    with (open('inputs/day_1.txt', 'r') as file):
        INPUT = file.read()

    start_time = time.time()
    print('----- PART 1 -----')
    part_1(INPUT)
    print('\nExecution time:', time.time() - start_time)

    start_time = time.time()
    print('\n----- PART 2 -----')
    part_2(INPUT)
    print('\nExecution time:', time.time() - start_time)
