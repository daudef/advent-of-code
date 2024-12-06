from aoc import helpers
from aoc.year24.day06.part1 import solution as p1  # pyright: ignore[reportUnusedImport]


def is_looping(input: p1.Input):
    visited = set[p1.State]()
    for state in p1.gen_states(input):
        if state in visited:
            return True
        visited.add(state)
    return False


def add_obstacle(pos: p1.Position, input: p1.Input):
    return p1.Input(max=input.max, start=input.start, obstacles=input.obstacles.union([pos]))


def set_start(state: p1.State, input: p1.Input):
    return p1.Input(max=input.max, start=state, obstacles=input.obstacles)


def is_looping_with_obstacle_in_front(current: p1.State, input: p1.Input, tried: set[p1.Position]):
    new_input = p1.Input(max=input.max, start=current, obstacles=input.obstacles)
    new_obstacle = current.pos + current.direction
    if (
        new_obstacle in input.obstacles
        or not p1.is_pos_in_bounds(new_obstacle, input)
        or new_obstacle in tried
    ):
        return None

    new_input.obstacles.add(new_obstacle)

    visited = set[p1.State]()
    is_looping = False
    for state in p1.gen_states(new_input):
        if state in visited:
            is_looping = True
            break

        visited.add(state)

    new_input.obstacles.remove(new_obstacle)
    return new_obstacle if is_looping else None


def gen_looping_obstacles(input: p1.Input):
    tried = set[p1.Position]()

    for state in p1.gen_states(input):
        new_obstacle = is_looping_with_obstacle_in_front(state, input, tried)
        if new_obstacle is not None:
            yield new_obstacle
        tried.add(state.pos)


def solution(lines: list[str]):
    return sum(1 for _ in gen_looping_obstacles(p1.parse_input(lines)))


if __name__ == '__main__':
    helpers.run_solution(solution)
