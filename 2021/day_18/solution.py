import copy
import functools
import operator
from typing import Optional, List, Iterator, Tuple


class Node:
    parent: Optional['Node']
    left: Optional['Node']
    right: Optional['Node']
    value: Optional[int]

    def __init__(self):
        self.parent = None
        self.left = None
        self.right = None
        self.value = None

    @classmethod
    def pair_node(cls, left: 'Node', right: 'Node', parent: Optional['Node'] = None):
        node = cls()
        node.parent = parent
        node.left = left
        node.right = right
        left.parent = node
        right.parent = node
        return node

    @classmethod
    def value_node(cls, value: int, parent: Optional['Node'] = None):
        node = cls()
        node.parent = parent
        node.value = value
        return node

    @property
    def magnitude(self):
        if self.is_value_node:
            return self.value
        else:
            return 3 * self.left.magnitude + 2 * self.right.magnitude

    @property
    def is_value_node(self) -> bool:
        return self.value is not None

    @property
    def is_pair_node(self) -> bool:
        return self.left is not None and self.right is not None

    def add_to_prev(self, value: int):
        node = self
        while node.parent is not None and node.parent.left == node:
            node = node.parent

        if node is None or node.parent is None:
            return

        node = node.parent.left
        while node is not None and node.right is not None:
            node = node.right

        if node is not None:
            node.value += value

    def add_to_next(self, value: int):
        node = self
        while node.parent is not None and node.parent.right == node:
            node = node.parent

        if node is None or node.parent is None:
            return

        node = node.parent.right
        while node is not None and node.left is not None:
            node = node.left

        if node is not None:
            node.value += value

    def explode(self):
        self.add_to_prev(self.left.value)
        self.add_to_next(self.right.value)
        self.left.parent = None
        self.right.parent = None
        self.left = None
        self.right = None
        self.value = 0

    def split(self):
        self.left = self.value_node(self.value // 2, self)
        self.right = self.value_node((self.value + 1) // 2, self)
        self.value = None

    def explodable(self) -> Iterator['Node']:
        for node, depth in self:
            if node.is_pair_node and node.left.is_value_node and node.right.is_value_node and depth >= 4:
                yield node

    def splittable(self) -> Iterator['Node']:
        for node, depth in self:
            if node.is_value_node and node.value >= 10:
                yield node

    def reduce_step(self) -> bool:
        for node in self.explodable():
            node.explode()
            return True

        for node in self.splittable():
            node.split()
            return True

        return False

    def reduce(self):
        while self.reduce_step():
            pass

    def dfs(self, depth: int):
        if self.is_pair_node:
            yield from self.left.dfs(depth + 1)
            yield from self.right.dfs(depth + 1)
        yield self, depth

    def __add__(self, other: 'Node') -> 'Node':
        node = self.pair_node(self, other)
        node.reduce()
        return node

    def __deepcopy__(self, _unused) -> 'Node':
        if self.is_value_node:
            return self.value_node(self.value)
        else:
            return self.pair_node(copy.deepcopy(self.left), copy.deepcopy(self.right))

    def __iter__(self) -> Iterator[Tuple['Node', int]]:
        return self.dfs(0)

    def __str__(self) -> str:
        if self.is_value_node:
            return str(self.value)
        else:
            return f'[{self.left},{self.right}]'


def find_comma(s: str) -> int:
    depth = 0
    for i, c in enumerate(s):
        if c == '[':
            depth += 1
        if c == ']':
            depth -= 1
        if c == ',' and depth == 1:
            return i
    return -1


def parse_node(s: str, parent: Optional[Node] = None) -> Node:
    if s.isnumeric():
        node = Node.value_node(int(s))
        node.parent = parent
        return node
    else:
        i = find_comma(s)
        return Node.pair_node(parse_node(s[1:i]), parse_node(s[i + 1:-1]), parent)


def read_input() -> List[Node]:
    with open('input.txt', 'r') as reader:
        return [parse_node(line.strip()) for line in reader.readlines()]


def task1(nodes: List[Node]) -> int:
    return functools.reduce(operator.add, copy.deepcopy(nodes)).magnitude


def task2(nodes: List[Node]) -> int:
    answer = 0
    for i, node1 in enumerate(nodes):
        for j, node2 in enumerate(nodes):
            if i == j:
                continue
            left = copy.deepcopy(node1)
            right = copy.deepcopy(node2)
            answer = max(answer, (left + right).magnitude)
    return answer


if __name__ == '__main__':
    nodes = read_input()
    print(task1(nodes))
    print(task2(nodes))
