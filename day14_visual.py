from datetime import datetime
from basics import helpers
import day14.task as task
import sys
import pygame
from pygame.locals import *

HEIGHT = 1000
WIDTH = 1800
FILE_NAME = 'input.txt'
CREATE_GIF = True
SHOW_GRID = False

COLOR_SAND = (233, 191, 141)
COLOR_FALING_SAND = (176, 138, 110)
COLOR_WALL = (171, 166, 170)


class App:
    def __init__(self):
        self.grid_holder = task.GridHolder(FILE_NAME, True)
        row_number = len(self.grid_holder.grid)
        column_number = len(self.grid_holder.grid[0])

        row_size = HEIGHT // row_number
        col_size = WIDTH // column_number

        self._cell_size = min(row_size, col_size)

        self.width = column_number * self._cell_size
        self.height = row_number * self._cell_size

        self._running = False
        self._display = None
        self._created_gif = False
        self.size = self.width, self.height
        self._create_gif_frame_event = pygame.USEREVENT + 1
        self._update_clock_event = pygame.USEREVENT + 2

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
        elif event.type == self._update_clock_event:
            self._update_clock()

    def on_loop(self):
        if not self.grid_holder.done:
            self.grid_holder.run_cycle()

    def on_render(self):
        if not self.grid_holder.done:
            for row, column in self.grid_holder.current_path:
                self._draw_cell(self.grid_holder.grid[row][column], row, column)
            pygame.display.update()
        else:
            self._create_gif()

    def on_cleanup(self):
        helpers.cleanup_gif_temp_dir()
        pygame.quit()
        sys.exit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        if CREATE_GIF:
            pygame.time.set_timer(self._create_gif_frame_event, 100)

        pygame.time.set_timer(self._update_clock_event, 500)
        self._draw()
        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def _update_clock(self):
        pygame.display.set_caption(datetime.now().strftime('%X.%f'))

    def _draw(self):
        row_index = 0
        for row in self.grid_holder.grid:
            column_index = 0
            for cell in row:
                self._draw_cell(cell, row_index, column_index)
                column_index += 1
            row_index += 1

    def _draw_cell(self, cell, row, column):
        x_min = column * self._cell_size
        x_center = x_min + (self._cell_size//2)
        x_max = x_min + self._cell_size
        y_min = row * self._cell_size
        y_center = y_min + (self._cell_size//2)
        y_max = y_min + self._cell_size

        if SHOW_GRID:
            rect = pygame.Rect(x_min, y_min, self._cell_size, self._cell_size)
            pygame.draw.rect(self._display, (255, 255, 255), rect, 1)

        if cell.is_start:
            pygame.draw.polygon(self._display, COLOR_FALING_SAND, [
                                (x_min, y_min), (x_max, y_min), (x_center,  y_max)])
        elif cell.is_wall:
            rect = pygame.Rect(x_min, y_min, self._cell_size, self._cell_size)
            pygame.draw.rect(self._display, COLOR_WALL, rect)
        elif cell.is_sand:
            pygame.draw.circle(self._display, COLOR_SAND,
                               (x_center, y_center), self._cell_size//2)
        elif (row, column) in self.grid_holder.current_path:
            pygame.draw.circle(self._display, COLOR_FALING_SAND, (x_center,
                               y_center), self._cell_size//2, max(1, self._cell_size//8))

    def _create_gif(self):
        if not CREATE_GIF or self._created_gif:
            return
        pygame.time.set_timer(self._create_gif_frame_event, 0)
        helpers.save_gif_frame(self._display)
        print('creating gif')
        helpers.create_gif('sand')
        print('gif created')
        self._created_gif = True


if __name__ == '__main__':
    helpers.cleanup_gif_temp_dir()

    theApp = App()
    theApp.on_execute()
