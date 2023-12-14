import dataclasses
from aoc import helpers


@dataclasses.dataclass
class Map:
    source_name: str
    target_name: str

    values: list[tuple[int, int, int]]

    def apply(self, i: int):
        for t, s, le in self.values:
            if s <= i < s + le:
                return i - s + t
        return i

    def update_with_line(self, line: str):
        a, b, c = map(int, line.split())
        self.values.append((a, b, c))


@dataclasses.dataclass
class Input:
    init_name: str
    init_values: list[int]
    maps: list[Map]


def parse_input(lines: list[str]):
    input = Input(init_name='', init_values=[], maps=[])
    for line in lines:
        if ':' in line:
            if 'map' in line:
                map_name, _, _ = line.partition('map:')
                source_name, _, target_name = map_name.partition('-to-')
                input.maps.append(
                    Map(source_name=source_name.strip(), target_name=target_name.strip(), values=[])
                )
            else:
                init_name, values = line.split(':')
                input.init_name = init_name.strip()
                input.init_values = [int(v) for v in values.split()]
        else:
            if line.strip() != '':
                input.maps[-1].update_with_line(line)
    return input


def apply(values: list[int], map: Map):
    return [map.apply(v) for v in values]


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
    return min(values)


if __name__ == '__main__':
    helpers.run_solution(solution)
