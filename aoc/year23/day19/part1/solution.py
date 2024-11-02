import dataclasses
import enum
import typing

from aoc import helpers


class Operation(enum.Enum):
    GT = enum.auto()
    LT = enum.auto()


type Result = str | bool
type Object = dict[str, int]
type ObjectRange = dict[str, range]


def object_range_intersect(or1: ObjectRange, or2: ObjectRange):
    result: ObjectRange = {}
    for k in or1 | or2:
        r1 = or1.get(k)
        r2 = or2.get(k)
        u = r1 or r2
        if u is None:
            continue
        if r1 is None or r2 is None:
            result[k] = u
        else:
            result[k] = range(max(r1.start, r2.start), min(r1.stop, r2.stop))
    return result


def parse_result(s: str):
    if s == 'A':
        return True
    if s == 'R':
        return False
    return s


@dataclasses.dataclass(frozen=True)
class Condition:
    op: Operation
    lhs: str
    rhs: int

    @staticmethod
    def parse(s: str):
        if '>' in s:
            op = Operation.GT
            symb = '>'
        else:
            op = Operation.LT
            symb = '<'
        lhs, rhs = s.split(symb)
        return Condition(op, lhs=lhs, rhs=int(rhs))

    def apply(self, object: Object):
        lhs = object[self.lhs]
        match self.op:
            case Operation.LT:
                return lhs < self.rhs
            case Operation.GT:
                return lhs > self.rhs

    def get_range(self, *, inverted: bool = False):
        match self.op:
            case Operation.LT:
                if not inverted:
                    return {self.lhs: range(1, self.rhs)}
                else:
                    return {self.lhs: range(self.rhs, 4001)}
            case Operation.GT:
                if not inverted:
                    return {self.lhs: range(self.rhs + 1, 4001)}
                else:
                    return {self.lhs: range(1, self.rhs + 1)}


WorkflowRangesGetter: typing.TypeAlias = typing.Callable[[str], list[ObjectRange]]


@dataclasses.dataclass(frozen=True)
class Step:
    condition: Condition | None
    result: Result

    @staticmethod
    def parse(s: str):
        if ':' in s:
            cond, result = s.split(':')
            return Step(condition=Condition.parse(cond), result=parse_result(result))
        return Step(condition=None, result=parse_result(s))

    def apply(self, object: Object):
        if self.condition is None or self.condition.apply(object):
            return self.result

    def get_ranges(
        self, workflow_ranges_getter: WorkflowRangesGetter, previous_conditions: list[Condition]
    ) -> list[ObjectRange]:
        base_obj_ranges: list[ObjectRange]
        match self.result:
            case True:
                base_obj_ranges = [{}]
            case False:
                base_obj_ranges = []
            case str():
                base_obj_ranges = workflow_ranges_getter(self.result)

        condition_obj_ranges = [
            condition.get_range(inverted=True) for condition in previous_conditions
        ] + ([self.condition.get_range(inverted=False)] if self.condition is not None else [])

        obj_ranges: list[ObjectRange] = []
        for obj_range in base_obj_ranges:
            for condition_obj_range in condition_obj_ranges:
                obj_range = object_range_intersect(obj_range, condition_obj_range)
            if any(len(range) == 0 for range in obj_range.values()):
                continue
            obj_ranges.append(obj_range)

        return obj_ranges


@dataclasses.dataclass(frozen=True)
class Workflow:
    name: str
    steps: list[Step]

    @staticmethod
    def parse(s: str):
        assert s[-1] == '}'
        s = s[:-1]
        name, steps = s.split('{')
        return Workflow(name=name, steps=[Step.parse(ss) for ss in steps.split(',')])

    def apply(self, object: Object):
        for step in self.steps:
            if (result := step.apply(object)) is not None:
                return result
        raise RuntimeError('No result')

    def get_ranges(self, workflow_ranges_getter: WorkflowRangesGetter):
        obj_ranges: list[ObjectRange] = []
        previous_conditions: list[Condition] = []
        for step in self.steps:
            obj_ranges.extend(step.get_ranges(workflow_ranges_getter, previous_conditions))
            if step.condition is not None:
                previous_conditions.append(step.condition)
        return obj_ranges


def parse_object(s: str):
    assert s[0] == '{'
    assert s[-1] == '}'
    s = s[1:-1]
    return {name: int(value) for part in s.split(',') for (name, value) in [part.split('=')]}


@dataclasses.dataclass
class Input:
    workflow_map: dict[str, Workflow]
    objects: list[Object]

    @staticmethod
    def parse(lines: list[str]):
        workflows: list[Workflow] = []
        objects: list[dict[str, int]] = []
        finished_workflows = False
        for line in lines:
            if line == '':
                finished_workflows = True
                continue

            if finished_workflows:
                objects.append(parse_object(line))
            else:
                workflows.append(Workflow.parse(line))

        return Input(workflow_map={w.name: w for w in workflows}, objects=objects)

    def apply(self, object: Object):
        current_workflow = self.workflow_map['in']
        visited: set[str] = set()
        while True:
            if current_workflow.name in visited:
                raise RuntimeError('Cycle in workflows')
            visited.add(current_workflow.name)
            result = current_workflow.apply(object)
            match result:
                case bool():
                    return result
                case str():
                    current_workflow = self.workflow_map[result]

    def get_ranges(self):
        workflow_obj_ranges: dict[str, list[ObjectRange]] = {}

        def workflow_ranges_getter(name: str) -> list[ObjectRange]:
            obj_ranges = workflow_obj_ranges.get(name)
            if obj_ranges is None:
                obj_ranges = self.workflow_map[name].get_ranges(workflow_ranges_getter)
                workflow_obj_ranges[name] = obj_ranges
            return obj_ranges

        return workflow_ranges_getter('in')

    def apply_all(self):
        for o in self.objects:
            yield o, self.apply(o)


def object_value(o: Object):
    return sum(o.values())


def solution(lines: list[str]):
    input = Input.parse(lines)
    return sum(object_value(o) for (o, accepted) in input.apply_all() if accepted)


if __name__ == '__main__':
    helpers.run_solution(solution)
