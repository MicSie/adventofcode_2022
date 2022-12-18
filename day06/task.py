from .context import basics as helpers
import os

def find_marker(data_line:str, unique_chars:int) -> int:
    buffer = [data for data in data_line[:unique_chars]]
    position = unique_chars
    for data in data_line[unique_chars:]:
        buffer.pop(0)
        buffer.append(data)
        position+=1
        if len(set(buffer)) == unique_chars:
            return position
    raise Exception('no marker found!')

def run_day():
    helpers.ensure_directory(os.path.dirname(__file__))
    message = helpers.read_file('input.txt')[0]
    print('Day06')
    print('data marker: ', find_marker(message, 4))
    print('message marker: ', find_marker(message, 14))
