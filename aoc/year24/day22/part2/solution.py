import typing
from collections import defaultdict

from aoc import helpers
from aoc.year24.day22.part1 import solution as p1

Sequence: typing.TypeAlias = tuple[int, int, int, int]


def get_sequence_score_map(secret: int):
    sequence_score_map: dict[Sequence, int] = defaultdict(int)
    changes: list[int] = []
    banana = secret % 10
    for _ in range(2000):
        new_secret = p1.apply_step(secret)
        new_banana = new_secret % 10
        changes.append(new_banana - banana)
        if len(changes) >= 4:
            sequence = (changes[-4], changes[-3], changes[-2], changes[-1])
            if sequence not in sequence_score_map:
                sequence_score_map[sequence] = new_banana
        secret = new_secret
        banana = new_banana
    return sequence_score_map


def merge_sequence_score_map(map1: dict[Sequence, int], map2: dict[Sequence, int]):
    return {seq: map1.get(seq, 0) + map2.get(seq, 0) for seq in map1 | map2}


def solution(lines: list[str]):
    merged_sequence_score_map: dict[Sequence, int] = {}
    for line in lines:
        sequence_score_map = get_sequence_score_map(int(line))
        merged_sequence_score_map = merge_sequence_score_map(
            merged_sequence_score_map, sequence_score_map
        )

    return max(merged_sequence_score_map.values())


if __name__ == '__main__':
    helpers.run_solution(solution)
