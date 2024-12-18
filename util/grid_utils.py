import enum


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2D(self.x * other, self.y * other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

    def __iter__(self):
        yield self.x
        yield self.y

    def __repr__(self):
        return f'({self.x}, {self.y})'

    @staticmethod
    def is_horizontally_adjacent(a: ['Vector2D'], b: ['Vector2D']) -> bool:
        return a.y == b.y and abs(a.x - b.x) == 1

    @staticmethod
    def is_vertically_adjacent(a: ['Vector2D'], b: ['Vector2D']) -> bool:
        return a.x == b.x and abs(a.y - b.y) == 1


class Direction(enum.Enum):
    UP = Vector2D(0, -1)
    RIGHT = Vector2D(1, 0)
    DOWN = Vector2D(0, 1)
    LEFT = Vector2D(-1, 0)

    def turn_90_degrees(self) -> ['Direction']:
        if self == Direction.UP:
            return Direction.RIGHT
        if self == Direction.RIGHT:
            return Direction.DOWN
        if self == Direction.DOWN:
            return Direction.LEFT
        if self == Direction.LEFT:
            return Direction.UP

    def __le__(self, other):
        return self.value <= other.value

    def __lt__(self, other):
        return self.value < other.value


class Grid:
    def __init__(self, grid: [[]]):
        self.grid = grid
        self.grid_width = len(grid[0])
        self.grid_height = len(grid)

    @classmethod
    def from_file(cls, file_path: str, transform=lambda x: x) -> 'Grid':
        with open(file_path, 'r') as file:
            return cls.from_text(file.read(), transform)

    @classmethod
    def from_text(cls, text: str, transform=lambda x: x) -> 'Grid':
        grid = [list(map(transform, row)) for row in text.split('\n')]
        return cls(grid)

    def all_positions(self) -> [Vector2D]:
        return [Vector2D(x, y) for x in range(self.grid_width) for y in range(self.grid_height)]

    def get(self, x: int, y: int):
        return self.grid[y][x]

    def put(self, x: int, y: int, value):
        self.grid[y][x] = value

    def find(self, value) -> Vector2D:
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == value:
                    return Vector2D(x, y)

    def find_all(self, value) -> [Vector2D]:
        return [Vector2D(x, y) for y, row in enumerate(self.grid) for x, cell in enumerate(row) if cell == value]

    def adjacent_positions(self, x: int, y: int) -> [Vector2D]:
        return [vector for vector in [Vector2D(x - 1, y), Vector2D(x + 1, y), Vector2D(x, y - 1), Vector2D(x, y + 1)]
                if self.position_is_on_grid(*vector)]

    def position_is_on_grid(self, x: int, y: int):
        return 0 <= x < self.grid_width and 0 <= y < self.grid_height

    def __repr__(self):
        return '\n'.join([''.join(row) for row in self.grid])
