import dataclasses
import functools
import itertools
from typing import List, Iterator, Tuple, Set, Union


@dataclasses.dataclass(eq=True, frozen=True)
class Instruction:
    operation: str
    args: Tuple[str, ...]


@dataclasses.dataclass(eq=True, frozen=True)
class Block:
    instructions: Tuple[Instruction]

    def __iter__(self) -> Iterator[Instruction]:
        return iter(self.instructions)

    def process(self, z: int, w: int) -> int:
        a, b = self._coefficients(z % 26, w)
        return a * (z // self._div) + b

    def unprocess(self, z: Union[int, Set[int]], w: int = None) -> Set[int]:
        zs = {z} if isinstance(z, int) else z
        ws = range(1, 10) if w is None else (w,)
        result = set()

        for z, w, mod in itertools.product(zs, ws, range(26)):
            a, b = self._coefficients(mod, w)
            if (z - b) % a != 0:
                continue
            if self._div == 1 and ((z - b) // a) % 26 == mod:
                result.add((z - b) // a)
            if self._div == 26:
                result.add((z - b) // a * self._div + mod)

        return result

    def _process(self, z: int, w: int) -> int:
        vars = {'x': 0, 'y': 0, 'z': z, 'w': w}

        for instruction in self:
            a, b = instruction.args
            b = vars[b] if b in vars else int(b)
            vars[a] = OPERATION[instruction.operation](vars[a], b)

        return vars['z']

    @functools.cached_property
    def _div(self) -> int:
        for instruction in self:
            if instruction.operation == 'div' and instruction.args[0] == 'z':
                return int(instruction.args[1])

    @functools.lru_cache(maxsize=26 * 9)
    def _coefficients(self, z: int, w: int) -> Tuple[int, int]:
        z1, z2 = z, z + 26
        r1 = self._process(z1, w)
        r2 = self._process(z2, w)
        a, b = linear_fit(z1 // self._div, r1, z2 // self._div, r2)
        return a, b


def parse_instruction(instruction: str) -> Instruction:
    tokens = instruction.split()
    return Instruction(tokens[0], tuple(tokens[1:]))


def parse_block(block: str) -> Block:
    return Block(tuple(parse_instruction(instruction.strip()) for instruction in block.splitlines()))


def read_input() -> List[Block]:
    with open('input.txt', 'r') as reader:
        return [parse_block(block) for block in reader.read().split('inp w\n') if block]


# a * x1 + b = y1
# a * x2 + b = y2
def linear_fit(x1: int, y1: int, x2: int, y2: int) -> Tuple[int, int]:
    a = (y1 - y2) // (x1 - x2)
    b = y1 - a * x1
    return a, b


OPERATION = {
    'add': lambda a, b: a + b,
    'mul': lambda a, b: a * b,
    'div': lambda a, b: a // b,
    'mod': lambda a, b: a % b,
    'eql': lambda a, b: 1 if a == b else 0
}


class Solution:
    def __init__(self, blocks: List[Block]):
        self.blocks = blocks

        allowed = [{0}]
        for block in reversed(blocks):
            allowed.append(block.unprocess(allowed[-1]))
        self.allowed = allowed[-2:: -1]

    def pow(self, i: int) -> int:
        return pow(10, len(self.blocks) - i - 1)

    def min(self) -> int:
        return self._solve(list(range(1, 10)))

    def max(self) -> int:
        return self._solve(list(range(9, 0, -1)))

    def _solve(self, digits: List[int]) -> int:
        z = 0
        answer = 0

        for i, (block, allowed) in enumerate(zip(self.blocks, self.allowed)):
            for d in digits:
                z1 = block.process(z, d)
                if z1 in allowed:
                    z = z1
                    answer += d * self.pow(i)
                    break

        return answer


if __name__ == '__main__':
    blocks = read_input()
    solution = Solution(blocks)
    print(solution.max())
    print(solution.min())
