import itertools

from aoc import helpers


def parse_reports(lines: list[str]):
    return [list(map(int, line.split())) for line in lines]


def is_monotonic(report: list[int]):
    return all(l1 <= l2 for l1, l2 in itertools.pairwise(report)) or all(
        l1 >= l2 for l1, l2 in itertools.pairwise(report)
    )


def is_speed_between(report: list[int], min: int, max: int):
    return all(min <= abs(l1 - l2) <= max for (l1, l2) in itertools.pairwise(report))


def is_report_safe(report: list[int]):
    return is_monotonic(report) and is_speed_between(report, 1, 3)


def solution(lines: list[str]):
    return sum(is_report_safe(report) for report in parse_reports(lines))


if __name__ == '__main__':
    helpers.run_solution(solution)
