import heapq
from typing import List, Tuple, Iterator


def parse_line(line: str) -> List[int]:
    return [int(c) for c in line.strip()]


def read_input() -> List[List[int]]:
    with open('input.txt', 'r') as reader:
        return [parse_line(line) for line in reader.readlines()]


class Grid:
    DELTAS = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    grid: List[List[int]]
    n: int
    m: int
    height: int
    width: int

    def __init__(self, grid: List[List[int]], repeats: int):
        self.grid = grid
        self.n = len(grid)
        self.m = len(grid[0])
        self.height = self.n * repeats
        self.width = self.m * repeats

    def get(self, x: int, y: int):
        value = self.grid[x % self.n][y % self.m]
        dx, dy = x // self.n, y // self.m
        return (value + dx + dy - 1) % 9 + 1

    def neighbours(self, x: int, y: int) -> Iterator[Tuple[int, int]]:
        for dx, dy in self.DELTAS:
            i, j = x + dx, y + dy
            if 0 <= i < self.height and 0 <= j < self.width:
                yield i, j

    
def dijkstra(grid: Grid) -> int:
    inf = grid.height * grid.width * 10
    dist = [[inf] * grid.width for _ in range(grid.height)]
    dist[0][0] = 0
    heap = [(dist[0][0], 0, 0)]

    while heap:
        d, x, y = heapq.heappop(heap)

        if d != dist[x][y]:
            continue

        for i, j in grid.neighbours(x, y):
            if dist[i][j] > d + grid.get(i, j):
                dist[i][j] = d + grid.get(i, j)
                heapq.heappush(heap, (dist[i][j], i, j))

    return dist[grid.height - 1][grid.width - 1]


def task1(grid: List[List[int]]) -> int:
    return dijkstra(Grid(grid, repeats=1))


def task2(grid: List[List[int]]) -> int:
    return dijkstra(Grid(grid, repeats=5))


if __name__ == '__main__':
    grid = read_input()
    print(task1(grid))
    print(task2(grid))
