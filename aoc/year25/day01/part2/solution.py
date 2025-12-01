import dataclasses

from aoc import helpers
from aoc.year25.day01.part1 import solution as p1


@dataclasses.dataclass
class State:
    count: int
    pos: int

    def apply(self, num: int) -> None:
        new_virtual_pos = self.pos + num

        if new_virtual_pos <= 0:
            if self.pos > 0:
                self.count += 1
            self.count += -new_virtual_pos // 100

        if new_virtual_pos >= 100:
            self.count += new_virtual_pos // 100

        self.pos = new_virtual_pos % 100


def solution(lines: list[str]):
    nums = p1.parse_lines(lines)

    state = State(count=0, pos=50)
    for num in nums:
        state.apply(num)

    return state.count


if __name__ == '__main__':
    helpers.run_solution(solution)
