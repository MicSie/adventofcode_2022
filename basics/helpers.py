import os


def read_file(file_name: str) -> list:
    with open(file_name, 'r') as file:
        return [line.strip() for line in file]


def ensure_directory(directory: str):
    if (os.path.basename(os.getcwd()).lower() != directory.lower()):
        os.chdir(directory)
