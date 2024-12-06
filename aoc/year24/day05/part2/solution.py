import collections

import graphlib

from aoc import helpers
from aoc.year24.day05.part1 import solution as p1


def fix_invalid_update(pages: list[int], input: p1.Input):
    if p1.get_invalid_rule(pages, input) is None:
        return None

    used_pages = set(pages)

    transitions: dict[int, set[int]] = collections.defaultdict(set)
    for a, b in input.ordering_rules:
        if a in used_pages and b in used_pages:
            transitions[b].add(a)

    page_order_map = {
        p: i for i, p in enumerate(graphlib.TopologicalSorter(transitions).static_order())
    }

    return sorted(pages, key=page_order_map.__getitem__)


def solution(lines: list[str]):
    input = p1.parse_input(lines)

    return sum(
        p1.get_middle_page(fixed_update)
        for update in input.updates
        if (fixed_update := fix_invalid_update(update, input)) is not None
    )


if __name__ == '__main__':
    helpers.run_solution(solution)
