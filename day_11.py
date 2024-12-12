import math
import time
from collections import defaultdict


def digits(value: int) -> int:
    return int(math.log10(value)) + 1


def change_stone(stone: int) -> [int]:
    if stone == 0:
        return [1]
    elif digits(stone) >= 2 and digits(stone) % 2 == 0:
        stone_str = str(stone)
        half_length = len(stone_str) // 2
        left_half = int(stone_str[:half_length])
        right_half = int(stone_str[half_length:])
        return [int(left_half), int(right_half)]
    else:
        return [stone * 2024]


def blink(stones: defaultdict) -> defaultdict:
    new_stones = defaultdict(int)
    for stone in stones.keys():
        new_stone_values = change_stone(stone)
        for new_stone in new_stone_values:
            new_stones[new_stone] += stones[stone]
    return new_stones


def part_1(stone_counts: defaultdict):
    for _ in range(25):
        stone_counts = blink(stone_counts)
    print(sum(stone_counts.values()))


def part_2(stone_counts: defaultdict):
    for i in range(75):
        start = time.time()
        stone_counts = blink(stone_counts)
    print(sum(stone_counts.values()))


if __name__ == '__main__':
    with (open('inputs/day_11.txt', 'r') as file):
        INPUT = file.read()
    STONES = list(map(int, INPUT.split()))
    STONE_COUNTS = defaultdict(int)
    for STONE in STONES:
        STONE_COUNTS[STONE] += 1

    start_time = time.time()
    print('----- PART 1 -----')
    part_1(STONE_COUNTS)
    print('\nExecution time:', time.time() - start_time)

    start_time = time.time()
    print('\n----- PART 2 -----')
    part_2(STONE_COUNTS)
    print('\nExecution time:', time.time() - start_time)
