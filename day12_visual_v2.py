import os
import shutil
import day12.task as task
from colorsys import hls_to_rgb
import time
import glob
from PIL import Image
import sys
import pygame
from pygame.locals import *

HEIGHT = 500
WIDTH = 1800
FILE_NAME = 'input'
TEMP_DIR = f'{os.getcwd()}/__gif_temp__'
CREATE_GIF = True


def from_rgb(rgb):
    return "#%02x%02x%02x" % (rgb_float_to_int(rgb))


def rgb_float_to_int(rgb):
    return int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)


def infert_rgb(rgb):
    return 1.0 - rgb[0], 1.0 - rgb[1], 1.0 - rgb[2]


class App:
    def __init__(self):
        self.grid_holder = task.GridHolder(FILE_NAME)
        row_number = len(self.grid_holder.grid)
        column_number = len(self.grid_holder.grid[0])

        self.cell_ids = []
        for _ in range(row_number):
            row = []
            for _ in range(column_number):
                row.append(None)
            self.cell_ids.append(row)

        row_size = HEIGHT // row_number
        col_size = WIDTH // column_number

        self.cell_size = min(row_size, col_size)

        self.width = column_number * self.cell_size
        self.height = row_number * self.cell_size

        self.found_part1 = False
        self.found_part2 = False
        self.first_path = None
        self.frame_counter = 0

        self._running = True
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
            self._save_gif_frame()

    def on_loop(self):
        if self.found_part1 and self.found_part2:
            return

        self.grid_holder.run_step()

        if self.grid_holder.is_finished:
            self._save()
            print('has_failed: ' + str(self.grid_holder.has_failed))
            print('has_found_path: ' + str(self.grid_holder.has_found_path))
            print('steps: ' + str(len(self.grid_holder.path)))
            if not self.found_part1:
                print('finding shortest path')
                self.found_part1 = True
                self._save_path()
                self.grid_holder.setup_shortest_path()
            else:
                self.found_part2 = True

    def on_render(self):
        if not self.found_part1 or not self.found_part2:
            if len(self.grid_holder.touched_cells) > 0:
                for cell in self.grid_holder.touched_cells:
                    self._draw_cell(cell)
            else:
                self._draw()
        else:
            self._create_gif()
            self._running = not CREATE_GIF

        #self._save_temp()
        self._update_clock()
        pygame.display.update()
        self.frame_counter += 1 if self._running else 0

    def on_cleanup(self):
        cleanup()
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
                self.cell_ids[cell.y][cell.x] = None
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

        color = rgb_float_to_int(base_color)

        rect = pygame.Rect(xmin, ymin, self.cell_size, self.cell_size)
        pygame.draw.rect(self._display, color, rect)

    def _save(self):
        pygame.image.save(self._display, 'screenshot.png')

    def _save_gif_frame(self,override=False):
        pygame.image.save(self._display, f'{TEMP_DIR}/{time.time()}.png')

    def _create_gif(self):
        if not CREATE_GIF:
            return
        pygame.time.set_timer(self._create_gif_frame_event, 0)
        self._save_gif_frame()
        
        frames = [Image.open(image)
                  for image in glob.glob(f'{TEMP_DIR}/*.png')]
        frame_one = frames[0]

        # 2 because: https://stackoverflow.com/questions/64473278/gif-frame-duration-seems-slower-than-expected
        frame_one.save('my_awesome.gif', format='GIF', append_images=frames,
                       save_all=True, optimize=True, duration=[2 for d in range(len(frames))] + [1000], loop=0)


def cleanup():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)

if __name__ == '__main__':
    cleanup()
    os.makedirs(TEMP_DIR)

    theApp = App()
    theApp.on_execute()
