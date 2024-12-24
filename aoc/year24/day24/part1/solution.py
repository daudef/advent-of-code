import collections
import dataclasses
import enum

import graphlib

from aoc import helpers


class Operator(enum.Enum):
    AND = enum.auto()
    OR = enum.auto()
    XOR = enum.auto()


OPERATOR_NAME_MAP = {o.name: o for o in Operator}


@dataclasses.dataclass(frozen=True)
class Operation:
    left: str
    op: Operator
    right: str
    res: str


@dataclasses.dataclass
class Input:
    initial_state: dict[str, bool]
    operations: list[Operation]


def parse_input(lines: list[str]):
    input = Input({}, [])
    line_it = iter(lines)
    for line in line_it:
        if line == '':
            break
        wire, value = line.split(':')
        input.initial_state[wire] = bool(int(value))
    for line in line_it:
        match line.split():
            case [left, op, right, '->', res]:
                input.operations.append(Operation(left, OPERATOR_NAME_MAP[op], right, res))
            case _:
                raise RuntimeError(f'invalid operation: {line}')
    return input


def sort_operations(input: Input):
    operand_operation_map: dict[str, set[Operation]] = collections.defaultdict(set)
    for operation in input.operations:
        operand_operation_map[operation.left].add(operation)
        operand_operation_map[operation.right].add(operation)

    transitions = {
        operation: operand_operation_map[operation.res] for operation in input.operations
    }
    return list(reversed(list(graphlib.TopologicalSorter(transitions).static_order())))


def run_operation(operation: Operation, state: dict[str, bool]):
    left = state[operation.left]
    right = state[operation.right]
    match operation.op:
        case Operator.OR:
            res = left or right
        case Operator.AND:
            res = left and right
        case Operator.XOR:
            res = left != right
    state[operation.res] = res


def run(input: Input):
    state = input.initial_state.copy()
    for operation in input.operations:
        run_operation(operation, state)
    return state


def get_result(state: dict[str, bool]):
    z_wires = sorted((k for k in state if k.startswith('z')), reverse=True)
    values = [state[k] for k in z_wires]
    return int(''.join(str(int(v)) for v in values), base=2)


def solution(lines: list[str]):
    input = parse_input(lines)
    input.operations = sort_operations(input)
    state = run(input)
    return get_result(state)


if __name__ == '__main__':
    helpers.run_solution(solution)
