from .context import basics
import os

def part1(calories: list) -> int:
    return max(calories)


def part2(calories: list) -> int:
    return sum(sorted(calories, reverse=True)[:3])


def read_calories_from_file(fileName: str) -> list:
    lines = basics.read_file(fileName)
    return sum_lines(lines)


def sum_lines(lines: list) -> list:
    result = []
    current = 0
    for line in lines:
        if (len(line) == 0):
            if (current > 0):
                result.append(current)
                current = 0
        else:
            current += int(line)

    if (current > 0):
        result.append(current)
    return result


def RunDay():
    basics.ensure_directory(os.path.dirname(__file__))
    print('Day01')
    calories = read_calories_from_file('input')
    print('Part1: '+str(part1(calories)))
    print('Part2: '+str(part2(calories)))