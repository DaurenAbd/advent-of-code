import collections
import functools
import heapq
import operator
from dataclasses import dataclass
from typing import List, Tuple, Iterator, Set

DELTAS = [(-1, 0), (0, -1), (0, 1), (1, 0)]


@dataclass
class Matrix:
    heights: List[List[int]]

    @property
    def n(self) -> int:
        return len(self.heights)

    @property
    def m(self) -> int:
        return len(self.heights[0])

    def get(self, x: int, y: int) -> int:
        return self.heights[x][y]

    def coordinates(self) -> Iterator[Tuple[int, int, int]]:
        for x in range(self.n):
            for y in range(self.m):
                yield x, y, self.get(x, y)

    def neighbours(self, x: int, y: int) -> Iterator[Tuple[int, int, int]]:
        for dx, dy in DELTAS:
            i, j = x + dx, y + dy
            if 0 <= i < self.n and 0 <= j < self.m:
                yield i, j, self.get(i, j)

    def is_low_point(self, x: int, y: int) -> bool:
        height = self.get(x, y)
        for i, j, h in self.neighbours(x, y):
            if height >= h:
                return False
        return True

    def task1(self) -> int:
        answer = 0
        for x, y, h in self.coordinates():
            if self.is_low_point(x, y):
                answer += h + 1
        return answer

    def get_basin(self, x: int, y: int) -> Set[Tuple[int, int]]:
        basin = {(x, y)}
        queue = collections.deque([(x, y)])

        while queue:
            x, y = queue.popleft()
            for i, j, h in self.neighbours(x, y):
                if h != 9 and (i, j) not in basin:
                    basin.add((i, j))
                    queue.append((i, j))

        return basin

    def task2(self) -> int:
        used = set()
        basin_sizes = []

        for x, y, h in self.coordinates():
            if h != 9 and (x, y) not in used:
                basin = self.get_basin(x, y)
                used.update(basin)

                if len(basin_sizes) < 3:
                    heapq.heappush(basin_sizes, len(basin))
                elif basin_sizes[0] < len(basin):
                    heapq.heapreplace(basin_sizes, len(basin))

        return functools.reduce(operator.mul, basin_sizes)


def parse_line(line: str) -> List[int]:
    return [int(c) for c in line.strip()]


def read_input() -> List[List[int]]:
    with open('input.txt', 'r') as reader:
        return [parse_line(line) for line in reader.readlines()]


if __name__ == '__main__':
    matrix = Matrix(read_input())
    print(matrix.task1())
    print(matrix.task2())
