from aoc import helpers
from aoc.year24.day17.part1 import solution as p1


def solution_rec(a: int, i: int, input: p1.Input) -> int | None:
    for a_candidate in range(a << 3, (a << 3) + 8):
        if a_candidate == 0:
            continue
        state = p1.State(a=a_candidate, b=0, c=0, program=input.program[:14], pc=0, output=[])
        p1.run(state)
        if state.output[0] == input.program[i]:
            if i == 0:
                return a_candidate
            solution = solution_rec(a_candidate, i - 1, input)
            if solution is not None:
                return solution
    return None


def solution(lines: list[str]):
    input = p1.parse_input(lines)
    solution = solution_rec(0, 15, input)
    assert solution is not None

    state = p1.make_state(input)
    state.a = solution
    p1.run(state)
    assert state.output == input.program, state.output

    return solution


if __name__ == '__main__':
    helpers.run_solution(solution)
