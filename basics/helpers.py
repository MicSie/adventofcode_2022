import os


def read_file(file_name: str, strip_space:bool = True) -> list:
    with open(file_name, 'r') as file:
        return [line.strip() if strip_space else line.strip('\n') for line in file]


def ensure_directory(directory: str):
    if (os.path.basename(os.getcwd()).lower() != directory.lower()):
        os.chdir(directory)
