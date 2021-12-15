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
    N: int
    M: int

    def __init__(self, grid: List[List[int]], repeats: int):
        self.grid = grid
        self.n = len(grid)
        self.m = len(grid[0])
        self.N = self.n * repeats
        self.M = self.m * repeats

    @property
    def start(self) -> Tuple[int, int]:
        return 0, 0

    @property
    def finish(self) -> Tuple[int, int]:
        return self.N - 1, self.M - 1

    def value_at(self, x: int, y: int):
        value = self.grid[x % self.n][y % self.m]
        dx, dy = x // self.n, y // self.m
        return (value + dx + dy - 1) % 9 + 1

    def neighbours(self, x: int, y: int) -> Iterator[Tuple[int, int]]:
        for dx, dy in self.DELTAS:
            i, j = x + dx, y + dy
            if 0 <= i < self.N and 0 <= j < self.M:
                yield i, j

    def dijkstra(self) -> int:
        start_x, start_y = self.start
        inf = self.N * self.M * 10
        dist = [[inf] * self.M for _ in range(self.N)]
        dist[start_x][start_y] = 0
        heap = [(dist[start_x][start_y], start_x, start_y)]

        while heap:
            d, x, y = heapq.heappop(heap)

            if d != dist[x][y]:
                continue

            for i, j in self.neighbours(x, y):
                if dist[i][j] > d + self.value_at(i, j):
                    dist[i][j] = d + self.value_at(i, j)
                    heapq.heappush(heap, (dist[i][j], i, j))

        return dist[self.finish[0]][self.finish[1]]


def task1(grid: List[List[int]]) -> int:
    return Grid(grid, repeats=1).dijkstra()


def task2(grid: List[List[int]]) -> int:
    return Grid(grid, repeats=5).dijkstra()


if __name__ == '__main__':
    grid = read_input()
    print(task1(grid))
    print(task2(grid))
