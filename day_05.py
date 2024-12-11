import time


def update_is_valid(update: list, rules: list):
    value_to_index = {}
    for i, value in enumerate(update):
        value_to_index[value] = i

    for ordering_rule in rules:
        a, b = ordering_rule
        if a in value_to_index and b in value_to_index and value_to_index[a] > value_to_index[b]:
            return False
    return True


def part_1(ordering_rules: list, updates: list):
    total_page_numbers = sum(int(update[len(update) // 2]) for update in updates
                             if update_is_valid(update, ordering_rules))
    print(total_page_numbers)


def part_2(ordering_rules: list, updates: list):
    updates_with_incorrect_ordering = [update for update in updates
                                       if not update_is_valid(update, ordering_rules)]
    for update in updates_with_incorrect_ordering:
        current_index = 0
        while current_index < len(update):
            current_value = update[current_index]
            for rule in ordering_rules:
                if current_value == rule[0]:
                    try:
                        b_index = update.index(rule[1])
                    except ValueError:
                        continue
                    if current_index > b_index:
                        update[current_index] = rule[1]
                        update[b_index] = current_value
                        current_index = b_index - 1
                        break
            current_index += 1
    total_page_numbers = sum(int(update[len(update) // 2]) for update in updates_with_incorrect_ordering)
    print(total_page_numbers)


if __name__ == '__main__':
    ORDERING_RULES, UPDATES = open('inputs/day_5.txt').read().split('\n\n')
    UPDATES = [list(map(int, update.split(','))) for update in UPDATES.split('\n')]
    ORDERING_RULES = [tuple(map(int, rule.split('|'))) for rule in ORDERING_RULES.split('\n')]

    start_time = time.time()
    print('----- PART 1 -----')
    part_1(ORDERING_RULES, UPDATES)
    print('\nExecution time:', time.time() - start_time)

    start_time = time.time()
    print('\n----- PART 2 -----')
    part_2(ORDERING_RULES, UPDATES)
    print('\nExecution time:', time.time() - start_time)
