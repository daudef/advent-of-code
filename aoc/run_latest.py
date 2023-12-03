import contextlib
import pathlib
import subprocess
import sys

from aoc import helpers


def try_parse_problem(path: pathlib.Path):
    with contextlib.suppress(Exception):
        return helpers.Problem.parse_from_dir_path(path)
    return None


async def main():
    problems = [
        problem
        for (dir, sub_dirs, _) in helpers.BASE_DIR.walk()
        if len(sub_dirs) == 0
        and (problem := try_parse_problem(dir)) is not None
        and len(problem.exemple_input_path.read_text()) > 0
    ]
    problem = max(problems, key=lambda p: (p.day.year, p.day.day, p.part))
    print(f'running year {problem.day.year} day {problem.day.day} part {problem.part}')
    subprocess.run([sys.executable, problem.solution_path])


if __name__ == '__main__':
    helpers.run_main(main)
