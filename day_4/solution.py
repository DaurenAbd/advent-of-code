import math
from typing import Dict, List, Tuple

Board = List[List[int]]


def parse_board(lines: List[str]) -> Board:
    return [[int(num) for num in line.split()] for line in lines]


def read_input() -> Tuple[List[int], List[Board]]:
    with open('input.txt', 'r') as reader:
        raw_lines = reader.readlines()
        stripped_lines = map(lambda line: line.strip(), raw_lines)
        non_empty_lines = filter(lambda line: line, stripped_lines)
        lines = list(non_empty_lines)

        moves = [int(move) for move in lines[0].split(',')]
        boards = [parse_board(lines[i - 5: i]) for i in range(6, len(lines) + 1, 5)]

        return moves, boards


def winning_time_and_score(board: Board, move_times: Dict[int, int]) -> Tuple[int, int]:
    timing_board = [[(move_times.get(num, math.inf), num) for num in row] for row in board]

    rows = min(max(timing_board[i]) for i in range(5))
    cols = min(max(timing_board[i][j] for i in range(5)) for j in range(5))
    winning_time, last_move = min(rows, cols)

    unmarked = sum(num for row in timing_board for t, num in row if t > winning_time)

    return winning_time, unmarked * last_move


def task1(moves: List[int], boards: List[Board]) -> int:
    move_times = {move: i for i, move in enumerate(moves)}
    results = [winning_time_and_score(board, move_times) for board in boards]
    return min(results)[1]


def task2(moves: List[int], boards: List[Board]) -> int:
    move_times = {move: i for i, move in enumerate(moves)}
    results = [winning_time_and_score(board, move_times) for board in boards]
    return max(results)[1]


if __name__ == '__main__':
    moves, boards = read_input()
    print(task1(moves, boards))
    print(task2(moves, boards))
