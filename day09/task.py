from .context import basics as helpers
import os
import re


class Head():
    position = None
    tail = None

    def __init__(self, starting: tuple = (0, 0)) -> None:
        self.position = starting
        self.tail = Tail(starting)

    def read_file(self, file_name:str) -> None:
        helpers.ensure_directory(os.path.dirname(__file__))
        [self.move(line) for line in helpers.read_file(file_name)]

    def move(self, instruction: str) -> None:
        direction, steps = instruction.split(' ')
        movement = {
            'R':(0,1),
            'L':(0,-1),
            'U':(1,0),
            'D':(-1,0),
        }.get(direction)

        for step in range(int(steps)):
            self.position = (self.position[0] + movement[0], self.position[1] + movement[1])
            self.tail.follow(self.position)

    def get_last_tail(self):
        tail = self.tail
        while not tail.tail is None:
            tail = tail.tail
        return tail


class Tail():
    position = None
    history = None
    number = 0
    tail = None

    def __init__(self, starting: tuple = (0, 0), number:int = 1) -> None:
        self.position = starting
        self.history = set()
        self.history.add(starting)
        self.number = number
        if number < 9 :
            self.tail = Tail(starting, number + 1)

    def follow(self, new_positon:tuple):
        if new_positon == self.position:
            return

        vertical_distance =  self.position[0] - new_positon[0]
        horizontal_distance = self.position[1] - new_positon[1]

        if abs(vertical_distance) < 2 and abs(horizontal_distance) < 2:
            return

        if vertical_distance != 0 and horizontal_distance != 0:
            self.position = (self.position[0] + 1  if vertical_distance < 0 else self.position[0] - 1, self.position[1] + 1  if horizontal_distance < 0 else self.position[1] - 1)
        elif vertical_distance != 0:
            self.position = (self.position[0] + 1  if vertical_distance < 0 else self.position[0] - 1, self.position[1])
        elif horizontal_distance != 0:
            self.position = (self.position[0], self.position[1] + 1  if horizontal_distance < 0 else self.position[1] - 1)

        self.history.add(self.position)
        if self.tail is not None:
            self.tail.follow(self.position)

def run_day():
    print('Day09')
    head = Head()
    head.read_file('input.txt')
    print('step couter: ' + str(len(head.tail.history)))
    print('step couter 9th knot: ' + str(len(head.get_last_tail().history)))
