import dataclasses
import heapq
import typing

type Graph[T] = typing.Callable[[T], typing.Iterable[tuple[T, int]]]


@dataclasses.dataclass(frozen=True, order=True)
class Path[T]:
    nodes: list[T] = dataclasses.field(compare=False)
    cost: int


def djikstra_gen[T](starts: typing.Iterable[T], graph: Graph[T], all_paths: bool):
    explored: set[T] = set()
    reachables: list[Path[T]] = []
    best_costs: dict[T, int] = {}
    for start in starts:
        reachables.append(Path(nodes=[start], cost=0))
        best_costs[start] = 0

    while len(reachables) > 0:
        path = heapq.heappop(reachables)
        node = path.nodes[-1]
        if not all_paths and node in explored:
            continue
        yield path
        explored.add(node)
        for neighbor, cost in graph(node):
            if not all_paths and neighbor in explored:
                continue
            new_neighbor_cost = path.cost + cost
            previous_best_neighbor_cost = best_costs.get(neighbor)
            if previous_best_neighbor_cost is None or (
                new_neighbor_cost <= previous_best_neighbor_cost
            ):
                best_costs[neighbor] = new_neighbor_cost
                heapq.heappush(
                    reachables, Path(nodes=[*path.nodes, neighbor], cost=new_neighbor_cost)
                )


def djikstra[T](starts: typing.Iterable[T], ends: typing.Iterable[T], graph: Graph[T]):
    end_set = set(ends)
    for path in djikstra_gen(starts, graph, all_paths=False):
        if path.nodes[-1] in end_set:
            return path
    return None


def djikstra_all[T](starts: typing.Iterable[T], ends: typing.Iterable[T], graph: Graph[T]):
    end_set = set(ends)
    cost = None
    for path in djikstra_gen(starts, graph, all_paths=True):
        if cost is not None and path.cost > cost:
            break
        if path.nodes[-1] in end_set:
            yield path
            cost = path.cost
    return
