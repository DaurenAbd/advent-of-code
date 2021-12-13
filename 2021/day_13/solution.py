from dataclasses import dataclass
from typing import List, Set, Tuple


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int


@dataclass(eq=True, frozen=True)
class Fold:
    axis: str
    value: int


class Matrix:
    points: Set[Point]

    def __init__(self, points: Set[Point]):
        self.points = points

    def apply(self, fold: Fold):
        if fold.axis == 'x':
            on_axis = {point for point in self.points if point.x == fold.value}
            down_side = {point for point in self.points if point.x > fold.value}
            self.points.difference_update(on_axis)
            self.points.difference_update(down_side)
            folded_down_side = {Point(2 * fold.value - point.x, point.y) for point in down_side}
            self.points.update(folded_down_side)
        if fold.axis == 'y':
            on_axis = {point for point in self.points if point.y == fold.value}
            down_side = {point for point in self.points if point.y > fold.value}
            self.points.difference_update(on_axis)
            self.points.difference_update(down_side)
            folded_down_side = {Point(point.x, 2 * fold.value - point.y) for point in down_side}
            self.points.update(folded_down_side)

    def __str__(self) -> str:
        min_x = min(point.x for point in self.points)
        min_y = min(point.y for point in self.points)
        max_x = max(point.x for point in self.points)
        max_y = max(point.y for point in self.points)
        table = [['.'] * (max_x - min_x + 1) for _ in range(max_y - min_y + 1)]
        for point in self.points:
            table[point.y - min_y][point.x - min_x] = '@'
        return '\n'.join(''.join(row) for row in table)


def read_input() -> Tuple[Set[Point], List[Fold]]:
    with open('input.txt', 'r') as reader:
        it = iter(reader)
        points = set()
        folds = []

        for line in it:
            line = line.strip()
            if not line:
                break
            x, y = line.split(',')
            points.add(Point(int(x), int(y)))

        for line in it:
            line = line.strip()
            axis, value = line.split(' ')[2].split('=')
            folds.append(Fold(axis, int(value)))

        return points, folds


def task1(points: Set[Point], folds: List[Fold]) -> int:
    matrix = Matrix(points)
    matrix.apply(folds[0])
    return len(matrix.points)


def task2(points: Set[Point], folds: List[Fold]) -> str:
    matrix = Matrix(points)
    for fold in folds:
        matrix.apply(fold)
    return str(matrix)


if __name__ == '__main__':
    points, folds = read_input()
    print(task1(points, folds))
    print(task2(points, folds))
