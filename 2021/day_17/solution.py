import abc
import dataclasses
import re
from typing import Iterator, Tuple

INPUT_RE = re.compile(r'^target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)\n$')


def read_input():
    with open('input.txt', 'r') as reader:
        line = reader.readline()
        x1, x2, y1, y2 = INPUT_RE.fullmatch(line).groups()
        return int(x1), int(x2), int(y1), int(y2)


@dataclasses.dataclass
class Range:
    min: int
    max: int

    def __contains__(self, pos: int) -> bool:
        return self.min <= pos <= self.max


class Trajectory(abc.ABC):
    """ Returns all positions and velocities that are part of this trajectory. """
    @abc.abstractmethod
    def __iter__(self) -> Iterator[Tuple[int, int]]:
        pass

    """ True if any position is between the given range. """
    @abc.abstractmethod
    def passes_through_range(self, position_range: Range) -> bool:
        pass


class TrajectoryWithAcceleration(Trajectory):
    def __init__(self, starting_position: int, starting_velocity: int, acceleration: int):
        self.starting_position = starting_position
        self.starting_velocity = starting_velocity
        self.acceleration = acceleration

    def __iter__(self) -> Iterator[Tuple[int, int]]:
        position = self.starting_position
        velocity = self.starting_velocity

        while True:
            yield position, velocity
            position += velocity
            velocity += self.acceleration

    def passes_through_range(self, position_range: Range) -> bool:
        for position, velocity in self:
            if position < position_range.min and velocity < 0 and self.acceleration < 0:
                break
            if position > position_range.max and velocity > 0 and self.acceleration > 0:
                break
            if position in position_range:
                return True
        return False


class TrajectoryWithDrag(Trajectory):
    def __init__(self, starting_position: int, starting_velocity: int):
        self.starting_position = starting_position
        self.starting_velocity = starting_velocity

    @classmethod
    def drag(cls, velocity: int) -> int:
        return 0 if velocity == 0 else (+1 if velocity < 0 else -1)

    def __iter__(self) -> Iterator[Tuple[int, int]]:
        position = self.starting_position
        velocity = self.starting_velocity

        while True:
            yield position, velocity
            position += velocity
            velocity += self.drag(velocity)

    def passes_through_range(self, position_range: Range) -> bool:
        for position, velocity in self:
            if velocity == 0:
                break
            if position in position_range:
                return True
        return False


class ProbeTrajectory:
    def __init__(self, x_trajectory: TrajectoryWithDrag, y_trajectory: TrajectoryWithAcceleration):
        self.x_trajectory = x_trajectory
        self.y_trajectory = y_trajectory

    def passes_through_area(self, x_range: Range, y_range: Range) -> bool:
        for (x_position, _), (y_position, y_velocity) in zip(self.x_trajectory, self.y_trajectory):
            if y_position < y_range.min and y_velocity < 0 and self.y_trajectory.acceleration < 0:
                break
            if y_position > y_range.max and y_velocity > 0 and self.y_trajectory.acceleration > 0:
                break
            if x_position in x_range and y_position in y_range:
                return True
        return False


def task1(range_y: Range) -> int:
    start_velocity = -range_y.min - 1
    return start_velocity * (start_velocity + 1) // 2


def task2(range_x: Range, range_y: Range) -> int:
    min_x_velocity = 0
    max_x_velocity = range_x.max
    x_trajectories = set()

    for x_velocity in range(min_x_velocity, max_x_velocity + 1):
        trajectory = TrajectoryWithDrag(0, x_velocity)
        if trajectory.passes_through_range(x_range):
            x_trajectories.add(trajectory)

    min_y_velocity = range_y.min
    max_y_velocity = -range_y.min - 1
    y_trajectories = set()

    for y_velocity in range(min_y_velocity, max_y_velocity + 1):
        trajectory = TrajectoryWithAcceleration(0, y_velocity, -1)
        if trajectory.passes_through_range(y_range):
            y_trajectories.add(trajectory)

    valid_probe_trajectories = 0

    for x_trajectory in x_trajectories:
        for y_trajectory in y_trajectories:
            probe_trajectory = ProbeTrajectory(x_trajectory, y_trajectory)
            if probe_trajectory.passes_through_area(x_range, y_range):
                valid_probe_trajectories += 1

    return valid_probe_trajectories


if __name__ == '__main__':
    x1, x2, y1, y2 = read_input()
    x_range = Range(x1, x2)
    y_range = Range(y1, y2)
    print(task1(y_range))
    print(task2(x_range, y_range))
