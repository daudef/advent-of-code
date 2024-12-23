import collections

from aoc import helpers


def parse_input(lines: list[str]):
    network_map: dict[str, set[str]] = collections.defaultdict(set)
    for line in lines:
        c1, _, c2 = line.partition('-')
        network_map[c1].add(c2)
        network_map[c2].add(c1)
    return network_map


def find_cliques_on_size_3(neighbors: dict[str, set[str]]):
    triplets: set[frozenset[str]] = set()
    for c1, c1_neighbors in neighbors.items():
        for c2 in c1_neighbors:
            for c3 in c1_neighbors.intersection(neighbors[c2]):
                triplets.add(frozenset((c1, c2, c3)))
    return triplets


def solution(lines: list[str]):
    neighbors = parse_input(lines)

    return len([c for c in find_cliques_on_size_3(neighbors) if any(e.startswith('t') for e in c)])


if __name__ == '__main__':
    helpers.run_solution(solution)
