from basics import helpers
import day12.task as task
from colorsys import hls_to_rgb
import time
import sys
import pygame
from pygame.locals import *

HEIGHT = 1000
WIDTH = 1800
FILE_NAME = 'input.txt'
CREATE_GIF = False


class App:
    def __init__(self):
        self.grid_holder = task.GridHolder(FILE_NAME)
        row_number = len(self.grid_holder.grid)
        column_number = len(self.grid_holder.grid[0])

        row_size = HEIGHT // row_number
        col_size = WIDTH // column_number

        self.cell_size = min(row_size, col_size)

        self.width = column_number * self.cell_size
        self.height = row_number * self.cell_size

        self.found_part1 = False
        self.found_part2 = False

        self.first_path = None
        self._running = False
        self._display = None
        self.size = self.width, self.height
        self._create_gif_frame_event = pygame.USEREVENT + 1

    def on_init(self):
        pygame.init()
        self._display = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._update_clock()
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == self._create_gif_frame_event:
            helpers.save_gif_frame(self._display)

    def on_loop(self):
        if self.found_part1 and self.found_part2:
            return

        self.grid_holder.run_step()

        if self.grid_holder.is_finished:
            print('has_failed: ' + str(self.grid_holder.has_failed))
            print('has_found_path: ' + str(self.grid_holder.has_found_path))
            print('steps: ' + str(len(self.grid_holder.path)))
            if not self.found_part1:
                print('finding shortest path')
                self.found_part1 = True
                self._save_path()
                self.grid_holder.setup_shortest_path()
            else:
                helpers.save_screenshot(self._display, 'screenshot.png')
                self.found_part2 = True

    def on_render(self):
        if not self.found_part1 or not self.found_part2:
            if len(self.grid_holder.touched_cells) > 0:
                for cell in self.grid_holder.touched_cells:
                    self._draw_cell(cell)
            else:
                self._draw()
        elif CREATE_GIF:
            self._create_gif()
            self._running = False

        self._update_clock()
        pygame.display.update()

    def on_cleanup(self):
        helpers.cleanup_gif_temp_dir()
        pygame.quit()
        sys.exit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        self._draw()
        if CREATE_GIF:
            pygame.time.set_timer(self._create_gif_frame_event, 100)
        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def _update_clock(self):
        pygame.display.set_caption(time.strftime("%H:%M:%S"))

    def _save_path(self):
        self.first_path = [(cell.x, cell.y) for cell in self.grid_holder.path]

    def _draw(self):
        for row in self.grid_holder.grid:
            for cell in row:
                self._draw_cell(cell)

    def _draw_cell(self, cell):
        xmin = cell.x * self.cell_size
        ymin = cell.y * self.cell_size

        if cell.is_start:
            base_color = (0, 1, 0)
        elif cell.is_end:
            base_color = (1, 0, 0)
        elif cell.is_path:
            base_color = hls_to_rgb(1/3, 1/3, 1)
        elif self.first_path != None and (cell.x, cell.y) in self.first_path:
            base_color = hls_to_rgb(0, 1/3, 1)
        else:
            base_color = hls_to_rgb(
                2/3 if cell.is_visited else 0, cell.height / 26, 1 if cell.is_visited else 0)

        color = helpers.rgb_float_to_int(base_color)

        rect = pygame.Rect(xmin, ymin, self.cell_size, self.cell_size)
        pygame.draw.rect(self._display, color, rect)

    def _create_gif(self):
        if not CREATE_GIF:
            return
        pygame.time.set_timer(self._create_gif_frame_event, 0)
        helpers.save_gif_frame(self._display)
        print('creating gif')
        helpers.create_gif('path')
        print('gif created')
        


if __name__ == '__main__':
    helpers.cleanup_gif_temp_dir()

    theApp = App()
    theApp.on_execute()
