import collections
import dataclasses
from typing import List, Tuple, Iterable, Set, Dict

import numpy as np


@dataclasses.dataclass
class Formula:
    formula: str

    @property
    def first(self) -> str:
        return self.formula[0]

    @property
    def last(self) -> str:
        return self.formula[-1]

    @property
    def pairs(self) -> List[Tuple[str, str]]:
        return [(self.formula[i], self.formula[i + 1]) for i in range(len(self.formula) - 1)]


@dataclasses.dataclass
class Insertion:
    left: str
    middle: str
    right: str

    def removed_pair(self) -> Tuple[str, str]:
        return self.left, self.right

    def inserted_pairs(self) -> Iterable[Tuple[str, str]]:
        return (self.left, self.middle), (self.middle, self.right)


def parse_insertion(line: str) -> Insertion:
    between, inserted = line.split(' -> ')
    return Insertion(between[0], inserted, between[1])


def read_input() -> Tuple[Formula, List[Insertion]]:
    with open('input.txt', 'r') as reader:
        it = iter(reader)
        formula = Formula(next(it).strip())
        insertions = [parse_insertion(line) for line in map(str.strip, it) if line]
        return formula, insertions


def all_pairs(formula: Formula, insertions: List[Insertion]) -> Set[Tuple[str, str]]:
    pairs = set(formula.pairs)
    for insertion in insertions:
        pairs.update(insertion.inserted_pairs())
        pairs.add(insertion.removed_pair())
    return pairs


def get_transition_matrix(insertions: List[Insertion], pair_to_index: Dict[Tuple[str, str], int]) -> np.matrix:
    n = len(pair_to_index)
    transitions = [[0] * n for _ in range(n)]

    # without any insertions, all pairs should be carried into the next step
    for i in range(n):
        transitions[i][i] = 1

    for insertion in insertions:
        # for each insertion, removed pair is... removed
        removed_pair_index = pair_to_index[insertion.removed_pair()]
        transitions[removed_pair_index][removed_pair_index] -= 1

        # for each insertion, inserted pairs are... inserted
        for inserted_pair in insertion.inserted_pairs():
            inserted_pair_index = pair_to_index[inserted_pair]
            transitions[inserted_pair_index][removed_pair_index] += 1

    return np.matrix(transitions, dtype='int64')


def get_initial_state_matrix(formula: Formula, pair_to_index: Dict[Tuple[str, str], int]) -> np.matrix:
    n = len(pair_to_index)
    initial_column_vector = [[0] for _ in range(n)]

    for pair in formula.pairs:
        initial_column_vector[pair_to_index[pair]][0] += 1

    return np.matrix(initial_column_vector, dtype='int64')


def to_elements_count(formula: Formula, pairs_count: Dict[Tuple[str, str], int]) -> Dict[str, int]:
    element_count = collections.Counter({formula.first: 1, formula.last: 1})
    for (left, right), pair_count in pairs_count.items():
        element_count[left] += pair_count
        element_count[right] += pair_count
    for element in element_count:
        element_count[element] //= 2
    return element_count


def task(formula: Formula, insertions: List[Insertion], steps: int) -> int:
    pairs = sorted(all_pairs(formula, insertions))

    n = len(pairs)
    pair_to_index = {pair: i for i, pair in enumerate(pairs)}
    index_to_pair = {i: pair for i, pair in enumerate(pairs)}

    transition_matrix = get_transition_matrix(insertions, pair_to_index)
    initial_state_matrix = get_initial_state_matrix(formula, pair_to_index)

    final_state_matrix = (transition_matrix ** steps * initial_state_matrix).tolist()
    pairs_count = {index_to_pair[index]: final_state_matrix[index][0] for index in range(n)}
    elements_count = to_elements_count(formula, pairs_count)

    return max(elements_count.values()) - min(elements_count.values())


if __name__ == '__main__':
    formula, insertions = read_input()
    print(task(formula, insertions, 10))
    print(task(formula, insertions, 40))
