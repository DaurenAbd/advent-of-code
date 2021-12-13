import functools
import statistics
from typing import List


def read_input() -> List[str]:
    with open('input.txt', 'r') as reader:
        return [line.strip() for line in reader.readlines()]


CHARS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}
SYNTAX_ERROR_SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}
COMPLETION_SCORES = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


def syntax_error_score(chunk: str) -> int:
    stack = []

    for c in chunk:
        if c in CHARS:
            stack.append(c)
        else:
            if not stack or CHARS[stack[-1]] != c:
                return SYNTAX_ERROR_SCORES[c]
            stack.pop()

    return 0


def task1(chunks: List[str]) -> int:
    return sum(map(syntax_error_score, chunks))


def completion_score(chunk: str) -> int:
    stack = []

    for c in chunk:
        if c in CHARS:
            stack.append(c)
        else:
            if not stack or CHARS[stack[-1]] != c:
                return 0
            stack.pop()

    return functools.reduce(lambda score, char: score * 5 + COMPLETION_SCORES[CHARS[char]], reversed(stack), 0)


def task2(chunks: List[str]) -> int:
    return statistics.median(filter(lambda score: score > 0, map(completion_score, chunks)))


if __name__ == '__main__':
    chunks = read_input()
    print(task1(chunks))
    print(task2(chunks))
