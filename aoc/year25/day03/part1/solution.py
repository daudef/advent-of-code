from aoc import helpers


def parse_lines(lines: list[str]):
    return [[int(c) for c in line] for line in lines]


def find_best_joltage(bank: list[int], digit_count: int):
    digits: list[int] = []
    start_index = 0
    for _ in range(digit_count):
        index, digit = max(
            list(enumerate(bank))[start_index : len(bank) + 1 - digit_count + len(digits)],
            key=lambda t: (t[1], -t[0]),
        )
        start_index = index + 1
        digits.append(digit)

    return int(''.join(map(str, digits)))


def solution(lines: list[str]):
    return sum(find_best_joltage(bank, 2) for bank in parse_lines(lines))


if __name__ == '__main__':
    helpers.run_solution(solution)
