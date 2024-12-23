from aoc import helpers


def apply_step(secret: int):
    secret = (secret ^ (secret << 6)) & 0xFFFFFF
    secret = (secret ^ secret >> 5) & 0xFFFFFF
    secret = (secret ^ (secret << 11)) & 0xFFFFFF
    return secret


def apply_n_step(secret: int, n: int):
    for _ in range(n):
        secret = apply_step(secret)
    return secret


def solution(lines: list[str]):
    return sum(apply_n_step(int(line), 2000) for line in lines)


if __name__ == '__main__':
    helpers.run_solution(solution)
