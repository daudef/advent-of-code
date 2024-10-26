import dataclasses
import functools
import itertools

from aoc import helpers
from aoc.year23.day15.part1 import solution as sol1  # pyright: ignore[reportUnusedImport]


@dataclasses.dataclass
class Lens:
    label: str
    focal_length: int

    def __str__(self):
        return f'[{self.label} {self.focal_length}]'


@dataclasses.dataclass
class Box:
    lenses: list[Lens] = dataclasses.field(default_factory=list)


@dataclasses.dataclass(frozen=True)
class DashOperation:
    def apply(self, box: Box, label: str):
        box.lenses = [lens for lens in box.lenses if lens.label != label]

    def __str__(self):
        return '-'


@dataclasses.dataclass(frozen=True)
class EqualOperation:
    focal_length: int

    def apply(self, box: Box, label: str):
        for lens in box.lenses:
            if lens.label == label:
                lens.focal_length = self.focal_length
                return
        box.lenses.append(Lens(label=label, focal_length=self.focal_length))

    def __str__(self):
        return f'={self.focal_length}'


def parse_operation(s: str):
    match [s[:1], s[1:]]:
        case ['=', focal_length]:
            return EqualOperation(focal_length=int(focal_length))
        case ['-', '']:
            return DashOperation()
        case _:
            raise RuntimeError(f'invalid operation: {s}')


@dataclasses.dataclass(frozen=True)
class Step:
    label: str
    operation: DashOperation | EqualOperation

    @staticmethod
    def parse(s: str):
        label = ''.join(itertools.takewhile(str.isalpha, s))
        return Step(label, parse_operation(s.removeprefix(label)))

    @functools.cached_property
    def box_index(self):
        return sol1.hash(self.label)

    def apply(self, boxes: list[Box]):
        self.operation.apply(box=boxes[self.box_index], label=self.label)

    def __str__(self) -> str:
        return f'{self.label}{self.operation}'


def parse_steps(s: str):
    return [Step.parse(e) for e in s.split(',')]


def compute_focusing_power(boxes: list[Box]):
    return sum(
        (box_index + 1) * (lens_index + 1) * lens.focal_length
        for box_index, box in enumerate(boxes)
        for lens_index, lens in enumerate(box.lenses)
    )


def display_step(step: Step, boxes: list[Box]):
    print(f'After "{step}" (box {step.box_index}):')
    for box_index, box in enumerate(boxes):
        if len(box.lenses) > 0:
            print(f'Box {box_index}: {' '.join(map(str, box.lenses))}')
    print('')


def solution(input: list[str]):
    steps = parse_steps(input[0])
    boxes = [Box() for _ in range(256)]

    for step in steps:
        step.apply(boxes)

        # display_step(step, boxes)

    return compute_focusing_power(boxes)


if __name__ == '__main__':
    helpers.run_solution(solution)
