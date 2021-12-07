import collections
from typing import List


def read_input() -> List[int]:
    with open('input.txt', 'r') as reader:
        return [int(num) for num in reader.readline().split(',')]


def task1(positions: List[int]) -> int:
    counter = collections.Counter(positions)
    crabs = [(k, v) for k, v in counter.items()]
    crabs.sort()
    n = len(crabs)

    right = 0
    right_count = 0
    for i in range(1, n):
        right += (crabs[i][0] - crabs[0][0]) * crabs[i][1]
        right_count += crabs[i][1]

    left = 0
    left_count = crabs[0][1]
    answer = left + right

    for i in range(1, n):
        pos_diff = crabs[i][0] - crabs[i - 1][0]

        left += left_count * pos_diff
        left_count += crabs[i][1]

        right -= right_count * pos_diff
        right_count -= crabs[i][1]

        answer = min(answer, left + right)

    return answer


class CrabGroup:
    def __init__(self, count: int):
        self.count = count
        self.bias = 0
        self.cost = 1

    def add(self, count: int):
        self.bias += (self.cost - 1) * self.count
        self.count += count
        self.cost = 1

    def move(self) -> int:
        move_cost = self.cost * self.count + self.bias
        self.cost += 1
        return move_cost


def task2(positions: List[int]) -> int:
    counter = collections.Counter(positions)
    L, R = min(counter.keys()), max(counter.keys())

    left_group = CrabGroup(0)
    left_costs = collections.Counter()

    for i in range(L, R + 1):
        left_costs[i] = left_costs[i - 1] + left_group.move()
        left_group.add(counter[i])

    right_group = CrabGroup(0)
    right_costs = collections.Counter()

    for i in range(R, L - 1, -1):
        right_costs[i] = right_costs[i + 1] + right_group.move()
        right_group.add(counter[i])

    return min(left_costs[i] + right_costs[i] for i in range(L, R + 1))


if __name__ == '__main__':
    print(task2(read_input()))
