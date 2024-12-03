from aoc import helpers
from aoc.year24.day03.part1 import solution as p1  # pyright: ignore[reportUnusedImport]


def gen_line_scores(line: str):
    enabled = True

    for word_range in sorted(
        [*p1.gen_words(line, 'mul'), *p1.gen_words(line, 'do'), *p1.gen_words(line, "don't")],
        key=lambda r: r.start,
    ):
        word = line[word_range.start : word_range.stop]
        inside_range = p1.find_par_inside(line, word_range.stop)
        if inside_range is None:
            continue
        args = p1.get_int_args(line, inside_range)
        if args is None:
            continue

        if word == 'do':
            enabled = True
        if word == "don't":
            enabled = False
        if word == 'mul' and enabled:
            yield p1.handle_mul(args)


def solution(lines: list[str]):
    return sum(gen_line_scores(' '.join(lines)))


if __name__ == '__main__':
    helpers.run_solution(solution)
