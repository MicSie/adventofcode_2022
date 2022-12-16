import functools
import itertools
import os
from .context import basics as helpers
import ast

DIVIDER_PACKET_1 = [[2]]
DIVIDER_PACKET_2 = [[6]]


def parse_line(line: str):
    return ast.literal_eval(line)


def sum_indices(pairs):
    return sum([index + 1 if is_in_order(pairs[index]) else 0 for index in range(len(pairs))])


def is_in_order(pair: tuple) -> bool:
    left_side, right_side = pair
    index = 0

    while True:
        if index >= len(left_side):
            return None if index >= len(right_side) else True

        if index >= len(right_side):
            return False

        left = left_side[index]
        right = right_side[index]

        if left == None:
            return None if right == None else True

        if right == None:
            return False

        if isinstance(left, int) and isinstance(right, int):
            if left == right:
                index += 1
            else:
                return left < right
        else:
            left_list = left if isinstance(left, list) else [left]
            right_list = right if isinstance(right, list) else [right]
            result = is_in_order((left_list, right_list))
            if result == None:
                index += 1
            else:
                return result


def insert_divider_packets_and_redorder(pairs: list):
    pairs.append((DIVIDER_PACKET_1, DIVIDER_PACKET_2))
    return sorted(itertools.chain(*pairs), key=functools.cmp_to_key(_compare))


def _compare(left, right):
    return {
        True: -1,
        False: 1,
        None: 0
    }.get(is_in_order((left, right)))

def calculate_decoder_key(pairs):
    sorted_list = insert_divider_packets_and_redorder(pairs)

    decoder_key = 1
    key_1_found = False
    key_2_found = False
    for index in range(len(sorted_list)):
        if DIVIDER_PACKET_1 == sorted_list[index]:
            decoder_key *= (index + 1)
            key_1_found = True
        elif DIVIDER_PACKET_2 == sorted_list[index]:
            decoder_key *= (index + 1)
            key_2_found = True
        if key_1_found and key_2_found:
            break
    return decoder_key


def read_file(file_name: str):
    helpers.ensure_directory(os.path.dirname(__file__))
    input_lines = helpers.read_file(file_name)
    return [(parse_line(input_lines[index]), parse_line(input_lines[index+1])) for index in range(0, len(input_lines), 3)]


def run_day():
    print('Day13')
    pairs = read_file('input')
    print(f'sum of the indices: {sum_indices(pairs)}')
    print(f'decoder key: {calculate_decoder_key(pairs)}')
