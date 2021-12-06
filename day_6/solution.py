from typing import List
import numpy as np


def read_input() -> List[int]:
    with open('input.txt', 'r') as reader:
        return [int(num) for num in reader.readline().split(',')]


M = np.matrix([
    [0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0]
], dtype='int64')


def task(fishes: List[int], days: int) -> int:
    timers = [0] * 9

    for fish in fishes:
        timers[fish] += 1

    timers = np.matrix([[timer] for timer in timers], dtype='int64')

    return (M ** days * timers).sum()


if __name__ == '__main__':
    print(task(read_input(), 80))
    print(task(read_input(), 256))
