import dataclasses
import functools
import math
from aoc import helpers
from aoc.year23.day08.part1 import solution as sol1


@dataclasses.dataclass
class Div:
    a: int
    b: int
    q: int
    r: int


@dataclasses.dataclass
class Equation:
    d: int
    u: int
    a: int
    v: int
    b: int


def extended_euclid(a: int, b: int):
    divs: list[Div] = []
    while True:
        q = a // b
        r = a % b
        if r == 0:
            break
        divs.append(Div(a, b, q, r))
        a, b = b, r

    eq = None
    for div in reversed(divs):
        if eq is None:
            eq = Equation(d=div.r, a=div.a, u=1, b=div.b, v=-div.q)
        else:
            assert eq.a == div.b
            assert eq.b == div.r
            eq = Equation(d=eq.d, a=div.a, b=div.b, u=eq.v, v=eq.u - eq.v * div.q)
            assert eq.d == eq.u * eq.a + eq.v * eq.b

    return eq


@dataclasses.dataclass
class Cycle:
    period: int
    offset: int

    def first_iter(self):
        assert self.period > 0
        if self.offset < 0:
            return math.ceil(-self.offset / self.period)
        return math.floor(1 - (1 + self.offset) / self.period)


def solve_diophantine(a: int, b: int, c: int):
    eq = extended_euclid(a, b)
    if eq is None:
        return None
    assert c % eq.d == 0
    f = c // eq.d
    return Cycle(offset=eq.u * f, period=b // eq.d), Cycle(offset=eq.v * f, period=-a // eq.d)


def merge(c1: Cycle, c2: Cycle):
    ks = solve_diophantine(c1.period, b=-c2.period, c=c2.offset - c1.offset)
    if ks is None:
        assert c1.period == c2.period
        assert c1.period % 2 == 0
        if c1.offset == c1.period:
            c1.offset = 0
        if c2.offset == c1.period:
            c2.offset = 0
        assert {c1.offset, c2.offset} == {0, c1.period // 2}
        return Cycle(period=c1.period // 2, offset=0)

    k1, k2 = ks
    assert k1.period > 0
    assert k2.period > 0

    first_k = max(k1.first_iter(), k2.first_iter())
    return Cycle(period=k1.period * c1.period, offset=c1.offset + (c1.period * first_k))


def get_cycles(inst: sol1.Instructions, start: str, ends: set[str]):
    reached: dict[sol1.State, int] = {}
    for i, state in enumerate(inst.run(start)):
        if (j := reached.get(state)) is not None:
            break
        reached[state] = i
    else:
        raise RuntimeError()

    period = i - j
    for state, i in reached.items():
        if state.label in ends and i >= j:
            yield Cycle(period, offset=i)


def solution(input: list[str]):
    # print(merge(Cycle(11, 10), Cycle(9, 30)))

    inst = sol1.parse(input)
    starts = {k for k in inst.labels if k.endswith('A')}
    ends = {k for k in inst.labels if k.endswith('Z')}
    cycles = [c for k in starts for c in get_cycles(inst, k, ends=ends)]
    print(cycles)

    cycle = functools.reduce(merge, cycles)
    print(cycle)
    res = cycle.offset + cycle.period * cycle.first_iter()
    if res == 0:
        return cycle.period
    return res


if __name__ == '__main__':
    helpers.run_solution(solution)
