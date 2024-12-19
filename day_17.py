import math
import re
import sys
import time
from typing import Optional

A = 0
B = 1
C = 2


def dv(operand: int, registers: list[int], storage_register: int):
    combo_operand = to_combo_operand(operand, registers)
    if combo_operand > math.log2(sys.maxsize):
        registers[storage_register] = 0
    else:
        registers[storage_register] = registers[A] // int(math.pow(2, combo_operand))


def to_combo_operand(operand: int, registers: list[int]) -> int:
    if operand < 4:
        return operand
    else:
        return registers[operand - 4]


def adv(registers: list[int], operand: int):
    dv(operand, registers, A)


def bxl(registers: list[int], operand: int):
    registers[B] ^= operand


def bst(registers: list[int], operand: int):
    registers[B] = to_combo_operand(operand, registers) % 8


# Special case this one because I'm lazy...
def jnz(registers: list[int], operand: int) -> Optional[int]:
    if registers[A] != 0:
        return operand
    return None


def bxc(registers: list[int], operand: int):
    registers[B] ^= registers[C]


def out(registers: list[int], operand: int) -> str:
    return str(to_combo_operand(operand, registers) % 8)


def bdv(registers: list[int], operand: int):
    dv(operand, registers, B)


def cdv(registers: list[int], operand: int):
    dv(operand, registers, C)


OPCODES = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv
}


def run_program(registers: list[int], program: list[int]):
    instruction_pointer = 0
    output = ''
    while instruction_pointer < len(program):
        opcode = program[instruction_pointer]
        operand = program[instruction_pointer + 1]
        operation = OPCODES[opcode]
        if operation == jnz:
            result = operation(registers, operand)
            instruction_pointer = result if result is not None else instruction_pointer + 2
        elif operation == out:
            output += operation(registers, operand)
            instruction_pointer += 2
        else:
            operation(registers, operand)
            instruction_pointer += 2
    return ','.join(output)


def part_1(registers: list[int], program: list[int]):
    print(run_program(registers, program))


def part_2(registers: list[int], program: list[int]):
    possibilities = []
    for j in range(8):
        registers[A] = j
        registers[B] = 0
        registers[C] = 0
        result = int(run_program(registers, program))
        if result == program[-1]:
            possibilities.append(j)

    for i in range(len(program) - 2, -1, -1):
        new_possibilities = []
        for possibility in possibilities:
            for j in range(8):
                a_value = (possibility << 3) | j
                registers[A] = a_value
                registers[B] = 0
                registers[C] = 0
                result = run_program(registers, program)
                if result == ','.join(map(str, program[i:])):
                    new_possibilities.append(a_value)
        possibilities = new_possibilities
    print(min(possibilities))


if __name__ == '__main__':
    with (open('inputs/day_17.txt', 'r') as file):
        INPUT = file.read()
    REGISTERS, PROGRAM = INPUT.split('\n\n')
    REGISTERS = [int(x) for x in re.findall(r'\d+', REGISTERS)]
    PROGRAM = [int(y) for y in re.findall(r'\d+', PROGRAM)]

    start_time = time.time()
    print('----- PART 1 -----')
    part_1(REGISTERS, PROGRAM)
    print('\nExecution time:', time.time() - start_time)

    start_time = time.time()
    print('\n----- PART 2 -----')
    part_2(REGISTERS, PROGRAM)
    print('\nExecution time:', time.time() - start_time)
