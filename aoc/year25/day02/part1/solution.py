from aoc import helpers


def parse_lines(lines: list[str]) -> list[range]:
    return [
        range(int(start), int(stop) + 1)
        for line in lines
        for range_str in line.split(',')
        if range_str
        for (start, _, stop) in [range_str.partition('-')]
    ]


def is_invalid_id(id: int, pattern_count: int):
    s = str(id)
    n = len(s)
    if n % pattern_count != 0:
        return False
    pattern = s[: n // pattern_count]

    return all(
        s[(i + 1) * len(pattern) : (i + 2) * len(pattern)] == pattern
        for i in range(pattern_count - 1)
    )


def get_invalid_ids_in_range(r: range, pattern_count: int):
    return (i for i in r if is_invalid_id(i, pattern_count))


def solution(lines: list[str]):
    return sum(sum(get_invalid_ids_in_range(r, 2)) for r in parse_lines(lines))


if __name__ == '__main__':
    helpers.run_solution(solution)
