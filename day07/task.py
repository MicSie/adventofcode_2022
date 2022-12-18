from typing import Any, Callable
from .context import basics as helpers
import os
import re


class File():
    _name = ''
    _size = 0

    def __init__(self, name: str, size: int) -> None:
        self._name = name
        self._size = size

    def get_name(self) -> str:
        return self._name

    def get_size(self) -> int:
        return self._size


class Directory():
    _directories = []
    _files = []
    _name = ''
    _parent = None

    def __init__(self, name: str = '/', parent: 'Directory' = None) -> None:
        self._directories = []
        self._files = []
        self._name = name
        if parent != None:
            self.set_parent(parent)

    def has_parent(self) -> bool:
        return self._parent != None

    def get_parent(self) -> 'Directory':
        return self._parent

    def set_parent(self, parent: 'Directory') -> None:
        self._parent = parent

    def add_directory(self, directory: 'Directory') -> None:
        self._directories.append(directory)
        directory.set_parent(self)

    def add_file(self, file: 'File') -> None:
        self._files.append(file)

    def get_size(self) -> int:
        return sum([file.get_size() for file in self._files]) + sum([directory.get_size() for directory in self._directories])

    def get_name(self) -> str:
        return self._name

    def find_directory(self, name: str) -> 'Directory':
        # next: next item of an iterator => (iterator, default)
        return next(filter((lambda directory: directory.get_name() == name), self._directories), None)

    def find_file(self, name: str) -> 'File':
        return next(filter((lambda file: file.get_name() == name), self._files), None)

    def get_all_directories(self) -> list['Directory']:
        all_directories = []
        for directory in self._directories:
            [all_directories.append(sub_directory)
             for sub_directory in directory.get_all_directories()]
            all_directories.append(directory)
        return all_directories


class Filesystem():
    _current_directory = None

    def __init__(self, file_name: str = None, root: 'Directory' = Directory()) -> None:
        self._current_directory = root
        if file_name != None:
            instructions = helpers.read_file(file_name)
            execute_instructions(self, split_instructions(instructions))
            self.change_directory('/')

    def _get_root(self) -> 'Directory':
        possible_root = self._current_directory
        while possible_root.has_parent():
            possible_root = possible_root.get_parent()
        return possible_root

    def get_current_directory(self) -> 'Directory':
        return self._current_directory

    def change_directory(self, name: str) -> None:
        change_to = None
        if name == '/':
            change_to = self._get_root()
        elif name == '..':
            change_to = self._current_directory.get_parent()
        else:
            change_to = self._current_directory.find_directory(name)

        if change_to != None:
            self._current_directory = change_to


def execute_instructions(filesystem: 'Filesystem', instructions: list[list[str]]) -> None:
    for instruction in instructions:
        if instruction[0].startswith('$ ls'):
            read_list(instruction, filesystem.get_current_directory())
        else:
            directory_name = re.search(
                '(?<=\$ cd)\s*\S+', instruction[0]).group().strip()
            if filesystem.get_current_directory().find_directory(directory_name) == None:
                filesystem.get_current_directory().add_directory(Directory(directory_name))
            filesystem.change_directory(directory_name)


def directory_size_to_delete(filesystem: 'Filesystem',) -> int:
    filesystem.change_directory('/')
    total_disk_space = 70000000
    update_size = 30000000
    free_space = total_disk_space - filesystem.get_current_directory().get_size()
    needed_size = update_size - free_space
    delete_candidates = [filtered_directory.get_size() for filtered_directory in filter_all_directories(
        filesystem, lambda directory: directory.get_size() >= needed_size)]
    delete_candidates.sort()
    return delete_candidates[0]


def sum_smallest_directories(filesystem: 'Filesystem', max_size: int) -> int:
    filesystem.change_directory('/')
    return sum([filtered_directory.get_size() for filtered_directory in filter_all_directories(filesystem, lambda directory: directory.get_size() < max_size)])


def filter_all_directories(filesystem: 'Filesystem', filter_methode: Callable[['Directory'], bool]) -> list['Directory']:
    directories = filesystem.get_current_directory().get_all_directories()
    return filter(filter_methode, directories)


def split_instructions(instructions: list[str]) -> list[list[str]]:
    split_instructions = []
    current_set = []

    for instruction in instructions:
        if instruction.startswith('$ cd'):
            if len(current_set) > 0:
                split_instructions.append(current_set)
            split_instructions.append([instruction])
            current_set = []
        else:
            current_set.append(instruction)

    if len(current_set) > 0:
        split_instructions.append(current_set)
    return split_instructions


def read_list(instructions: list[str], directory: 'Directory') -> None:
    for instruction in instructions:
        if instruction.startswith('$'):
            continue
        split_instruction = instruction.split(' ')
        if split_instruction[0] == 'dir':
            directory.add_directory(Directory(split_instruction[1]))
        else:
            directory.add_file(
                File(split_instruction[1], int(split_instruction[0])))


def run_day():
    helpers.ensure_directory(os.path.dirname(__file__))
    filesystem = Filesystem('input.txt')
    print('Day07')
    print('directories with a total size of at most 100000: ' +
          str(sum_smallest_directories(filesystem, 100000)))
    print('size of directory to delete: ' +
          str(directory_size_to_delete(filesystem)))
