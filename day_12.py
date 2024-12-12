import time
from dataclasses import dataclass

from util.grid_utils import Direction, Grid, Vector2D


@dataclass
class Region:
    area: int
    perimeter: int
    all_cells: set[Vector2D]
    perimeter_cells: set[(Vector2D, Direction)]
    plant_type: str


def get_regions(grid: Grid) -> [Region]:
    regions = []
    unvisited_set = set()
    unvisited_set.update(grid.all_positions())
    while unvisited_set:
        start = next(iter(unvisited_set))
        to_explore = [start]
        all_cells = set()
        perimeter_cells = set()
        plant_type = grid.get(*start)
        while to_explore:
            current_position = to_explore.pop()
            if current_position in unvisited_set:
                all_cells.add(current_position)
                unvisited_set.remove(current_position)
            else:
                continue
            adjacent_cells_of_same_type \
                = [adjacent_position for adjacent_position in grid.adjacent_positions(*current_position)
                   if grid.get(*adjacent_position) == plant_type]
            for direction in list(Direction):
                if current_position + direction.value not in adjacent_cells_of_same_type:
                    perimeter_cells.add((current_position, direction))
            to_explore.extend(adjacent_cells_of_same_type)
        regions.append(Region(len(all_cells), len(perimeter_cells), all_cells, perimeter_cells, plant_type))
    return regions


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


def part_1(grid: Grid):
    regions = get_regions(grid)
    print(sum(region.area * region.perimeter for region in regions))


def part_2(grid: Grid):
    regions = get_regions(grid)
    print(sum(region.area * number_of_sides(region.perimeter_cells, grid) for region in regions))


if __name__ == '__main__':
    GRID = Grid.from_file('inputs/day_12.txt')
    start_time = time.time()
    print('----- PART 1 -----')
    part_1(GRID)
    print('\nExecution time:', time.time() - start_time)

    print('\n----- PART 2 -----')
    part_2(GRID)
    print('\nExecution time:', time.time() - start_time)
