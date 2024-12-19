import time


def number_of_possible_patterns(pattern_to_check: str, towel_patterns: [str], pattern_memo: dict) -> int:
    if pattern_to_check in pattern_memo:
        return pattern_memo[pattern_to_check]
    if len(pattern_to_check) == 0:
        pattern_memo[pattern_to_check] = 1
        return 1
    num = 0
    for pattern in towel_patterns:
        if pattern_to_check.startswith(pattern):
            num += number_of_possible_patterns(pattern_to_check[len(pattern):], towel_patterns, pattern_memo)
    pattern_memo[pattern_to_check] = num
    return num


def part_1(patterns_to_check: [str], towel_patterns: [str]):
    pattern_memo = {}
    valid_patterns = 0
    for pattern in patterns_to_check:
        if number_of_possible_patterns(pattern, towel_patterns, pattern_memo) > 0:
            valid_patterns += 1
    print(valid_patterns)


def part_2(patterns_to_check: [str], towel_patterns: [str]):
    pattern_memo = {}
    total = 0
    for pattern in patterns_to_check:
        total += number_of_possible_patterns(pattern, towel_patterns, pattern_memo)
    print(total)


if __name__ == '__main__':
    with (open('inputs/day_19.txt', 'r') as file):
        INPUT = file.read()
    TOWEL_PATTERNS, PATTERNS_TO_CHECK = INPUT.split('\n\n')
    TOWEL_PATTERNS = TOWEL_PATTERNS.split(', ')
    PATTERNS_TO_CHECK = PATTERNS_TO_CHECK.split('\n')
    start_time = time.time()
    print('----- PART 1 -----')
    part_1(PATTERNS_TO_CHECK, TOWEL_PATTERNS)
    print('\nExecution time:', time.time() - start_time)

    start_time = time.time()
    print('\n----- PART 2 -----')
    part_2(PATTERNS_TO_CHECK, TOWEL_PATTERNS)
    print('\nExecution time:', time.time() - start_time)
