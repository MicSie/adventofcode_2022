
from datetime import datetime
import math
import os
import sys
from .context import basics as helpers

NEXT_POSITIONS = [
    (1, 0),  # straigt down
    (1, -1),  # down left
    (1, 1),  # down right
]


class Cell:
    def __init__(self, is_wall = False) -> None:
        self.is_sand = False
        self.is_wall = is_wall
        self.is_start = False

    def is_blocked(self):
        return self.is_sand or self.is_wall


class GridHolder:
    def __init__(self, file_name, compress=False) -> None:
        self._start_position = (0, 500)
        self.grid = [[Cell()]]
        self.done = False
        self.sand_counter = 0
        self.abyss_sand_counter = 0
        self.filled_sand_counter = 0
        self.current_path = [self._start_position]
        self._abyss_level = 0
        self._build_grid(file_name, compress)

    def count_sand(self):
        while not self.done:
            self.run_cycle()

    def run_cycle(self):
        current_sand = self._start_position
        self.current_path = []
        self.sand_counter += 1
        has_moved = True
        while has_moved == True:
            has_moved = False
            self.current_path.append(current_sand)
            current_row, current_column = current_sand
            if current_row + 1 == self._abyss_level and self.abyss_sand_counter == 0:
                self.abyss_sand_counter = self.sand_counter - 1  # don't count current
            for next_row, next_column in NEXT_POSITIONS:
                next_position = self.grid[next_row +
                                          current_row][next_column + current_column]
                if not next_position.is_blocked():
                    current_row += next_row
                    current_column += next_column
                    has_moved = True
                    break
            if not has_moved:
                if self.grid[current_row][current_column].is_start:
                    self.filled_sand_counter = self.sand_counter
                    self.done = True
                    return
                self.grid[current_row][current_column].is_sand = True
            else:
                current_sand = (current_row, current_column)

    def _build_grid(self, file_name, compress):
        helpers.ensure_directory(os.path.dirname(__file__))
        for input_line in helpers.read_file(file_name):
            last_checkpoint = None
            for column, row in [point.strip().split(',') for point in input_line.split('->')]:
                row = int(row)
                column = int(column)
                self._ensure_rows(row)
                self._ensure_columns(column)
                if last_checkpoint != None:
                    self._fill_gabs(last_checkpoint, (row, column))
                last_checkpoint = (row, column)

        if len(self.grid[0]) > self._start_position[1]:
            self.grid[self._start_position[0]
                      ][self._start_position[1]].is_start = True

        if compress:
            self._compress_grid()

        self._abyss_level = len(self.grid)
        self.grid.append([Cell() for _ in range(len(self.grid[0]))])
        self.grid.append([Cell(True) for _ in range(len(self.grid[0]))])

    def _ensure_rows(self, target_row_count):
        while len(self.grid) <= target_row_count:
            self.grid.append([Cell() for _ in range(len(self.grid[0]))])

    def _ensure_columns(self, target_column_count):
        target_column_count += 1
        missing_column_count = target_column_count - len(self.grid[0])
        if missing_column_count > 0:
            for row in self.grid:
                row.extend([Cell() for _ in range(missing_column_count)])

    def _fill_gabs(self, from_point, to_point):
        from_row, from_column = from_point
        to_row, to_column = to_point
        for row in self._get_range(from_row, to_row):
            for column in self._get_range(from_column, to_column):
                self.grid[row][column].is_wall = True

    def _get_range(self, start, end):
        numbers = list(range(start, end, 1 if start < end else -1))
        numbers.append(end)
        return numbers

    def _compress_grid(self):
        min_column = self._get_min_column_index()
        max_column = self._get_max_column_index()
        max_size = max(math.ceil(abs(max_column-min_column)*1.1),
                       math.ceil((len(self.grid)+2)*2.1))

        if max_size % 2 != 0:
            max_size += 1

        min_column = min(
            min_column, self._start_position[1] - math.ceil(max_size / 2))

        row_index = 0
        for row in self.grid:
            self.grid[row_index] = row[min_column:]
            row_index += 1

        self._ensure_columns(max_size)

        column_index = 0
        for column in self.grid[0]:
            if column.is_start:
                self._start_position = (0, column_index)
                break
            column_index += 1

    def _get_min_column_index(self):
        for column_index in range(len(self.grid[0])):
            for row in self.grid:
                if row[column_index].is_blocked():
                    return column_index-1

    def _get_max_column_index(self):
        for column_index in range(len(self.grid[0])-1, -1, -1):
            for row in self.grid:
                if row[column_index].is_blocked():
                    return column_index+1


def run_day():
    print('Day14')
    grid_holder = GridHolder('input.txt', True)
    grid_holder.count_sand()
    print(f'sand until abyss: {grid_holder.abyss_sand_counter}')
    print(f'sand until filled: {grid_holder.filled_sand_counter}')
