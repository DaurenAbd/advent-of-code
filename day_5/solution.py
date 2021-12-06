import collections
from dataclasses import dataclass
from typing import Iterator, List


def between(start: int, end: int) -> Iterator[int]:
    inclusive_end = end + 1 if start < end else end - 1
    step = 1 if start < end else -1
    return range(start, inclusive_end, step)


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int


@dataclass
class Line:
    p1: Point
    p2: Point

    def integer_points(self) -> Iterator[Point]:
        if self.is_vertical:
            return (Point(self.p1.x, y) for y in between(self.p1.y, self.p2.y))

        if self.is_horizontal:
            return (Point(x, self.p1.y) for x in between(self.p1.x, self.p2.x))

        return (Point(x, y) for x, y in zip(between(self.p1.x, self.p2.x), between(self.p1.y, self.p2.y)))

    @property
    def is_horizontal(self) -> bool:
        return self.p1.y == self.p2.y

    @property
    def is_vertical(self) -> bool:
        return self.p1.x == self.p2.x


def parse_line(line: str) -> Line:
    start, end = line.split(' -> ')
    x1, y1 = start.split(',')
    x2, y2 = end.split(',')
    return Line(Point(int(x1), int(y1)), Point(int(x2), int(y2)))


def read_input() -> List[Line]:
    with open('input.txt', 'r') as reader:
        return [parse_line(line) for line in reader.readlines()]


def task1(lines: List[Line]) -> int:
    counter = collections.Counter()

    for line in lines:
        if line.is_vertical or line.is_horizontal:
            counter.update(line.integer_points())

    return sum(1 for count in counter.values() if count > 1)


def task2(lines: List[Line]) -> int:
    counter = collections.Counter()

    for line in lines:
        counter.update(line.integer_points())

    return sum(1 for count in counter.values() if count > 1)


if __name__ == '__main__':
    lines = read_input()
    print(task1(lines))
    print(task2(lines))
