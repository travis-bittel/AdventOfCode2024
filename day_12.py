import time

from util.grid_utils import Direction, Grid, Vector2D


def part_1(grid: Grid):
    unvisited_set = set()
    unvisited_set.update(grid.all_positions())

    total_price = 0
    while unvisited_set:
        start = next(iter(unvisited_set))
        to_explore = [start]
        plant_type = grid.get(*start)
        region_area = 0
        region_perimeter = 0
        while to_explore:
            current_position = to_explore.pop()
            if current_position in unvisited_set:
                unvisited_set.remove(current_position)
            else:
                continue
            adjacent_cells_of_same_type \
                = [adjacent_position for adjacent_position in grid.adjacent_positions(*current_position)
                   if grid.get(*adjacent_position) == plant_type]
            region_perimeter += 4 - len(adjacent_cells_of_same_type)
            region_area += 1
            to_explore.extend(adjacent_cells_of_same_type)
        total_price += region_area * region_perimeter
    print(total_price)


def part_2(grid: Grid):
    unvisited_set = set()
    unvisited_set.update(grid.all_positions())

    total_price = 0
    while unvisited_set:
        start = next(iter(unvisited_set))
        to_explore = [start]
        plant_type = grid.get(*start)
        region_area = 0
        perimeter_cells = set()
        while to_explore:
            current_position = to_explore.pop()
            if current_position in unvisited_set:
                unvisited_set.remove(current_position)
            else:
                continue
            adjacent_cells_of_same_type = [adjacent_position for adjacent_position
                                           in grid.adjacent_positions(*current_position)
                                           if grid.get(*adjacent_position) == plant_type]
            for direction in list(Direction):
                if current_position + direction.value not in adjacent_cells_of_same_type:
                    perimeter_cells.add((current_position, direction))
            region_area += 1
            to_explore.extend(adjacent_cells_of_same_type)
        sides = number_of_sides(perimeter_cells, grid)
        total_price += region_area * sides
    print(total_price)


def number_of_sides(perimeter_cells: set[(Vector2D, Direction)], grid: Grid) -> int:
    sides = 0
    while perimeter_cells:
        sides += 1
        start = perimeter_cells.pop()
        start_position, start_direction = start
        adjacent_perimeter_cells = [(adjacent_position, start_direction) for adjacent_position
                                    in grid.adjacent_positions(*start_position)
                                    if (adjacent_position, start_direction) in perimeter_cells]
        search_horizontally = any(Vector2D.is_horizontally_adjacent(start_position, cell[0])
                                  and start_direction == cell[1] for cell in adjacent_perimeter_cells)

        to_explore = set()
        to_explore.add(start)
        while to_explore:
            current = to_explore.pop()
            current_position, current_direction = current
            if current in perimeter_cells:
                perimeter_cells.remove(current)
            adjacent_perimeter_cells = [(adjacent_position, current_direction) for adjacent_position
                                        in grid.adjacent_positions(*current_position)
                                        if (adjacent_position, current_direction) in perimeter_cells]
            if search_horizontally:
                for perimeter_cell in adjacent_perimeter_cells:
                    if Vector2D.is_horizontally_adjacent(current_position, perimeter_cell[0]):
                        to_explore.add(perimeter_cell)
            else:
                for perimeter_cell in adjacent_perimeter_cells:
                    if Vector2D.is_vertically_adjacent(current_position, perimeter_cell[0]):
                        to_explore.add(perimeter_cell)
    return sides


if __name__ == '__main__':
    GRID = Grid.from_file('inputs/day_12.txt')
    start_time = time.time()
    print('----- PART 1 -----')
    part_1(GRID)
    print('\nExecution time:', time.time() - start_time)

    print('\n----- PART 2 -----')
    part_2(GRID)
    print('\nExecution time:', time.time() - start_time)
