from .context import basics as helpers
import os
from typing import Callable


def read_tuple(assignment: str) -> tuple[int]:
    splitted = assignment.split('-')
    return (int(splitted[0]), int(splitted[1]))


def contains(assignment: list[str]) -> bool:
    tuple1 = read_tuple(assignment[0])
    tuple2 = read_tuple(assignment[1])
    return ((tuple1[0] <= tuple2[0] and tuple1[1] >= tuple2[1])
            or (tuple2[0] <= tuple1[0] and tuple2[1] >= tuple1[1]))


def count_fully_contained_assignments(file_name: str) -> int:
    return count_data(file_name, contains)


def is_in_range(number: int, range: tuple[int]) -> bool:
    return number >= min(range) and number <= max(range)


def are_ranges_intersecting(range1: tuple[int], range2: tuple[int]) -> bool:
    return (is_in_range(min(range1), range2)
            or is_in_range(max(range1), range2)
            or is_in_range(min(range2), range1)
            or is_in_range(max(range2), range1))


def overlaps(assignment: list[str]) -> bool:
    return are_ranges_intersecting(read_tuple(assignment[0]), read_tuple(assignment[1]))


def count_overlaping_assignments(file_name: str) -> int:
    return count_data(file_name, overlaps)


def count_data(file_name: str, evaluator: Callable[[list[str]], bool]) -> int:
    return sum([1 if evaluator(line.split(',')) else 0 for line in helpers.read_file(file_name)])


def run_day():
    helpers.ensure_directory(os.path.dirname(__file__))
    print('Day04')
    print('fully contained assignments: ' +
          str(count_fully_contained_assignments('input.txt')))
    print('overlaping assignments: ' +
          str(count_overlaping_assignments('input.txt')))
