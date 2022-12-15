import day12.task as task
from colorsys import hls_to_rgb
from tkinter import Canvas, Tk
import time
from PIL import Image, ImageDraw

HEIGHT = 500
WIDTH = 1800
FILE_NAME = 'input'
PAUSE = 1


def from_rgb(rgb):
    return "#%02x%02x%02x" % (rgb_float_to_int(rgb))


def rgb_float_to_int(rgb):
    return int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)


def infert_rgb(rgb):
    return 1.0 - rgb[0], 1.0 - rgb[1], 1.0 - rgb[2]


class CellGridCanvas(Canvas):
    def __init__(self, master, *args, **kwargs):
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
        Canvas.__init__(self, master, width=self.width,
                        height=self.height, *args, **kwargs)

        self.found_part1 = False
        self.found_part2 = False
        self.draw()
        self.update_clock()
        self.update_draw_step()

    def update_draw_step(self):
        self.grid_holder.run_step()

        for cell in self.grid_holder.touched_cells:
            self.draw_cell(cell)

        if self.grid_holder.is_finished:
            self.save()
            print('has_failed: ' + str(self.grid_holder.has_failed))
            print('has_found_path: ' + str(self.grid_holder.has_found_path))
            print('steps: ' + str(len(self.grid_holder.path)))
            if not self.found_part1:
                print('finding shortest path')
                self.found_part1 = True
                self.save_path()
                self.grid_holder.setup_shortest_path()
                self.draw()
            else:
                self.found_part2 = True

        if self.found_part1 and self.found_part2:
            self.save()
        else:
            self.master.after(PAUSE, self.update_draw_step)

    first_path = None

    def save_path(self):
        self.first_path = [(cell.x, cell.y) for cell in self.grid_holder.path]

    def save(self):
        print('saving')
        self.draw_image().save('day12.png')
        print('saved')

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.master.title(now)
        self.master.after(1000, self.update_clock)

    def draw(self):
        self.delete("all")  # clear all elements
        for row in self.grid_holder.grid:
            for cell in row:
                self.cell_ids[cell.y][cell.x] = None
                self.draw_cell(cell)

    def draw_image(self):
        image = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(image)
        for row in self.grid_holder.grid:
            for cell in row:
                self.draw_cell(cell, draw)

        return image

    def draw_cell(self, cell, draw=None):
        xmin = cell.x * self.cell_size
        xmax = xmin + self.cell_size - 1
        ymin = cell.y * self.cell_size
        ymax = ymin + self.cell_size - 1

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

        color = from_rgb(base_color)

        if draw != None:
            draw.rectangle(
                [(xmin, ymin), (xmax, ymax)], fill=color, outline=color)
            return

        self.delete('current_cell')

        if self.cell_ids[cell.y][cell.x] == None:
            self.cell_ids[cell.y][cell.x] = self.create_rectangle(xmin, ymin, xmax, ymax,
                                                                  fill=color, outline=color)
        else:
            for item in self.find_withtag(self.cell_ids[cell.y][cell.x]):
                self.itemconfigure(item, fill=color, outline=color)

        if cell.is_current:
            other_color = from_rgb(hls_to_rgb(0, 1/3, 1))
            self.create_oval(xmin, ymin, xmax, ymax,
                             fill=other_color, outline=other_color, tags='current_cell')


if __name__ == "__main__":
    app = Tk()

    grid = CellGridCanvas(app)
    grid.pack(padx=1, pady=1)
    
    app.mainloop()
