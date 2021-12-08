import itertools
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Display:
    numbers: List[str]
    outputs: List[str]


def parse_line(line: str) -> Display:
    left, right = line.split(' | ')
    return Display(left.split(), right.split())


def read_input() -> List[Display]:
    with open('input.txt', 'r') as reader:
        return [parse_line(line) for line in reader.readlines()]


def task1(displays: List[Display]) -> int:
    answer = 0
    for display in displays:
        for output in display.outputs:
            if len(output) in (2, 3, 4, 7):
                answer += 1
    return answer


SEGMENTS = 'abcdefg'
DIGITS = {
    'abcefg': '0',
    'cf': '1',
    'acdeg': '2',
    'acdfg': '3',
    'bcdf': '4',
    'abdfg': '5',
    'abdefg': '6',
    'acf': '7',
    'abcdefg': '8',
    'abcdfg': '9'
}


def shuffles():
    permutations = itertools.permutations(SEGMENTS)
    return map(lambda permutation: dict(zip(SEGMENTS, permutation)), permutations)


def convert(code: str, shuffle: Dict[str, str]) -> str:
    return ''.join(sorted(map(shuffle.get, code)))


def try_to_decode(display: Display, shuffle: Dict[str, str]) -> Optional[int]:
    for code in itertools.chain(display.numbers, display.outputs):
        if convert(code, shuffle) not in DIGITS:
            return None
    decoded_outputs = (DIGITS[convert(output, shuffle)] for output in display.outputs)
    return int(''.join(decoded_outputs))


def task2(displays: List[Display]) -> int:
    answer = 0
    for display in displays:
        for shuffle in shuffles():
            decoding = try_to_decode(display, shuffle)
            if decoding is not None:
                answer += decoding
                break
    return answer


if __name__ == '__main__':
    print(task1(read_input()))
    print(task2(read_input()))
