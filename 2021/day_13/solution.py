from dataclasses import dataclass
from typing import List, Set, Tuple

from PIL import Image
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


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

    def fold_x(self, x: int):
        right_side = {point for point in self.points if point.x > x}
        self.points.difference_update(right_side)

        folded_right_side = {Point(2 * x - point.x, point.y) for point in right_side}
        self.points.update(folded_right_side)

    def fold_y(self, y: int):
        down_side = {point for point in self.points if point.y > y}
        self.points.difference_update(down_side)

        folded_down_side = {Point(point.x, 2 * y - point.y) for point in down_side}
        self.points.update(folded_down_side)

    def apply(self, fold: Fold):
        if fold.axis == 'x':
            self.fold_x(fold.value)
        if fold.axis == 'y':
            self.fold_y(fold.value)

    def as_text(self) -> str:
        min_x = min(point.x for point in self.points)
        min_y = min(point.y for point in self.points)
        max_x = max(point.x for point in self.points)
        max_y = max(point.y for point in self.points)

        # extra +2's to add 1 pixel padding to the image
        width = max_x - min_x + 3
        height = max_y - min_y + 3
        image = Image.new('L', (width, height), 255)

        for point in self.points:
            # extra +1's to add 1 pixel padding to the image
            image.putpixel((point.x - min_x + 1, point.y - min_y + 1), 0)

        # "psm 8" means that the image will be interpreted a single word
        return pytesseract.image_to_string(image, config='--psm 8')


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
    return matrix.as_text()


if __name__ == '__main__':
    points, folds = read_input()
    print(task1(points, folds))
    print(task2(points, folds))
