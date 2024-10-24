from aoc import helpers
from aoc.year23.day05.part1 import solution as part1


def solution(input: list[str]):
    pinput = part1.parse_input(input)
    name = pinput.init_name[:-1]

    assert 2 * (len(pinput.init_values) // 2) == len(pinput.init_values)
    values: list[range] = []
    for i in range(len(pinput.init_values) // 2):
        values.append(
            range(
                pinput.init_values[2 * i], pinput.init_values[2 * i] + pinput.init_values[2 * i + 1]
            )
        )

    while name != 'location':
        map = pinput.src_name_map_map[name]
        values = part1.apply(values, map)
        name = map.dst_name
    return min(v.start for v in values)


if __name__ == '__main__':
    helpers.run_solution(solution)
