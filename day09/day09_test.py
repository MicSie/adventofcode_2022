import os
import day09.task as task    # The code to test
import unittest   # The test framework
from .context import basics as helpers


class Test_day09(unittest.TestCase):
    def test_move(self):
        head = task.Head((1,1))

        head.move("R 1")
        self.assertEqual(head.position, (1,2))
        self.assertEqual(head.tail.position, (1,1))

        head.move("L 2")
        self.assertEqual(head.position, (1,0))
        self.assertEqual(head.tail.position, (1,1))

        head.move("R 1")
        head.move("U 1")
        self.assertEqual(head.position, (2,1))
        self.assertEqual(head.tail.position, (1,1))

        head.move("D 2")
        self.assertEqual(head.position, (0,1))
        self.assertEqual(head.tail.position, (1,1))

        head = task.Head((1,1))
        head.move("R 2")
        self.assertEqual(head.position, (1,3))
        self.assertEqual(head.tail.position, (1,2))

        head = task.Head((1,1))
        head.move("U 2")
        self.assertEqual(head.position, (3,1))
        self.assertEqual(head.tail.position, (2,1))

    def test_diagonal(self):
        head = task.Head((1,1))

        head.move("R 1")
        head.move("U 1")
        self.assertEqual(head.position, (2,2))
        self.assertEqual(head.tail.position, (1,1))

        head.move("U 1")
        self.assertEqual(head.position, (3,2))
        self.assertEqual(head.tail.position, (2,2))

    def test_position_counter(self):
        head = task.Head()
        head.read_file('testinput.txt')

        self.assertEqual(len(head.tail.history), 13)

    def test_position_counter(self):
        head = task.Head()
        head.read_file('testinput.txt')
        self.assertEqual(len(head.get_last_tail().history), 1)

    def test_position_counter_new(self):
        head = task.Head()
        head.read_file('testinput2.txt')
        self.assertEqual(len(head.get_last_tail().history), 36)


if __name__ == '__main__':
    unittest.main()
