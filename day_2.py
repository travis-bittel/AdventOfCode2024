import time


def report_is_safe(report: [int]) -> bool:
    increasing = report[1] - report[0] > 0
    for i in range(1, len(report)):
        if (report[i] - report[i - 1] > 0) != increasing \
                or abs(report[i] - report[i - 1]) > 3 \
                or report[i] - report[i - 1] == 0:
            return False
    return True


def report_is_safe_with_dampener(report: [int]) -> bool:
    # Check if the report is safe with all entries or with one entry removed
    if report_is_safe(report):
        return True
    for i in range(0, len(report)):
        if report_is_safe(report[:i] + report[i + 1:]):
            return True
    return False


def part_1(reports: list):
    safe_reports = len([report for report in reports if report_is_safe(report)])
    print(f'Safe reports: {safe_reports}')


def part_2(reports: list):
    safe_reports = len([report for report in reports if report_is_safe_with_dampener(report)])
    print(f'Safe reports: {safe_reports}')


if __name__ == '__main__':
    with (open('inputs/day_2.txt', 'r') as file):
        INPUT = file.read()
    REPORTS = [[int(num) for num in line.split()] for line in INPUT.strip().split('\n')]

    start_time = time.time()
    print('----- PART 1 -----')
    part_1(REPORTS)
    print('\nExecution time:', time.time() - start_time)

    start_time = time.time()
    print('\n----- PART 2 -----')
    part_2(REPORTS)
    print('\nExecution time:', time.time() - start_time)
