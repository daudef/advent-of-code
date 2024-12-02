from aoc import helpers
from aoc.year24.day02.part1 import solution as p1


def is_report_safe(report: list[int]):
    return any(
        p1.is_report_safe([level for j, level in enumerate(report) if j != i])
        for i, _ in enumerate(report)
    )


def solution(lines: list[str]):
    return sum(is_report_safe(report) for report in p1.parse_reports(lines))


if __name__ == '__main__':
    helpers.run_solution(solution)
