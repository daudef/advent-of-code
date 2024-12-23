from aoc import helpers
from aoc.year24.day23.part1 import solution as p1


def expand_clique(clique: frozenset[str], neighbors: dict[str, set[str]]):
    candidates = None
    for elem in clique:
        if candidates is None:
            candidates = neighbors[elem]
        else:
            candidates = candidates.intersection(neighbors[elem])
        if len(candidates) == 0:
            break

    if candidates is not None and len(candidates) > 0:
        return frozenset([*clique, next(iter(candidates))])


def solution(lines: list[str]):
    neighbors = p1.parse_input(lines)

    cliques = p1.find_cliques_on_size_3(neighbors)
    while True:
        new_cliques = {
            new_clique
            for clique in cliques
            if (new_clique := expand_clique(clique, neighbors)) is not None
        }
        if len(new_cliques) == 0:
            assert len(cliques) == 1, cliques
            clique = next(iter(cliques))
            return ','.join(sorted(clique))
        cliques = new_cliques


if __name__ == '__main__':
    helpers.run_solution(solution)
