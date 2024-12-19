from aoc import helpers
from aoc.lib import Delta, Pos, djikstra_all
from aoc.year24.day16.part1 import solution as p1


def block_path_rec(blocked: set[Pos], input: p1.Input, tried: set[tuple[Pos, ...]]) -> set[Pos]:
    key = tuple(sorted(blocked, key=lambda p: (p.row, p.col)))
    print(key)
    if key in tried:
        return set()
    tried.add(key)

    for pos in blocked:
        input.grid[pos] = True

    path = p1.get_best_path(input)

    for pos in blocked:
        input.grid[pos] = False

    if path is None:
        return set()

    positions = set(state.pos for state in path.nodes)
    for state in path.nodes:
        if state.pos != input.start and state.pos != input.end:
            positions.update(block_path_rec(blocked.union([state.pos]), input, tried))
    return positions


def display(input: p1.Input, best_pos: set[Pos]):
    for i, line in enumerate(input.grid.values):
        print(
            ''.join(
                '#' if cell else ('.' if Pos(i, j) not in best_pos else 'O')
                for j, cell in enumerate(line)
            )
        )


def solution(lines: list[str]):
    input = p1.parse_input(lines)
    positions = set[Pos]()
    for path in djikstra_all(
        starts=[p1.State(input.start, Delta(0, 1))],
        ends=[p1.State(input.end, dir) for dir in Delta.of_norm(1)],
        graph=lambda s: p1.transition(s, input),
    ):
        positions.update(state.pos for state in path.nodes)
    # display(input, positions)

    return len(positions)


if __name__ == '__main__':
    helpers.run_solution(solution)
