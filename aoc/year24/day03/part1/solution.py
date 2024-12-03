import contextlib

from aoc import helpers


def gen_words(line: str, word: str):
    n = len(line)
    k = len(word)
    for i in range(n - k + 1):
        if line[i : i + k] == word:
            yield range(i, i + k)


def find_par_inside(line: str, i: int):
    if line[i] != '(':
        return None
    count = 0
    for j in range(i, len(line)):
        c = line[j]
        if c == '(':
            count += 1
        if c == ')':
            count -= 1
            if count == 0:
                return range(i + 1, j)
    return None


def handle_mul(args: list[int]):
    if len(args) == 2:
        a, b = args
        if 0 <= a < 1000 and 0 <= b < 1000:
            return a * b
    return 0


def get_int_args(line: str, args_range: range):
    inside = line[args_range.start : args_range.stop]
    if len(inside) == 0:
        return list[int]()
    raw_args = inside.split(',')
    with contextlib.suppress(ValueError):
        return list(map(int, raw_args))


def gen_line_scores(line: str):
    for word_range in gen_words(line, 'mul'):
        inside_range = find_par_inside(line, word_range.stop)
        if inside_range is None:
            continue

        args = get_int_args(line, inside_range)
        if args is not None:
            yield handle_mul(args)


def solution(lines: list[str]):
    return sum(sum(gen_line_scores(line)) for line in lines)


if __name__ == '__main__':
    helpers.run_solution(solution)
