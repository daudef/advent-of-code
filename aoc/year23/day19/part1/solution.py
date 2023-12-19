import dataclasses
import enum
from aoc import helpers


class Operation(enum.Enum):
    GT = enum.auto()
    LT = enum.auto()


type Result = str | bool
type Object = dict[str, int]


def parse_result(s: str):
    if s == 'A':
        return True
    if s == 'R':
        return False
    return s


@dataclasses.dataclass
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


@dataclasses.dataclass
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


@dataclasses.dataclass
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
