from aoc import helpers
from aoc.year23.day10.part1 import solution as p1


def gen_inside_pos(input: p1.Input):
    path = p1.get_path(input)
    assert path is not None
    path_pos_set = set(path)

    start_dir1 = p1.Direction.from_position_pair(path[-1], path[0])
    start_dir2 = p1.Direction.from_position_pair(path[-1], path[-2])
    assert start_dir1 is not None
    assert start_dir2 is not None
    start_connector = p1.Connector(start_dir1, start_dir2)

    for row_index, row in enumerate(input.grid):
        is_inside = False
        for col_index, cell in enumerate(row):
            pos = p1.Position(row=row_index, col=col_index)

            if pos in path_pos_set:
                assert cell is not None
                connector = start_connector if isinstance(cell, p1.Start) else cell
                if connector.dir1 == p1.Direction.UP or connector.dir2 == p1.Direction.UP:
                    is_inside = not is_inside
            else:
                if is_inside:
                    yield pos


def solution(lines: list[str]):
    input = p1.Input.parse(lines)
    input.display()
    return len(list(gen_inside_pos(input)))


if __name__ == '__main__':
    helpers.run_solution(solution)
