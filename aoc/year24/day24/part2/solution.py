from aoc import helpers
from aoc.year24.day24.part1 import solution as p1  # pyright: ignore[reportUnusedImport]


def export_dot_graph(input: p1.Input):
    return (
        'digraph G {'
        + ' '.join(
            arrow
            for i, operation in enumerate(input.operations)
            for op_name in [f'"{operation.op.name}-{i}"']
            for arrow in [
                f'"{operation.left}" -> {op_name};',
                f'"{operation.right}" -> {op_name};',
                f'{op_name} -> "{operation.res}";',
            ]
        )
        + '}'
    )


def solution(lines: list[str]):
    input = p1.parse_input(lines)
    print(export_dot_graph(input))
    return 0


if __name__ == '__main__':
    helpers.run_solution(solution)
