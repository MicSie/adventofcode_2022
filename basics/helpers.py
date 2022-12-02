import os


def read_file(fileName: str) -> list:
    with open(fileName, 'r') as file:
        return [line.strip() for line in file]


def ensure_directory(directory: str):
    if (os.path.basename(os.getcwd()).lower() != directory.lower()):
        os.chdir(directory)
