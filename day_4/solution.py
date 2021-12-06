import math
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(order=True)
class Ball:
    time: int
    num: int


class Board:
    def __init__(self, lines: List[str]):
        self.board = [[int(num) for num in line.split()] for line in lines]

    def as_timing_board(self, ball_times: Dict[int, int]) -> List[List[Ball]]:
        return [[Ball(ball_times.get(num, math.inf), num) for num in row] for row in self.board]

    def winning_time_and_score(self, ball_times: Dict[int, int]) -> Tuple[int, int]:
        timing_board = self.as_timing_board(ball_times)
        rows = min(max(timing_board[i]) for i in range(5))
        cols = min(max(timing_board[i][j] for i in range(5)) for j in range(5))
        winning_ball = min(rows, cols)

        unmarked = sum(ball.num for row in timing_board for ball in row if ball.time > winning_ball.time)

        return winning_ball.time, unmarked * winning_ball.num


def read_input() -> Tuple[List[Ball], List[Board]]:
    with open('input.txt', 'r') as reader:
        raw_lines = reader.readlines()
        stripped_lines = map(lambda line: line.strip(), raw_lines)
        non_empty_lines = filter(lambda line: line, stripped_lines)
        lines = list(non_empty_lines)

        balls = [Ball(t, int(num)) for t, num in enumerate(lines[0].split(','))]
        boards = [Board(lines[i - 5: i]) for i in range(6, len(lines) + 1, 5)]

        return balls, boards


def task1(balls: List[Ball], boards: List[Board]) -> int:
    ball_times = {ball.num: ball.time for ball in balls}
    results = [board.winning_time_and_score(ball_times) for board in boards]
    return min(results)[1]


def task2(balls: List[Ball], boards: List[Board]) -> int:
    ball_times = {ball.num: ball.time for ball in balls}
    results = [board.winning_time_and_score(ball_times) for board in boards]
    return max(results)[1]


if __name__ == '__main__':
    balls, boards = read_input()
    print(task1(balls, boards))
    print(task2(balls, boards))
