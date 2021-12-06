from typing import List
import numpy as np


def read_input() -> List[int]:
    with open('input.txt', 'r') as reader:
        return [int(num) for num in reader.readline().split(',')]


# Let's say that fish(k, t) is the number of fish on day k with timer t, then
# fish(k, 0) = fish(k - 1, 1), as 1-timer fish get older;
# fish(k, 1) = fish(k - 1, 2), as 2-timer fish get older;
# fish(k, 2) = fish(k - 1, 3), as 3-timer fish get older;
# fish(k, 3) = fish(k - 1, 4), as 4-timer fish get older;
# fish(k, 4) = fish(k - 1, 5), as 5-timer fish get older;
# fish(k, 5) = fish(k - 1, 6), as 6-timer fish get older;
# fish(k, 6) = fish(k - 1, 7) + fish(k - 1, 0), as 7-timer fish get older and 0-timer fish re-enter the cycle;
# fish(k, 7) = fish(k - 1, 8), as 8-timer fish get older;
# fish(k, 8) = fish(k - 1, 0), as 0-timer fish produce new offsprings;
#
# This logic can be encoded in a matrix M, where M[i][j] is 1 if fish(k, i) depends on fish(k - 1, j)
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
# Let's put all fish(k, i) in a column vector day(k), like this
# day(k) = [
#  [fish(k, 0)],
#  [fish(k, 1)],
#  [fish(k, 2)],
#  [fish(k, 3)],
#  [fish(k, 4)],
#  [fish(k, 5)],
#  [fish(k, 6)],
#  [fish(k, 7)],
#  [fish(k, 8)]
# ],
# then day(k) = M * day(k - 1).
# Using the same logic, day(k + 1) = M * day(k) = M * (M * day(k - 1)) = M^2 * day(k - 1).
# In general, day(k) = M^k * day(0). We already know day(0) from the input, and M^k can be computed using
# exponentiation by squaring, thus resulting in O(log(k)) time complexity.


def task(fish: List[int], k: int) -> int:
    day_0 = [0] * 9
    for fish in fish:
        day_0[fish] += 1
    day_0 = np.matrix([[timer] for timer in day_0], dtype='int64')

    return (M ** k * day_0).sum()


if __name__ == '__main__':
    print(task(read_input(), 80))
    print(task(read_input(), 256))
