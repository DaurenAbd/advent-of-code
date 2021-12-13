import collections
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple


def read_line(line: str) -> Tuple[str, str]:
    start, end = line.strip().split('-')
    return start, end


def read_input() -> List[Tuple[str, str]]:
    with open('input.txt', 'r') as reader:
        return [read_line(line) for line in reader.readlines()]


@dataclass(eq=True, frozen=True)
class Cave:
    name: str
    id: int

    @classmethod
    def is_small_cave_name(cls, cave_name: str) -> bool:
        return cave_name not in ('start', 'end') and cave_name.islower()

    @classmethod
    def from_cave_names(cls, cave_names: Iterable[str]) -> Dict[str, 'Cave']:
        small_cave_names = filter(lambda cave_name: cls.is_small_cave_name(cave_name), cave_names)
        other_cave_names = filter(lambda cave_name: not cls.is_small_cave_name(cave_name), cave_names)
        small_caves = {
            cave_name: Cave(cave_name, cave_id)
            for cave_id, cave_name in enumerate(small_cave_names)
        }
        other_caves = {
            cave_name: Cave(cave_name, cave_id)
            for cave_id, cave_name in enumerate(other_cave_names, len(small_caves))
        }
        return dict(**small_caves, **other_caves)

    def is_start(self):
        return self.name == 'start'

    def is_small(self):
        return self.is_small_cave_name(self.name)


class State:
    allow_two_visits_for_single_small_cave: bool
    visits: List[Cave]
    visit_count: Dict[Cave, int]
    twice_visited_small_cave: Optional[Cave]
    hash: Tuple[int, ...]

    def __init__(self, start_cave: Cave, allow_two_visits: bool):
        self.allow_two_visits_for_single_small_cave = allow_two_visits
        self.visits = [start_cave]
        self.visit_count = collections.Counter({start_cave: 1})
        self.twice_visited_small_cave = None
        self.hash = (0, start_cave.id)

    @property
    def last(self):
        return self.visits[-1]

    def update_hash(self, extra_hash: int = 0):
        if self.twice_visited_small_cave is None:
            self.hash = (self.hash[0] + extra_hash, self.visits[-1].id)
        else:
            self.hash = (self.hash[0] + extra_hash, self.visits[-1].id, self.twice_visited_small_cave.id)

    def is_valid_move(self, cave: Cave) -> bool:
        if self.last == cave or cave.is_start():
            return False
        if cave.is_small():
            if self.visit_count[cave] == 0:
                return True
            if not self.allow_two_visits_for_single_small_cave:
                return False
            if self.visit_count[cave] == 1 and self.twice_visited_small_cave is None:
                return True
            return False
        return True

    def move(self, cave: Cave):
        self.visits.append(cave)
        self.visit_count[cave] += 1
        if cave.is_small():
            if self.visit_count[cave] == 2:
                self.twice_visited_small_cave = cave
            self.update_hash(1 << cave.id)
        else:
            self.update_hash()

    def cancel_move(self):
        cave = self.visits.pop()
        self.visit_count[cave] -= 1
        if cave.is_small():
            if self.visit_count[cave] == 1:
                self.twice_visited_small_cave = None
            self.update_hash(-(1 << cave.id))
        else:
            self.update_hash()


class Graph:
    def __init__(self, edges: List[Tuple[str, str]]):
        cave_names = {cave_name for edge in edges for cave_name in edge}
        caves_by_name = Cave.from_cave_names(cave_names)

        self.graph = collections.defaultdict(list)
        self.start_cave = caves_by_name['start']
        self.end_cave = caves_by_name['end']

        for edge_from, edge_to in edges:
            edge_from_cave = caves_by_name[edge_from]
            edge_to_cave = caves_by_name[edge_to]

            # forbid adding (cave -> start) and (end -> cave) edges
            if edge_from != 'end' and edge_to != 'start':
                self.graph[edge_from_cave].append(edge_to_cave)

            # forbid adding (cave -> start) and (end -> cave) edges
            if edge_to != 'end' and edge_from != 'start':
                self.graph[edge_to_cave].append(edge_from_cave)

        self.mem = {}

    def dfs(self, state: State) -> int:
        if state.hash in self.mem:
            return self.mem[state.hash]

        if state.last == self.end_cave:
            return 1

        paths = 0

        for cave in self.graph[state.last]:
            if not state.is_valid_move(cave):
                continue
            state.move(cave)
            paths += self.dfs(state)
            state.cancel_move()

        self.mem[state.hash] = paths

        return paths

    def count_paths(self, allow_two_visits_for_single_small_cave: bool) -> int:
        self.mem.clear()
        paths = self.dfs(State(self.start_cave, allow_two_visits_for_single_small_cave))
        self.mem.clear()
        return paths


if __name__ == '__main__':
    print(Graph(read_input()).count_paths(allow_two_visits_for_single_small_cave=False))
    print(Graph(read_input()).count_paths(allow_two_visits_for_single_small_cave=True))
