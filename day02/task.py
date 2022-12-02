from .context import basics as helpers
import os

# A for Rock, B for Paper, and C for Scissors
# X for Rock, Y for Paper, and Z for Scissors
# 1 for Rock, 2 for Paper, and 3 for Scissors

# updated: X lose, Y draw, and Z win

ROCK = 1
PAPER = 2
SCISSORS = 3

LOST = 0
DRAW = 3
WIN = 6


def get_value(input: str, guested: bool = True) -> int:
    return {
        'A': ROCK,
        'X': ROCK if guested else LOST,
        'B': PAPER,
        'Y': PAPER if guested else DRAW,
        'C': SCISSORS,
        'Z': SCISSORS if guested else WIN
    }.get(input.upper())


def fight(left: int, right: int) -> int:
    if (left == right):
        return DRAW

    if (left == ROCK):
        return WIN if right == SCISSORS else LOST

    if (left == PAPER):
        return WIN if right == ROCK else LOST

    # SCISSORS
    return WIN if right == PAPER else LOST


def calulate_line_guest(line: str) -> int:
    values = [get_value(part) for part in line.split(' ')]
    return values[1] + fight(values[1], values[0])


def calculate_score(file_name: str) -> int:
    return sum([calulate_line_guest(line) for line in helpers.read_file(file_name)])


def calulate_line_guide(line: str) -> int:
    values = [get_value(part, guested=False) for part in line.split(' ')]
    if (fight(ROCK, values[0]) == values[1]):
        return ROCK + values[1]
    if (fight(PAPER, values[0]) == values[1]):
        return PAPER + values[1]
    return SCISSORS + values[1]


def read_guide(file_name: str) -> int:
    return sum([calulate_line_guide(line) for line in helpers.read_file(file_name)])


def RunDay():
    helpers.ensure_directory(os.path.dirname(__file__))
    print('Day02')
    print('guested score: ' + str(calculate_score('input')))
    print('guide score: ' + str(read_guide('input')))


if __name__ == '__main__':
    RunDay()
