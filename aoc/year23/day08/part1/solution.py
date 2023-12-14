import dataclasses
from aoc import helpers


@dataclasses.dataclass(frozen=True)
class State:
    label: str
    index: int


@dataclasses.dataclass
class Instructions:
    transitions: dict[State, State]
    labels: set[str]

    def run(self, start: str):
        current = State(start, 0)
        while True:
            yield current
            current = self.transitions[current]


def parse(lines: list[str]):
    move_to_rights = [True if c == 'R' else False for c in lines[0].strip()]

    instructions = Instructions(transitions={}, labels=set())
    map: dict[str, tuple[str, str]] = {}
    for line in lines[1:]:
        if len(line.strip()) > 0:
            k, vs = line.split('=')
            v1, v2 = vs.split(',')
            map[k.strip()] = (v1.strip()[1:], v2.strip()[:-1])

    for k, (v1, v2) in map.items():
        instructions.labels.add(k)
        for i, move_to_right in enumerate(move_to_rights):
            instructions.transitions[State(k, i)] = State(
                v2 if move_to_right else v1, (i + 1) % len(move_to_rights)
            )

    return instructions


def solution(input: list[str]):
    trans = parse(input)
    for i, v in enumerate(trans.run('AAA')):
        if v.label == 'ZZZ':
            return i
    return 0


if __name__ == '__main__':
    helpers.run_solution(solution)
