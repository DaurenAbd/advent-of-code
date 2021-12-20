from typing import List, Tuple


class Matrix:
    DELTAS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]

    filler: int
    grid: List[List[int]]
    length: int
    width: int
    algorithm: List[int]

    def __init__(self, algorithm: List[int], grid: List[List[int]]):
        self.filler = 0
        self.grid = grid
        self.length = len(grid)
        self.width = len(grid[0])
        self.algorithm = algorithm
        self.normalise()

    def is_filled(self, layer: int) -> bool:
        for i in range(self.length):
            if self.grid[i][layer] != self.filler or self.grid[i][self.width - 1 - layer] != self.filler:
                return False

        for j in range(self.width):
            if self.grid[layer][j] != self.filler or self.grid[self.length - 1 - layer][j] != self.filler:
                return False

        return True

    def outer_layer_thickness(self) -> int:
        max_thickness = min((self.length + 1) // 2, (self.width + 1) // 2)
        for layer in range(max_thickness):
            if not self.is_filled(layer):
                return layer
        return max_thickness

    def remove_boundary(self, thickness: int):
        self.grid = [row[thickness: -thickness] for row in self.grid[thickness: -thickness]]
        self.length = len(self.grid)
        self.width = len(self.grid[0])

    def add_boundary(self):
        empty_cell = lambda: [self.filler]
        empty_row = lambda: [empty_cell() * (self.width + 2)]
        extended_row = lambda row: empty_cell() + row + empty_cell()
        self.grid = empty_row() + [extended_row(row) for row in self.grid] + empty_row()
        self.length = len(self.grid)
        self.width = len(self.grid[0])

    def normalise(self):
        thickness = self.outer_layer_thickness()
        if thickness > 1:
            self.remove_boundary(thickness - 1)
        if thickness == 0:
            self.add_boundary()

    def apply_algorithm(self, x: int, y: int) -> int:
        value = 0
        powers = reversed(range(len(self.DELTAS)))

        for power, (dx, dy) in zip(powers, self.DELTAS):
            i, j = x + dx, y + dy
            if 0 <= i < self.length and 0 <= j < self.width:
                value ^= self.grid[i][j] << power
            else:
                value ^= self.filler << power

        return self.algorithm[value]

    def next_step(self):
        self.grid = [[self.apply_algorithm(i, j) for j in range(self.width)] for i in range(self.length)]
        self.filler = self.apply_algorithm(-1, -1)
        self.normalise()

    def lit_pixel_count(self) -> int:
        return sum(map(sum, self.grid))


def read_input() -> Tuple[List[int], List[List[int]]]:
    with open('input.txt', 'r') as reader:
        algorithm, grid = reader.read().split('\n\n')
        algorithm = [(1 if c == '#' else 0) for c in algorithm.strip()]
        grid = [[(1 if c == '#' else 0) for c in row.strip()] for row in grid.split()]
        return algorithm, grid


def task(algorithm: List[int], grid: List[List[int]], steps: int) -> int:
    matrix = Matrix(algorithm, grid)
    for _ in range(steps):
        matrix.next_step()
    return matrix.lit_pixel_count()


if __name__ == '__main__':
    algorithm, grid = read_input()
    print(task(algorithm, grid, 2))
    print(task(algorithm, grid, 50))
