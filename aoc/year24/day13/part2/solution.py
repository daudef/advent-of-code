from aoc import helpers
from aoc.lib import Delta
from aoc.year24.day13.part1 import solution as p1


def update_problem(problem: p1.Problem):
    problem.prize += 10000000000000 * Delta(1, 1)
    return problem


def solution(lines: list[str]):
    problems = p1.parse_problems(lines)

    return sum(
        p1.get_solution_cost(solution)
        for problem in problems
        if (solution := p1.solve_problem(update_problem(problem))) is not None
    )


if __name__ == '__main__':
    helpers.run_solution(solution)
