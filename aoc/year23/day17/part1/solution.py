import collections
import dataclasses
import enum
import typing
from aoc import helpers


class Direction(enum.Enum):
    DOWN = enum.auto()
    RIGHT = enum.auto()
    UP = enum.auto()
    LEFT = enum.auto()

    def __repr__(self) -> str:
        return self.name

    def clockwise(self):
        match self:
            case Direction.DOWN:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.UP
            case Direction.UP:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.DOWN

    def anti_clockwise(self):
        match self:
            case Direction.DOWN:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.UP
            case Direction.UP:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.DOWN


@dataclasses.dataclass(frozen=True)
class Position:
    row: int
    col: int

    def __repr__(self) -> str:
        return f'({self.row}, {self.col})'

    def apply_direction(self, direction: Direction, row_count: int, col_count: int):
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
        if 0 <= row < row_count and 0 <= col < col_count:
            yield Position(row, col)


@dataclasses.dataclass(frozen=True)
class Node:
    position: Position
    dir: Direction
    move_left: int

    neighbors: 'dict[Node, int]' = dataclasses.field(compare=False, repr=False)


type NodeMap = dict[Position, dict[Direction, dict[int, Node]]]


def make_nodes(grid: list[list[int]]):
    nodes = [
        Node(position=Position(row, col), dir=dir, move_left=move_left, neighbors={})
        for row, row_values in enumerate(grid)
        for col, _ in enumerate(row_values)
        for dir in Direction
        for move_left in range(4)
    ]

    node_map: NodeMap = collections.defaultdict(lambda: collections.defaultdict(dict))

    for node in nodes:
        node_map[node.position][node.dir][node.move_left] = node

    row_count = len(grid)
    col_count = len(grid[0])

    for node in nodes:
        for dir2 in (node.dir.clockwise(), node.dir.anti_clockwise()):
            for pos2 in node.position.apply_direction(dir2, row_count, col_count):
                cost = grid[pos2.row][pos2.col]
                node2 = node_map[pos2][dir2][2]
                node.neighbors[node2] = cost
        if node.move_left > 0:
            for pos2 in node.position.apply_direction(node.dir, row_count, col_count):
                cost = grid[pos2.row][pos2.col]
                node2 = node_map[pos2][node.dir][node.move_left - 1]
                node.neighbors[node2] = cost

    return node_map


def parse_lines(lines: list[str]):
    return [[int(c) for c in line] for line in lines]


@dataclasses.dataclass(frozen=True)
class Path:
    nodes: typing.Sequence[Node]
    cost: int


def shortest_paths(start: Node):
    closest_nodes: dict[Node, Path] = {
        node: Path(nodes=[start, node], cost=cost) for node, cost in start.neighbors.items()
    }
    explored = {start}

    while len(closest_nodes) > 0:
        node, path = min(closest_nodes.items(), key=lambda t: t[1].cost)
        yield node, path
        closest_nodes.pop(node)
        explored.add(node)
        for node2, cost in node.neighbors.items():
            if node2 not in explored:
                if (previous_path := closest_nodes.get(node2)) is None or (
                    path.cost + cost < previous_path.cost
                ):
                    closest_nodes[node2] = Path(nodes=[*path.nodes, node2], cost=path.cost + cost)


def solution(lines: list[str]):
    node_map = make_nodes(parse_lines(lines))
    for node, path in shortest_paths(node_map[Position(0, 0)][Direction.RIGHT][3]):
        if node.position == Position(len(lines) - 1, len(lines[0]) - 1):
            return path.cost
    raise AssertionError


if __name__ == '__main__':
    helpers.run_solution(solution)
