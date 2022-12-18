import os
import shutil
import time
import pygame
import glob
from PIL import Image

TEMP_DIR = f'{os.getcwd()}/__gif_temp__'


def read_file(file_name: str, strip_space: bool = True) -> list:
    with open(file_name, 'r') as file:
        return [line.strip() if strip_space else line.strip('\n') for line in file]


def ensure_directory(directory: str):
    if (os.path.basename(os.getcwd()).lower() != directory.lower()):
        os.chdir(directory)


def from_rgb(rgb):
    return "#%02x%02x%02x" % (rgb_float_to_int(rgb))


def rgb_float_to_int(rgb):
    return int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)


def infert_rgb(rgb):
    return 1.0 - rgb[0], 1.0 - rgb[1], 1.0 - rgb[2]


def save_gif_frame(display: pygame.Surface):
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    save_screenshot(display, f'{TEMP_DIR}/{time.time()}')

def save_screenshot(display: pygame.Surface, file_name:str):
    pygame.image.save(display, f'{file_name}.png')

def create_gif(gif_name):
    frames = [Image.open(image)
              for image in glob.glob(f'{TEMP_DIR}/*.png')]
    frame_one = frames[0]

    # 2 because: https://stackoverflow.com/questions/64473278/gif-frame-duration-seems-slower-than-expected
    # last image is shown longer
    frame_one.save(f'{gif_name}.gif', format='GIF', append_images=frames,
                   save_all=True, optimize=True, duration=[2 for d in range(len(frames))] + [5000], loop=0)

def cleanup_gif_temp_dir():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
