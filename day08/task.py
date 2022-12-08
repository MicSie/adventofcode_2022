from .context import basics as helpers
import os
import re

LEFT = 0
RIGHT = LEFT + 1
TOP = RIGHT + 1
BOTTOM = TOP + 1


def parse_file(file_name: str) -> list[list[int]]:
    helpers.ensure_directory(os.path.dirname(__file__))
    return [[int(number) for number in re.findall("\d", line)] for line in helpers.read_file(file_name)]


def calculate_visibility(trees: list[list[int]]) -> list[list[int]]:
    lines = [[[] for tree in tree_line] for tree_line in trees]
    left = _calculate_visibility_from_viewpint(trees, LEFT)
    right = _calculate_visibility_from_viewpint(trees, RIGHT)
    top = _calculate_visibility_from_viewpint(trees, TOP)
    bottom = _calculate_visibility_from_viewpint(trees, BOTTOM)

    for vertical in range(len(left)):
        for horizontal in range(len(top)):
            if left[vertical][horizontal]:
                lines[vertical][horizontal].append(LEFT)
            if top[horizontal][vertical]:
                lines[vertical][horizontal].append(TOP)
            if right[vertical][horizontal]:
                lines[vertical][horizontal].append(RIGHT)
            if bottom[horizontal][vertical]:
                lines[vertical][horizontal].append(BOTTOM)

    return lines


def _calculate_visibility_from_viewpint(trees: list[list[int]], direction: int) -> list[list[bool]]:
    lines = []
    if direction == LEFT or direction == RIGHT:
        lines = [line.copy() for line in trees]
    else:
        lines = _get_vertical_lines(trees)

    if direction == BOTTOM or direction == RIGHT:
        [line.reverse() for line in lines]

    result = [_calculate_visibility_for_line(line) for line in lines]
    if direction == BOTTOM or direction == RIGHT:
        [line.reverse() for line in result]

    return result


def _get_vertical_lines(lines: list[list[int]]) -> list[list[int]]:
    vertical_lines = []
    for index in range(len(lines[0])):
        vertical_lines.append([trees[index] for trees in lines])
    return vertical_lines


def _calculate_visibility_for_line(line: list[int]) -> list[bool]:
    current_max = -1
    counter = 0
    index = 0
    result = []
    for tree in line:
        result.append(tree > current_max)
        if (result[index]):
            counter += 1
            current_max = tree
        index += 1

    return result


def count_trees(trees: list[list[int]]) -> int:
    visibility = calculate_visibility(trees)
    return sum([sum([1 if len(tree) > 0 else 0 for tree in tree_line]) for tree_line in visibility])


def get_max_scenic_score(trees: list[list[int]]) -> int:
    max_score = 0
    for vertical in range(len(trees)):
        for horizontal in range(len(trees[vertical])):
            max_score = max(max_score, get_scenic_score(
                trees, vertical, horizontal))
    return max_score


def get_scenic_score(trees: list[list[int]], vertical: int, horizontal: int) -> int:
    if vertical == 0 or vertical == len(trees) - 1:
        return 0

    if horizontal == 0 or horizontal == len(trees[vertical]) - 1:
        return 0

    directions = [
        (0, -1), (0, 1),
        (-1, 0), (1, 0)
    ]

    result = 1
    for direction in directions:
        result = result * \
            _count_visible_trees_from_position(
                (vertical, horizontal), direction, trees)
    return result


def _count_visible_trees_from_position(start: tuple[int], next: tuple[int], trees: list[list[int]]):
    value = 0
    vertical = start[0]
    horizontal = start[1]
    height = trees[vertical][horizontal]
    def break_on_edge(): return horizontal <= 0 or vertical <= 0 or vertical >= len(
        trees)-1 or horizontal >= len(trees[vertical])-1
    while (True):
        value += 1
        vertical += next[0]
        horizontal += next[1]
        if (break_on_edge() or trees[vertical][horizontal] >= height):
            break
    return value


def run_day():
    print('Day08')
    trees = parse_file('input')
    print('visible trees: ' + str(count_trees(trees)))
    print('max scenic score: ' + str(get_max_scenic_score(trees)))
