from aoc import helpers


def parse_line(line: str) -> int:
    assert line[0] in 'LR'
    num = int(line[1:])
    if line[0] == 'L':
        num = -num
    return num


def parse_lines(lines: list[str]) -> list[int]:
    return [parse_line(line) for line in lines]


def run(nums: list[int]):
    positions = [50]
    for num in nums:
        positions.append((positions[-1] + num) % 100)
    return positions


def solution(lines: list[str]):
    positions = run(parse_lines(lines))
    return sum(1 for p in positions if p == 0)


if __name__ == '__main__':
    helpers.run_solution(solution)
