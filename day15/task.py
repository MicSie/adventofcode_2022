from datetime import datetime
import multiprocessing as mp
import os
import re
from .context import basics as helpers


class GridHolder:
    def __init__(self, file_name) -> None:
        self._pairs = []
        self._sensor_ranges = [(0, 0, 0)]
        self._build_list(file_name)

    def find_tuning_frequency(self, min_index, max_index):
        arguments = [(min_index, max_index, row_index)
                     for row_index in range(min_index, max_index+1)]

        with mp.Pool(mp.cpu_count()) as pool:
            for chunk in self._chunks(arguments, mp.cpu_count()):
                for result in pool.map(self._find_tuning_frequency_for_row, chunk):
                    if result != None:
                        return result

    def _chunks(self, lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def _find_tuning_frequency_for_row(self, input_tuple):
        min_index, max_index, row_index = input_tuple
        date_time = datetime.now().strftime('%X.%f')
        print(f'{date_time}: testing row {row_index} / {max_index}')
        blocked_ranges = list(self._get_blocked_ranges_in_row(
            row_index, min_index, max_index))
        if len(blocked_ranges) > 1:
            index = blocked_ranges[0][1] + 1
            return self._calculate_tuning_frequenzy(row_index, index)
        elif blocked_ranges[0][0] > 0:
            return self._calculate_tuning_frequenzy(row_index, 0)
        elif blocked_ranges[0][1] < max_index:
            return self._calculate_tuning_frequenzy(row_index, max_index)

    def _calculate_tuning_frequenzy(self, row_index, index):
        return 4000000 * index + row_index

    def count_blocked_tiles_in_row(self, row_to_count):
        blocked_ranges = self._get_blocked_ranges_in_row(
            row_to_count, float('-inf'), float('inf'))
        beacons = set([(beacon_row, beacon_column) for _, _, beacon_row,
                      beacon_column in self._pairs if beacon_row == row_to_count])

        blocked_ranges = [range(min, max+1) for min, max in blocked_ranges]
        blocked_tiles = set([(row_to_count, position)
                            for blocked_range in blocked_ranges for position in blocked_range])

        return len([position for position in blocked_tiles if position not in beacons])

    def _get_blocked_ranges_in_row(self, row_to_count, min_index, max_index):
        sensors_in_range = [(row, column, distance) for row, column, distance in self._sensor_ranges
                            if not (row_to_count < row - distance or row_to_count > row + distance)]

        results = [self._get_cells_in_sensor_distance_for_index_range(
            row, column, distance, row_to_count, min_index, max_index) for row, column, distance in sensors_in_range]

        blocked_ranges = [
            blocked_range for blocked_range in results if isinstance(blocked_range, tuple)]
        self._compress(blocked_ranges)
        return set(blocked_ranges)

    def _compress(self, blocked_ranges):
        working = True
        while working:
            working = False
            blocked_ranges.sort()
            for index in range(1, len(blocked_ranges)):
                last_range = blocked_ranges[index-1]
                current_range = blocked_ranges[index]

                # last end >= current start or last start >= current end
                if last_range[1] + 1 >= current_range[0] or last_range[0] >= current_range[1] + 1:
                    blocked_ranges[index] = (min(last_range[0], current_range[0]),
                                             max(last_range[1], current_range[1]))
                    blocked_ranges.remove(last_range)
                    working = True
                    break

    def _build_list(self, file_name):
        helpers.ensure_directory(os.path.dirname(__file__))
        for input_line in helpers.read_file(file_name):
            sensor_column, sensor_row, beacon_column, beacon_row = [
                int(point) for point in re.findall('(?<=x=)-?\d+|(?<=y=)-?\d+', input_line)]
            self._pairs.append((sensor_row, sensor_column,
                                beacon_row, beacon_column))
        self._sensor_ranges = list(self._get_sensor_ranges())

    def _get_cells_in_sensor_distance_for_index_range(self, sensor_row, sensor_column, distance, row_to_test, min_index, max_index):
        if row_to_test >= min_index and row_to_test <= max_index:
            return self._get_cells_in_sensor_distance(
                sensor_row, sensor_column, distance, row_to_test, min_index, max_index)

    def _get_cells_in_sensor_distance(
            self,
            sensor_row,
            sensor_column,
            distance,
            row_to_test,
            column_min,
            column_max):

        column_distance = 0
        column_distance = distance - (abs(sensor_row - row_to_test))
        return (max(sensor_column-column_distance, column_min), min(sensor_column+column_distance, column_max))

    def _get_sensor_ranges(self):
        for sensor_row, sensor_column, beacon_row, beacon_column in self._pairs:
            yield (sensor_row, sensor_column, self._calculate_manhattan_distance(sensor_row, sensor_column, beacon_row, beacon_column))

    def _calculate_manhattan_distance(self, row1, column1, row2, column2):
        return abs(row1 - row2) + abs(column1 - column2)


def run_day():
    print('Day15')
    grid_holder = GridHolder('input.txt')
    print(
        f'blocked cells in y=2000000: {grid_holder.count_blocked_tiles_in_row(2000000)}')
    start = datetime.now().strftime('%X.%f')
    frequenzy = grid_holder.find_tuning_frequency(0, 4000000)
    end = datetime.now().strftime('%X.%f')
    print(f'tuning frequency: {frequenzy}')
    print(f'{start} => {end} : {frequenzy}')
