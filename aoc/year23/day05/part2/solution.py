import dataclasses
import typing
from aoc import helpers


@dataclasses.dataclass(frozen=True)
class Value:
    start: int
    end: int


@dataclasses.dataclass
class Map:
    source_name: str
    target_name: str

    ranges: list[tuple[int, int, int]]

    def apply(self, i: Value) -> typing.Iterator[Value]:
        values = {i}

        for t, s, le in self.ranges:
            new_values: set[Value] = set()
            for value in values:
                start_inter = max(s, value.start)
                end_inter = min(s + le, value.end)
                if start_inter < end_inter:
                    yield Value(start_inter - s + t, end_inter - s + t)
                    if s > value.start:
                        new_values.add(Value(value.start, s))
                    if s + le < value.end:
                        new_values.add(Value(s + le + 1, value.end))
                else:
                    new_values.add(value)
            value = new_values

        yield from values

    def update_with_line(self, line: str):
        a, b, c = map(int, line.split())
        self.ranges.append((a, b, c))


@dataclasses.dataclass
class Input:
    init_name: str
    init_values: list[Value]
    maps: list[Map]


def parse_input(lines: list[str]):
    input = Input(init_name='', init_values=[], maps=[])
    for line in lines:
        if ':' in line:
            if 'map' in line:
                map_name, _, _ = line.partition('map:')
                source_name, _, target_name = map_name.partition('-to-')
                input.maps.append(
                    Map(source_name=source_name.strip(), target_name=target_name.strip(), ranges=[])
                )
            else:
                init_name, values = line.split(':')
                input.init_name = init_name.strip()

                raw_values = values.split()
                for i in range(0, len(raw_values), 2):
                    a, b = map(int, raw_values[i : i + 2])
                    input.init_values.append(Value(a, a + b))

        else:
            if line.strip() != '':
                input.maps[-1].update_with_line(line)
    return input


def apply(values: list[Value], map: Map):
    return [mv for v in values for mv in map.apply(v)]


def solution(input: list[str]):
    pinput = parse_input(input)
    name = pinput.init_name[:-1]
    values = pinput.init_values
    while name != 'location':
        for map in pinput.maps:
            if map.source_name == name:
                break
        else:
            raise RuntimeError
        values = apply(values, map)
        name = map.target_name
    return min(v.start for v in values)


if __name__ == '__main__':
    helpers.run_solution(solution)
