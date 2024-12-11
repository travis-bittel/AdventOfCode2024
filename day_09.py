import time
from dataclasses import dataclass

# left_pointer, right_pointer, open_slots, blocks_to_place, block_placing_id
# If there is no space in open_slots, advance left pointer.
#    If left_pointer is a memory block, process it. If it is an empty block, add the number of slots to open_slots.
# If there is space in open_slots, process the blocks_to_place, calculating the whatever solution thing, subtracting
# from open_slots and blocks_to_place.
# If blocks_to_place is empty, advance right_pointer
#    If right_pointer is a memory block, add it to blocks_to_place and update block_placing_id. If it is an empty block,
#    discard it.


def checksum_for_file_block(start_index: int, file_id: int, size: int) -> int:
    checksum = 0
    for i in range(start_index, start_index + size):
        checksum += i * file_id
    return checksum


def part_1(puzzle_input: [int]):
    total_checksum = 0

    left_pointer = -1
    right_pointer = len(puzzle_input)
    open_slots = 0
    blocks_to_place = 0
    file_id_to_place = 0

    blocks_counted = 0

    while left_pointer < right_pointer:
        if open_slots == 0:
            left_pointer += 1

            # Avoid letting the left pointer count the last file's memory blocks. Otherwise, we will count the block as
            # being full when part of it has been moved. We instead count the remaining portion after the while loop
            if left_pointer == right_pointer:
                break

            if left_pointer % 2 == 1:
                open_slots += puzzle_input[left_pointer]
            else:
                start_index = blocks_counted
                file_id = left_pointer // 2
                size = puzzle_input[left_pointer]
                total_checksum += checksum_for_file_block(start_index, file_id, size)
                blocks_counted += size
        else:
            if blocks_to_place > 0:
                slots_to_fill = min(open_slots, blocks_to_place)
                open_slots -= slots_to_fill
                blocks_to_place -= slots_to_fill
                total_checksum += checksum_for_file_block(blocks_counted, file_id_to_place, slots_to_fill)
                blocks_counted += slots_to_fill
            else:
                right_pointer -= 1
                if right_pointer % 2 == 0:
                    blocks_to_place += puzzle_input[right_pointer]
                    file_id_to_place = right_pointer // 2
    # Count remaining blocks_to_place
    if blocks_to_place > 0:
        total_checksum += checksum_for_file_block(blocks_counted, file_id_to_place, blocks_to_place)
    print(total_checksum)


@dataclass
class MemoryBlock:
    start_index: int
    length: int
    file_id: int


def checksum_for_memory_block(memory_block: MemoryBlock) -> int:
    checksum = 0
    for i in range(memory_block.start_index, memory_block.start_index + memory_block.length):
        if memory_block.file_id != -1:
            checksum += i * memory_block.file_id
    return checksum


def print_memory_blocks(memory_blocks: [MemoryBlock]):
    output = []
    for memory_block in memory_blocks:
        for i in range(memory_block.start_index, memory_block.start_index + memory_block.length):
            output.append('.' if memory_block.file_id == -1 else memory_block.file_id)
    print(''.join(map(str, output)))


def part_2(puzzle_input: [int]):
    total_checksum = 0

    EMPTY_BLOCK_ID = -1

    memory_blocks = []
    current_index = 0
    for i, block_size in enumerate(puzzle_input):
        start_index = current_index
        length = block_size
        file_id = EMPTY_BLOCK_ID if i % 2 == 1 else i // 2
        memory_blocks.append(MemoryBlock(start_index, length, file_id))
        current_index += length

    new_location = 0
    right_pointer = len(memory_blocks) - 1

    while right_pointer > 0:
        while memory_blocks[right_pointer].file_id == EMPTY_BLOCK_ID:
            right_pointer -= 1

        found = False
        for i in range(0, right_pointer):
            if memory_blocks[i].file_id == EMPTY_BLOCK_ID \
                    and memory_blocks[i].length >= memory_blocks[right_pointer].length:
                new_location = i
                found = True
                break
        if not found:
            right_pointer -= 1
            continue

        # Move block
        to_move = memory_blocks.pop(right_pointer)
        memory_blocks.insert(right_pointer, MemoryBlock(to_move.start_index,
                                                        to_move.length,
                                                        EMPTY_BLOCK_ID))
        to_move.start_index = memory_blocks[new_location].start_index

        empty_block = memory_blocks.pop(new_location)
        memory_blocks.insert(new_location, MemoryBlock(to_move.start_index + to_move.length,
                                                       empty_block.length - to_move.length,
                                                       EMPTY_BLOCK_ID))
        memory_blocks.insert(new_location, to_move)
        right_pointer -= 1

    for memory_block in memory_blocks:
        total_checksum += checksum_for_memory_block(memory_block)
    print(total_checksum)


if __name__ == '__main__':
    with (open('inputs/day_9.txt', 'r') as file):
        INPUT = file.read()
    INPUT = [int(x) for x in list(INPUT)]
    start_time = time.time()

    print('----- PART 1 -----')
    part_1(INPUT)
    print('\nExecution time:', time.time() - start_time)

    start_time = time.time()
    print('\n----- PART 2 -----')
    part_2(INPUT)
    print('\nExecution time:', time.time() - start_time)
