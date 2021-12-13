import collections
from typing import List, Tuple


def read_line(line: str) -> List[int]:
    return list(map(int, line.strip()))


def read_input() -> List[List[int]]:
    with open('input.txt', 'r') as reader:
        return list(map(read_line, reader.readlines()))


class Matrix:
    DELTAS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def __init__(self, energy: List[List[int]]):
        self.energy = energy
        self.n = len(energy)
        self.m = len(energy[0])

    def neighbours(self, x: int, y: int):
        for dx, dy in self.DELTAS:
            i, j = x + dx, y + dy
            if 0 <= i < self.n and 0 <= j < self.m:
                yield i, j

    def coordinates(self):
        for x in range(self.n):
            for y in range(self.m):
                yield x, y

    def normalise(self) -> int:
        flashes = 0

        for x, y in self.coordinates():
            if self.energy[x][y] == 10:
                flashes += 1
                self.energy[x][y] = 0

        return flashes

    def increment(self) -> List[Tuple[int, int]]:
        flashes = []

        for x, y in self.coordinates():
            self.energy[x][y] += 1
            if self.energy[x][y] == 10:
                flashes.append((x, y))

        return flashes

    def flash(self, x: int, y: int) -> List[Tuple[int, int]]:
        flashes = []

        for i, j in self.neighbours(x, y):
            if self.energy[i][j] == 10:
                continue
            self.energy[i][j] += 1
            if self.energy[i][j] == 10:
                flashes.append((i, j))

        return flashes

    def next_step(self) -> int:
        queue = collections.deque(self.increment())

        while queue:
            x, y = queue.popleft()
            queue.extend(self.flash(x, y))

        return self.normalise()

    def is_synced(self) -> bool:
        return all(e == self.energy[0][0] for row in self.energy for e in row)


def task1(energy: List[List[int]], steps: int) -> int:
    matrix = Matrix(energy)
    answer = 0

    for _ in range(steps):
        answer += matrix.next_step()

    return answer


def task2(energy: List[List[int]]) -> int:
    matrix = Matrix(energy)
    answer = 0

    while not matrix.is_synced():
        answer += 1
        matrix.next_step()

    return answer


if __name__ == '__main__':
    print(task1(read_input(), 100))
    print(task2(read_input()))
