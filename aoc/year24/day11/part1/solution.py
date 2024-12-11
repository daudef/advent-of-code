import typing

from aoc import helpers


def evolve_stone(v: int):
    if v == 0:
        return [1]
    digits = str(v)
    digit_count = len(digits)
    mid_digit_index = digit_count // 2
    if 2 * mid_digit_index == digit_count:
        return [int(digits[:mid_digit_index]), int(digits[mid_digit_index:])]

    return [v * 2024]


Cache: typing.TypeAlias = dict[tuple[int, int], int]


def get_stone_count(value: int, n_blink: int, cache: Cache) -> int:
    if n_blink == 0:
        return 1

    cache_key = (value, n_blink)
    if (count := cache.get(cache_key)) is not None:
        return count

    count = sum(get_stone_count(v, n_blink - 1, cache) for v in evolve_stone(value))
    cache[cache_key] = count
    return count


# def evolve_stones(values: list[int]):
#     return [new_value for value in values for new_value in evolve_stone(value)]


# def repeat_evolve_stones(values: list[int], n: int):
#     for _ in range(n):
#         values = evolve_stones(values)
#     return values


def parse_input(lines: list[str]):
    return [int(e) for e in lines[0].split()]


def solution(lines: list[str]):
    return sum(get_stone_count(v, 25, {}) for v in parse_input(lines))


if __name__ == '__main__':
    helpers.run_solution(solution)
