import dataclasses
import typing

from aoc import helpers


@dataclasses.dataclass
class Input:
    a: int
    b: int
    c: int
    program: list[int]


def parse_input(lines: list[str]):
    a = None
    b = None
    c = None
    program = None
    for line in lines:
        if line == '':
            continue
        key, _, values = line.partition(':')
        values = list(map(int, values.split(',')))
        match key.lower().split():
            case ['register', name]:
                assert len(values) == 1
                value = values[0]
                match name:
                    case 'a':
                        a = value
                    case 'b':
                        b = value
                    case 'c':
                        c = value
                    case _:
                        raise RuntimeError('invalid register name', name)

            case ['program']:
                program = values

            case _:
                raise RuntimeError('invalid line', line)
    assert a is not None
    assert b is not None
    assert c is not None
    assert program is not None

    return Input(a=a, b=b, c=c, program=program)


def make_state(input: Input):
    return State(a=input.a, b=input.b, c=input.c, program=input.program, pc=0, output=[])


@dataclasses.dataclass
class State(Input):
    pc: int
    output: list[int]


def get_combo_value(i: int, state: State):
    if i in range(4):
        return i

    if i == 4:
        return state.a
    if i == 5:
        return state.b
    if i == 6:
        return state.c

    raise RuntimeError('invalid combo value', i)


def adv(state: State, arg: int):
    state.a = state.a // (1 << get_combo_value(arg, state))


def bxl(state: State, arg: int):
    state.b = state.b ^ arg


def bst(state: State, arg: int):
    state.b = get_combo_value(arg, state) & 0x7


def jnz(state: State, arg: int):
    if state.a != 0:
        state.pc = arg


def bxc(state: State, _arg: int):
    state.b = state.b ^ state.c


def out(state: State, arg: int):
    state.output.append(get_combo_value(arg, state) & 0x7)


def bdv(state: State, arg: int):
    state.b = state.a // (1 << get_combo_value(arg, state))


def cdv(state: State, arg: int):
    state.c = state.a // (1 << get_combo_value(arg, state))


OPCODE_INSTRUCTION_MAP: list[typing.Callable[[State, int], None]] = [
    adv,
    bxl,
    bst,
    jnz,
    bxc,
    out,
    bdv,
    cdv,
]


def run(state: State):
    while 0 <= state.pc < len(state.program) - 1:
        opcode = state.program[state.pc]
        arg = state.program[state.pc + 1]
        state.pc += 2
        OPCODE_INSTRUCTION_MAP[opcode](state, arg)


def make_result(state: State):
    print(','.join(str(c) for c in state.output))
    if len(state.output) > 0:
        return int(''.join(str(c) for c in state.output))
    return 0


def solution(lines: list[str]):
    input = parse_input(lines)
    state = make_state(input)
    run(state)
    print(state)
    return make_result(state)


if __name__ == '__main__':
    helpers.run_solution(solution)
