from typing import Callable
from .context import basics as helpers
import os
import re

AMOUNT_INDEX = 0
FROM_INDEX = 1
TO_INDEX = 2


def split_crates_and_instructions(input_lines: list[str]) -> tuple[list[str]]:
    result = ([], [])

    index = 0
    for line in input_lines:
        if (line.strip() == ''):
            index = 1
        else:
            result[index].append(line)

    return result


def get_stack_count(ship: list[str]) -> int:
    # from the last line find the last digits and return as int
    return int(re.search('\d+\s*$', ship.pop()).group().strip())


def read_stacks(ship: list[str]) -> list[list[str]]:
    stack_range = range(get_stack_count(ship))
    stacks = [[] for stack in stack_range]
    ship.reverse()
    for line in ship:
        index = 0
        for current_stack in stack_range:
            crate = re.sub(
                '\[|\]', '', line[index:min(index+3, len(line))]).strip()
            if (len(crate) > 0):
                stacks[current_stack].append(crate)
            index += 4
    return stacks


def parse_instructions(insructions: list[str]) -> list[list[int]]:
    return [parse_instruction(insruction) for insruction in insructions]


def parse_instruction(insruction: str) -> list[int]:
    amount = int(re.search('(?<=move)\s*\d+\s*', insruction).group().strip())
    from_value = int(re.search('(?<=from)\s*\d+\s*',
                     insruction).group().strip())
    to_value = int(re.search('(?<=to)\s*\d+\s*', insruction).group().strip())
    return [amount, from_value, to_value]


def execute_cratemover9000_instruction(instruction: list[int], crates: list[list[str]]):
    for index in range(instruction[AMOUNT_INDEX]):
        crates[instruction[TO_INDEX] -
               1].append(crates[instruction[FROM_INDEX]-1].pop())


def execute_cratemover9001_instruction(instruction: list[int], crates: list[list[str]]):
    position = len(crates[instruction[TO_INDEX]-1])
    for index in range(instruction[AMOUNT_INDEX]):
        crates[instruction[TO_INDEX] -
               1].insert(position, crates[instruction[FROM_INDEX]-1].pop())


def move_crates(file_name: str, executor: Callable[[list[int], list[list[str]]], None]) -> str:
    crates_and_instructions = split_crates_and_instructions(
        helpers.read_file(file_name, False))
    crates = read_stacks(crates_and_instructions[0])
    instructions = parse_instructions(crates_and_instructions[1])
    [executor(instruction, crates) for instruction in instructions]
    return ''.join([stack.pop() for stack in crates])


def run_createmover9000(file_name: str) -> str:
    return move_crates(file_name, execute_cratemover9000_instruction)


def run_createmover9001(file_name: str) -> str:
    return move_crates(file_name, execute_cratemover9001_instruction)


def run_day():
    helpers.ensure_directory(os.path.dirname(__file__))
    print('Day05')
    print('CrateMover9000: ' + str(run_createmover9000('input')))
    print('CrateMover9001: ' + str(run_createmover9001('input')))
