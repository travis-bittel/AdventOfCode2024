import re
import time


def sum_all_mul_command_results(text: str) -> int:
    pattern = r'mul\(\d+,\d+\)'
    matches = re.findall(pattern, text)
    numbers = [list(map(int, re.findall(r'\d+', match))) for match in matches]
    return sum([a * b for a, b in numbers])


def part_1(puzzle_input: str):
    result = sum_all_mul_command_results(puzzle_input)
    print(result)


def part_2(puzzle_input: str):
    # Use regex to split string by "do()" OR "don't()", including the separators in the output
    segments = re.split(r'(do\(\)|don\'t\(\))', puzzle_input)

    result = 0
    include_statements = True
    for segment in segments:
        if segment == 'do()':
            include_statements = True
        elif segment == 'don\'t()':
            include_statements = False
        elif include_statements:
            result += sum_all_mul_command_results(segment)
    print(result)


if __name__ == '__main__':
    with (open('inputs/day_3.txt', 'r') as file):
        INPUT = file.read()

    start_time = time.time()
    print('----- PART 1 -----')
    part_1(INPUT)
    print('\nExecution time:', time.time() - start_time)

    start_time = time.time()
    print('\n----- PART 2 -----')
    part_2(INPUT)
    print('\nExecution time:', time.time() - start_time)
