import dataclasses
import functools
import operator
from typing import List, Optional

HEXADECIMAL_TO_BINARY = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}


def read_input() -> str:
    with open('input.txt', 'r') as reader:
        hexadecimal_transmission = reader.read().strip()
        return ''.join(map(HEXADECIMAL_TO_BINARY.get, hexadecimal_transmission))


LITERAL_VALUE_TYPE = 4


@dataclasses.dataclass
class Packet:
    version: int
    type: int
    literal_value: int
    subpackets: List['Packet']

    @classmethod
    def literal(cls, version: int, value: int,) -> 'Packet':
        return Packet(version, LITERAL_VALUE_TYPE, value, [])

    @classmethod
    def operator(cls, version: int, packet_type: int, subpackets: List['Packet']) -> 'Packet':
        return Packet(version, packet_type, 0, subpackets)

    def version_sum(self) -> int:
        return self.version + sum(subpacket.version_sum() for subpacket in self.subpackets)

    def value(self) -> int:
        if self.type == 0:
            return sum(map(Packet.value, self.subpackets))
        if self.type == 1:
            return functools.reduce(operator.mul, map(Packet.value, self.subpackets))
        if self.type == 2:
            return min(map(Packet.value, self.subpackets))
        if self.type == 3:
            return max(map(Packet.value, self.subpackets))
        if self.type == 4:
            return self.literal_value
        if self.type == 5:
            return 1 if self.subpackets[0].value() > self.subpackets[1].value() else 0
        if self.type == 6:
            return 1 if self.subpackets[0].value() < self.subpackets[1].value() else 0
        if self.type == 7:
            return 1 if self.subpackets[0].value() == self.subpackets[1].value() else 0
        raise RuntimeError()


class Parser:
    def __init__(self, transmission: str):
        self.transmission = transmission
        self.index = 0

    def read_bits(self, length: int) -> int:
        if self.index + length > len(self.transmission):
            raise IndexError()

        value = 0
        indices = range(self.index, self.index + length)
        powers = reversed(range(length))

        for index, power in zip(indices, powers):
            if self.transmission[index] == '1':
                value += (1 << power)

        self.index += length

        return value

    def read_str(self, length: int) -> str:
        if self.index + length > len(self.transmission):
            raise IndexError()

        value = self.transmission[self.index: self.index + length]
        self.index += length
        return value

    def read_packets(self, count: Optional[int] = None) -> List[Packet]:
        i = 0
        packets = []

        while self.index < len(self.transmission):
            packets.append(self.read_packet())
            i += 1
            if count is not None and i == count:
                break

        return packets

    def read_packet(self) -> Packet:
        version = self.read_bits(3)
        packet_type = self.read_bits(3)

        if packet_type == LITERAL_VALUE_TYPE:
            value = self.read_literal()
            return Packet.literal(version, value)

        mode = self.read_bits(1)

        if mode == 0:
            length = self.read_bits(15)
            data = self.read_str(length)
            subpackets = Parser(data).read_packets()
            return Packet.operator(version, packet_type, subpackets)
        else:
            count = self.read_bits(11)
            subpackets = self.read_packets(count)
            return Packet.operator(version, packet_type, subpackets)

    def read_literal(self) -> int:
        value = 0

        while True:
            group_type = self.read_bits(1)
            group_value = self.read_bits(4)
            value = (value << 4) ^ group_value
            if group_type == 0:
                break

        return value


def task1(transmission: str) -> int:
    return Parser(transmission).read_packet().version_sum()


def task2(transmission: str) -> int:
    return Parser(transmission).read_packet().value()


if __name__ == '__main__':
    transmission = read_input()
    print(task1(transmission))
    print(task2(transmission))
