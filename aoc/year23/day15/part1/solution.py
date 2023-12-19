from aoc import helpers


def hash(s: str):
    res = 0
    for c in s:
        res += ord(c)
        res *= 17
        res %= 256
    return res


def parse_values(input: list[str]):
    return input[0].split(',')


def solution(input: list[str]):
    return sum(hash(v) for v in parse_values(input))


if __name__ == '__main__':
    helpers.run_solution(solution)
