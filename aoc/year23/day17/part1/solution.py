import dataclasses
import enum
import heapq
import typing

from aoc import helpers


class Direction(enum.Enum):
    DOWN = enum.auto()
    RIGHT = enum.auto()
    UP = enum.auto()
    LEFT = enum.auto()

    def clockwise(self):
        return CLOCKWISE_DIRECTION_MAP[self]

    def anti_clockwise(self):
        return ANTI_CLOCKWISE_DIRECTION_MAP[self]


CLOCKWISE_DIRECTION_MAP = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP,
}

ANTI_CLOCKWISE_DIRECTION_MAP = {d2: d1 for (d1, d2) in CLOCKWISE_DIRECTION_MAP.items()}


@dataclasses.dataclass(frozen=True, slots=True)
class Position:
    row: int
    col: int

    def apply_direction(self, direction: Direction, max_pos: 'Position'):
        row = self.row
        col = self.col
        match direction:
            case Direction.DOWN:
                row += 1
            case Direction.RIGHT:
                col += 1
            case Direction.UP:
                row -= 1
            case Direction.LEFT:
                col -= 1
        if 0 <= row <= max_pos.row and 0 <= col <= max_pos.col:
            return Position(row, col)
        return None


@dataclasses.dataclass(frozen=True, slots=True)
class Momentum:
    dir: Direction
    len: int


@dataclasses.dataclass(frozen=True, slots=True)
class MomentumRange:
    min_len: int
    max_len: int


@dataclasses.dataclass(frozen=True, slots=True)
class Node:
    pos: Position
    mom: Momentum | None


def gen_neighbors(node: Node, max_pos: Position, mom_range: MomentumRange):
    turn_directions: typing.Iterable[Direction]
    if node.mom is None:
        turn_directions = Direction
    else:
        if node.mom.len >= mom_range.min_len:
            turn_directions = (node.mom.dir.clockwise(), node.mom.dir.anti_clockwise())
        else:
            turn_directions = []

        if node.mom.len < mom_range.max_len:
            neighbor_pos = node.pos.apply_direction(node.mom.dir, max_pos)
            if neighbor_pos is not None:
                yield Node(neighbor_pos, Momentum(node.mom.dir, len=node.mom.len + 1))

    for dir in turn_directions:
        neighbor_pos = node.pos.apply_direction(dir, max_pos)
        if neighbor_pos is not None:
            yield Node(neighbor_pos, Momentum(dir, len=1))


@dataclasses.dataclass(frozen=True, slots=True, order=True)
class Path:
    cost: int
    nodes: typing.Sequence[Node] = dataclasses.field(compare=False)


def gen_shortest_paths(grid: list[list[int]], max_pos: Position, mom_range: MomentumRange):
    start_node = Node(Position(row=0, col=0), mom=None)
    explored: set[Node] = set()
    reachables = [Path(nodes=[start_node], cost=0)]
    best_costs = {start_node: 0}

    while len(reachables) > 0:
        path = heapq.heappop(reachables)
        node = path.nodes[-1]
        if node in explored:
            continue
        yield path
        explored.add(node)
        for neighbor_node in gen_neighbors(node, max_pos, mom_range):
            if neighbor_node in explored:
                continue
            new_neighbor_cost = path.cost + grid[neighbor_node.pos.row][neighbor_node.pos.col]
            previous_best_neighbor_cost = best_costs.get(neighbor_node)
            if previous_best_neighbor_cost is None or (
                new_neighbor_cost < previous_best_neighbor_cost
            ):
                best_costs[neighbor_node] = new_neighbor_cost
                heapq.heappush(
                    reachables, Path(nodes=[*path.nodes, neighbor_node], cost=new_neighbor_cost)
                )


def parse_lines(lines: list[str]):
    return [[int(c) for c in line] for line in lines]


def solve(lines: list[str], mom_range: MomentumRange):
    grid = parse_lines(lines)
    max_pos = Position(row=len(grid) - 1, col=len(grid[0]) - 1)
    for path in gen_shortest_paths(grid, max_pos, mom_range):
        last_node = path.nodes[-1]
        if (
            last_node.pos == max_pos
            and last_node.mom is not None
            and last_node.mom.len >= mom_range.min_len
        ):
            return path.cost
    raise RuntimeError('Last position not found')


def solution(lines: list[str]):
    return solve(lines, mom_range=MomentumRange(1, 3))


if __name__ == '__main__':
    helpers.run_solution(solution)
