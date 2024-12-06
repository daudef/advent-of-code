import dataclasses

from aoc import helpers


@dataclasses.dataclass
class Input:
    ordering_rules: list[tuple[int, int]]
    updates: list[list[int]]


def parse_input(lines: list[str]):
    input = Input(ordering_rules=[], updates=[])
    line_it = iter(lines)
    for line in line_it:
        if len(line) == 0:
            break

        a, b = line.split('|')
        input.ordering_rules.append((int(a), int(b)))

    for line in line_it:
        pages = line.split(',')
        input.updates.append(list(map(int, pages)))

    return input


def get_invalid_rule(pages: list[int], input: Input):
    page_index_map = {p: i for i, p in enumerate(pages)}
    for p1, p2 in input.ordering_rules:
        if (i1 := page_index_map.get(p1)) is not None and (
            i2 := page_index_map.get(p2)
        ) is not None:
            if i1 > i2:
                return p1, p2
    return None


def get_middle_page(pages: list[int]):
    mid = len(pages) // 2
    assert 2 * mid + 1 == len(pages)
    return pages[mid]


def solution(lines: list[str]):
    input = parse_input(lines)

    return sum(
        get_middle_page(update)
        for update in input.updates
        if get_invalid_rule(update, input) is None
    )


if __name__ == '__main__':
    helpers.run_solution(solution)
