from .context import basics as helpers
import os
from math import sqrt


INFINITY = float('inf')


class Cell():
    def __init__(self, x, y, height, is_start, is_end):
        self.x = x
        self.y = y
        self.height = height
        self.is_start = is_start
        self.is_end = is_end
        self.reset(is_start)

    def reset(self,is_start):
        self.is_visited = is_start
        self.is_current = is_start
        self.is_path = False
        self.g_score = 0 if is_start else INFINITY
        self.f_score = INFINITY
        self.came_from = None

    # h function
    def distance_to_cell(self, cell):
        return sqrt(((self.x - cell.x) ** 2) + ((self.y - cell.y) ** 2) + ((self.height - cell.height) ** 2))


class GridHolder():
    current_cell = None

    def __init__(self, file_name):
        helpers.ensure_directory(os.path.dirname(__file__))
        input_lines = helpers.read_file(file_name)
        self.grid = []
        self.reset()

        row = 0
        for input_line in input_lines:
            line = []
            column = 0
            for input_column in input_line:
                if input_column == 'S':
                    height = ord('a')-96
                elif input_column == 'E':
                    height = ord('z')-96
                else:
                    height = ord(input_column)-96
                cell = Cell(column, row, height,
                            input_column == 'S', input_column == 'E')
                line.append(cell)
                if input_column == 'S':
                    start = cell
                elif input_column == 'E':
                    self.end = cell
                column += 1
            self.grid.append(line)
            row += 1

        start.f_score = start.distance_to_cell(self.end)
        self.open_set = [start]

    def reset(self):
        self.touched_cells = set()
        self.steps = 0
        self.is_finished = False
        self.has_found_path = False
        self.has_failed = False
        self.path = None
        self.current_cell = None

    def find_path(self):
        while not self.is_finished:
            self.run_step()
        self.steps = len(self.path)

    def find_shortest_path(self):
        self.setup_shortest_path()
        while not self.is_finished:
            self.run_step()
        self.steps = len(self.path)

    def setup_shortest_path(self):
        self.reset()
        self.open_set = []
        for row in self.grid:
            for cell in row:
                if cell.x == 0:
                    cell.reset(True)
                    self.open_set.append(cell)
                    cell.f_score = cell.distance_to_cell(self.end)
                else:
                    cell.reset(False)

    def run_step(self):
        self.touched_cells = set()
        if self.is_finished:
            return

        if len(self.open_set) == 0:
            self.has_failed = True
            self.is_finished = True
            return

        self._get_current_cell()
        self._create_path(self.current_cell)

        if self.current_cell.is_end:
            self.has_found_path = True
            self.is_finished = True
            return

        for neighbor in self._get_neighbors(self.current_cell):
            # d(current,neighbor) is the weight (here distance) of the edge from current to neighbor
            # tentative_gScore is the distance from start to the neighbor through current
            tentative_g_score = self.current_cell.g_score + \
                neighbor.distance_to_cell(self.current_cell)
            if tentative_g_score < neighbor.g_score:
                # This path to neighbor is better than any previous one. Record it!
                neighbor.came_from = self.current_cell
                neighbor.g_score = tentative_g_score
                neighbor.f_score = tentative_g_score + \
                    neighbor.distance_to_cell(self.end)
                self.touched_cells.add(neighbor)
                if neighbor not in self.open_set:
                    self.open_set.append(neighbor)

    def _get_neighbors(self, cell):
        neighbors = []

        directions = [
            (0, -1),  # north
            (1, 0),  # east
            (0, 1),  # south
            (-1, 0),  # west
        ]

        for x, y in directions:
            x = cell.x + x
            y = cell.y + y
            if y < 0 or x < 0 or x >= (len(self.grid[0])) or y >= (len(self.grid)):
                continue

            neighbor = self.grid[y][x]
            if neighbor.height - cell.height <= 1 or neighbor.is_end:
                neighbors.append(neighbor)

        return neighbors

    def _get_current_cell(self):
        if self.current_cell != None:
            self.current_cell.is_current = False
            self.touched_cells.add(self.current_cell)

        self.open_set.sort(key=lambda cell: cell.f_score)
        self.current_cell = self.open_set.pop(0)
        self.touched_cells.add(self.current_cell)
        self.current_cell.is_current = True
        self.current_cell.is_visited = True

    def _create_path(self, cell):
        if self.path != None and len(self.path) > 0:
            for path_cell in self.path:
                path_cell.is_path = False
                self.touched_cells.add(path_cell)

        self.path = []
        current_cell = cell
        while current_cell.came_from != None:
            self.touched_cells.add(current_cell)
            self.path.append(current_cell)
            current_cell.is_path = True
            current_cell = current_cell.came_from


def run_day():
    print('Day12')
    grid_holder = GridHolder('input')
    grid_holder.find_path()
    print('steps: ' + str(grid_holder.steps))
    grid_holder.find_shortest_path()
    print('shortest path: ' + str(grid_holder.steps))
