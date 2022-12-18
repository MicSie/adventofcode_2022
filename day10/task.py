from .context import basics as helpers
import os
import re

def execute_instructions(instructions:list[str]) -> list[int]:
    current_value = 1
    history = [current_value]
    for raw_line in instructions:
        history.append(current_value)
        if raw_line != 'noop':
            amount = raw_line.split(' ')[1]
            current_value += int(amount)
            history.append(current_value)
    return history

def parse_file(file_name: str) -> list[int]:
    helpers.ensure_directory(os.path.dirname(__file__))
    return execute_instructions(helpers.read_file(file_name))

def calulate_strength(history: list[int]) -> int:
    position = 19
    strength = 0
    while position < len(history):
        strength += (position+1) * history[position]
        position += 40
    return strength

def daw_screen(history: list[int]) -> None:
    [print(screen_row) for screen_row in calculate_screen(history)]

def calculate_screen(history: list[int]) -> list[str]:
    return [_calulate_row(screen_row) for screen_row in _split_into_screen_rows(history)]

def _split_into_screen_rows(history: list[int]) -> list[list[int]]:
    rows = []
    position = 0
    while position+40 < len(history):
        rows.append(history[position:position+40])
        position += 40
    return rows

def _calulate_row(history: list[int]) -> str:
    result = ''
    for cycle in range(40):
        sprite = _calculate_sprite(history[cycle])
        result += sprite[cycle]

    return result

def _calculate_sprite(position:int) -> str:
    left = max(position - 1, 0)
    right = min(position + 1, 39)
    return '.'*(left) + '#'*3 + '.'*(39-right)

def run_day():
    print('Day10')
    history = parse_file('input.txt')
    print("signal strength: " + str(calulate_strength(history)))
    print("screen:")
    print()
    daw_screen(history)