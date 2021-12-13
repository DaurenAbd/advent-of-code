import collections
from dataclasses import dataclass
from typing import List


def read_input() -> List[int]:
    with open('input.txt', 'r') as reader:
        return [int(num) for num in reader.readline().split(',')]


@dataclass(order=True)
class CrabGroup1:
    position: int
    count: int

    def add(self, count: int):
        self.count += count

    def move(self, position: int) -> int:
        move_cost = abs(self.position - position) * self.count
        self.position = position
        return move_cost


def task1(positions: List[int]) -> int:
    counter = collections.Counter(positions)
    crabs = [CrabGroup1(position, count) for position, count in counter.items()]
    crabs.sort()
    n = len(crabs)

    right_group = CrabGroup1(crabs[n - 1].position, 0)
    right_costs = [0] * (n + 1)

    for i in reversed(range(n)):
        right_costs[i] = right_costs[i + 1] + right_group.move(crabs[i].position)
        right_group.add(crabs[i].count)

    left_group = CrabGroup1(crabs[0].position, 0)
    left_costs = [0] * n

    for i in range(1, n):
        left_group.add(crabs[i - 1].count)
        left_costs[i] = left_costs[i - 1] + left_group.move(crabs[i].position)

    return min(left_costs[i] + right_costs[i] for i in range(n))


@dataclass(order=True)
class CrabGroup2:
    count: int
    bias: int = 0
    cost: int = 1

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

    left_group = CrabGroup2(0)
    left_costs = collections.Counter()

    for i in range(L, R + 1):
        left_costs[i] = left_costs[i - 1] + left_group.move()
        left_group.add(counter[i])

    right_group = CrabGroup2(0)
    right_costs = collections.Counter()

    for i in range(R, L - 1, -1):
        right_costs[i] = right_costs[i + 1] + right_group.move()
        right_group.add(counter[i])

    return min(left_costs[i] + right_costs[i] for i in range(L, R + 1))


if __name__ == '__main__':
    print(task1(read_input()))
    print(task2(read_input()))
