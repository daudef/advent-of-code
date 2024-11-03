import datetime
import pathlib

import cyclopts

from aoc import _solution_template, helpers


def make_file(path: pathlib.Path, content: str | None = None):
    with path.open('w', encoding='utf-8') as f:
        if content is not None:
            f.write(content)


def get_solution_content(problem: helpers.Problem):
    content = pathlib.Path(_solution_template.__file__).read_text(encoding='utf-8')
    if problem.part == 1:
        return '\n'.join(line for line in content.split('\n') if not line.startswith('#'))
    else:
        problem.day.dir_path.parent.name
        return content.replace('# ', '', 1).format(
            year=problem.day.dir_path.parent.name,
            day=problem.day.dir_path.name,
            part=helpers.Problem(day=problem.day, part=1).dir_path.name,
        )


APP = cyclopts.App()


@APP.default
async def main(day: int = datetime.datetime.now().day, year: int = datetime.datetime.now().year):
    day_ = helpers.Day(year=year, day=day)

    print(f'Creating year {day_.year} day {day_.day}')

    try:
        day_.dir_path.mkdir(parents=True)
    except FileExistsError:
        print('Day already exists')
        exit()

    for part in (1, 2):
        problem = helpers.Problem(day=day_, part=part)
        problem.dir_path.mkdir()

        make_file(problem.solution_path, content=get_solution_content(problem))
        make_file(problem.exemple_input_path)
        make_file(problem.exemple_result_path)


if __name__ == '__main__':
    APP()
