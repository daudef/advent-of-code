import dataclasses

from aoc import helpers


@dataclasses.dataclass
class Input:
    block_ids: list[int | None]
    block_ranges: list[range]


def parse_block_ids(line: str):
    input = Input(block_ids=[], block_ranges=[])

    current_id = 0
    is_empty = False
    for c in line:
        value = int(c)
        if is_empty:
            input.block_ids.extend(None for _ in range(value))
        else:
            input.block_ranges.append(range(len(input.block_ids), len(input.block_ids) + value))
            input.block_ids.extend(current_id for _ in range(value))
            current_id += 1
        is_empty = not is_empty
    return input


def move_blocks(block_ids: list[int | None]):
    block_ids = block_ids[:]
    start = 0
    end = len(block_ids) - 1
    while True:
        while start < len(block_ids) and block_ids[start] is not None:
            start += 1
        while end >= 0 and block_ids[end] is None:
            end -= 1
        if start >= end:
            break
        block_ids[start] = block_ids[end]
        block_ids[end] = None
    return block_ids


def compute_checksum(block_ids: list[int | None]):
    return sum(i * id for (i, id) in enumerate(block_ids) if id is not None)


def solution(lines: list[str]):
    return compute_checksum(move_blocks(parse_block_ids(lines[0]).block_ids))


if __name__ == '__main__':
    helpers.run_solution(solution)
