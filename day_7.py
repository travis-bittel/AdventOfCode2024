import time
from typing import Callable


def can_produce_expected_value(expected_value: int, start_value: int, equation_numbers: [int],
                               operators: [Callable[[int, int], int]]) -> bool:
    if not equation_numbers:
        return start_value == expected_value
    else:
        for operator in operators:
            if can_produce_expected_value(expected_value, operator(start_value, equation_numbers[0]),
                                          equation_numbers[1:], operators):
                return True
        return False


def sum_valid_equation_values(expected_values: [int], equation_numbers: [[int]],
                              operators: [Callable[[int, int], int]]) -> int:
    return sum([expected_value for expected_value, equation_numbers in zip(expected_values, equation_numbers)
                if can_produce_expected_value(expected_value, equation_numbers[0], equation_numbers[1:], operators)])


if __name__ == '__main__':
    with (open('inputs/day_7.txt', 'r') as file):
        INPUT = file.read()
    DESIRED_VALUES = []
    EQUATION_NUMBERS = []
    for line in INPUT.split('\n'):
        desired_value, numbers = line.split(':')
        DESIRED_VALUES.append(int(desired_value.strip()))
        EQUATION_NUMBERS.append([int(x) for x in numbers.split()])

    start_time = time.time()
    print('----- PART 1 -----')
    OPERATORS = [lambda a, b: a + b, lambda a, b: a * b]
    print(sum_valid_equation_values(DESIRED_VALUES, EQUATION_NUMBERS, OPERATORS))
    print('\nExecution time:', time.time() - start_time)

    start_time = time.time()
    print('\n----- PART 2 -----')
    OPERATORS = [lambda a, b: a + b, lambda a, b: a * b, lambda a, b: int(''.join([str(a), str(b)]), )]
    print(sum_valid_equation_values(DESIRED_VALUES, EQUATION_NUMBERS, OPERATORS))
    print('\nExecution time:', time.time() - start_time)
