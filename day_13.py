import re
import sys
import time
from dataclasses import dataclass
from typing import Optional

from util.grid_utils import Vector2D


@dataclass
class Machine:
    buttons: list[Vector2D]
    prize: Vector2D


def part_1(machines: list[Machine]):
    print(sum(cost for machine in machines if (cost := minimum_token_cost(machine)) is not None))


def part_2(machines: list[Machine]):
    IMPRESSIVELY_BAD_ERROR_IN_MEASUREMENTS = 10000000000000
    for machine in machines:
        machine.prize = Vector2D(machine.prize.x + IMPRESSIVELY_BAD_ERROR_IN_MEASUREMENTS,
                                 machine.prize.y + IMPRESSIVELY_BAD_ERROR_IN_MEASUREMENTS)
    print(sum(cost for machine in machines if (cost := minimum_token_cost(machine)) is not None))
    pass


def minimum_token_cost(machine: Machine) -> Optional[int]:
    Py = machine.prize.y
    Px = machine.prize.x
    X1 = machine.buttons[0].x
    Y1 = machine.buttons[0].y
    X2 = machine.buttons[1].x
    Y2 = machine.buttons[1].y
    A = int((Px * Y2 - X2 * Py) / (X1 * Y2 - X2 * Y1))
    B = int((Py * X1 - Px * Y1) / (Y2 * X1 - X2 * Y1))
    if machine.buttons[0] * A + machine.buttons[1] * B != machine.prize:
        return None
    return int(3 * A + B)


if __name__ == '__main__':
    with (open('inputs/day_13.txt', 'r') as file):
        INPUT = file.read().split('\n\n')

    MACHINES = []
    equation_pattern = re.compile(r'X\+(\d+), Y\+(\d+)')
    prize_pattern = re.compile(r'X=(\d+), Y=(\d+)')
    for MACHINE in INPUT:
        a, b, PRIZE = MACHINE.split('\n')
        EQUATIONS = [equation_pattern.findall(a)[0], equation_pattern.findall(b)[0]]
        PRIZE = prize_pattern.findall(PRIZE)[0]
        MACHINES.append(Machine([Vector2D(*map(int, equation)) for equation in EQUATIONS], Vector2D(*map(int, PRIZE))))

    start_time = time.time()
    print('----- PART 1 -----')
    part_1(MACHINES)
    print('\nExecution time:', time.time() - start_time)

    print('\n----- PART 2 -----')
    part_2(MACHINES)
    print('\nExecution time:', time.time() - start_time)
