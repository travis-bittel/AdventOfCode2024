import math
import re
import time
from collections import defaultdict

from util.grid_utils import Vector2D


AREA_WIDTH = 101
AREA_HEIGHT = 103


def safety_factor(robot_positions: list[Vector2D]):
    quadrants = [0, 0, 0, 0]
    for robot in robot_positions:
        print(robot)
        if robot.x < 50:
            if robot.y < 51:
                quadrants[0] += 1
                print('0')
            elif robot.y > 51:
                quadrants[1] += 1
                print('1')
        elif robot.x > 50:
            if robot.y < 51:
                quadrants[2] += 1
                print('2')
            elif robot.y > 51:
                quadrants[3] += 1
                print('3')
    return math.prod(quadrants)


def part_1(robots: list[tuple[Vector2D, Vector2D]]):
    ITERATIONS = 100
    final_robot_positions = []
    for robot in robots:
        final_position = robot[0] + robot[1] * ITERATIONS
        final_position = Vector2D(final_position.x % AREA_WIDTH, final_position.y % AREA_HEIGHT)
        final_robot_positions.append(final_position)
    print(safety_factor(final_robot_positions))


def part_2(robots: list[tuple[Vector2D, Vector2D]]):
    # Write each iteration to a file
    with open(f'this-puzzle-sucks.txt', 'w') as file:
        for i in range(1000000):
            print(i)
            final_robot_positions = []
            for position in robots:
                final_position = position[0] + position[1] * i
                final_position = Vector2D(final_position.x % AREA_WIDTH, final_position.y % AREA_HEIGHT)
                final_robot_positions.append(final_position)
            file.write(f'Iteration {i}\n')
            file.write(get_robot_position_visual(final_robot_positions))
            file.write('\n\n\n')


def get_robot_position_visual(robot_positions: list[Vector2D]):
    grid = [['.' for _ in range(AREA_WIDTH)] for _ in range(AREA_HEIGHT)]
    for robot in robot_positions:
        grid[robot.y][robot.x] = '#'
    return ''.join([''.join(row) + '\n' for row in grid])


if __name__ == '__main__':
    with (open('inputs/day_14.txt', 'r') as file):
        INPUT = file.read().split('\n')

    pattern = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')
    ROBOTS = []
    for line in INPUT:
        match = pattern.findall(line)[0]
        ROBOTS.append((Vector2D(int(match[0]), int(match[1])), Vector2D(int(match[2]), int(match[3]))))

    start_time = time.time()
    print('----- PART 1 -----')
    part_1(ROBOTS)
    print('\nExecution time:', time.time() - start_time)

    print('\n----- PART 2 -----')
    part_2(ROBOTS)
    print('\nExecution time:', time.time() - start_time)
