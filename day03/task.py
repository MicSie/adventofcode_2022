from .context import basics as helpers
import os

GROUP_SIZE = 3


def get_item_value(item: str) -> int:
    return ord(item) - 38 if item.isupper() else ord(item) - 96


def find_duplicate(rucksack: str) -> str:
    compartment1 = set(rucksack[int(len(rucksack)/2):])
    compartment2 = set(rucksack[:int(len(rucksack)/2)])
    return ''.join(compartment1.intersection(compartment2))


def read_priority(file_name: str) -> int:
    return sum([get_item_value(find_duplicate(rucksack)) for rucksack in helpers.read_file(file_name)])


def find_group_items(rucksacks: list) -> list:
    # *group => repetition operator on list
    return [''.join(set.intersection(*group)) for group in split_groups(rucksacks)]


def split_groups(rucksacks: list) -> list:
    for index in range(0, len(rucksacks), GROUP_SIZE):
        yield [set(rucksack) for rucksack in rucksacks[index:index+GROUP_SIZE]]


def read_group_priority(file_name: str) -> int:
    return sum([get_item_value(item) for item in find_group_items(helpers.read_file(file_name))])


def run_day():
    helpers.ensure_directory(os.path.dirname(__file__))
    print('Day03')
    print('priorities: ' + str(read_priority('input.txt')))
    print('group priorities: ' + str(read_group_priority('input.txt')))
