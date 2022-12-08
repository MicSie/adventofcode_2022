import os
import day08.task as task    # The code to test
import unittest   # The test framework
from .context import basics as helpers


class Test_day08(unittest.TestCase):
    def test_pasing_input(self):
        self.assertEqual(task.parse_file('testinput'),
                         [[3, 0, 3, 7, 3],
                          [2, 5, 5, 1, 2],
                          [6, 5, 3, 3, 2],
                          [3, 3, 5, 4, 9],
                          [3, 5, 3, 9, 0]])

    def test_count_tree_lines(self):
        trees = task.parse_file('testinput')
        result = task.calculate_visibility(trees)
        expected = [[[task.LEFT, task.TOP], [task.TOP], [task.TOP], [task.LEFT, task.TOP, task.RIGHT], [task.TOP, task.RIGHT]],
                    [[task.LEFT], [task.LEFT, task.TOP], [
                        task.TOP, task.RIGHT], [], [task.RIGHT]],
                    [[task.LEFT, task.TOP, task.RIGHT, task.BOTTOM], [
                        task.RIGHT], [], [task.RIGHT], [task.RIGHT]],
                    [[task.LEFT], [], [task.LEFT, task.BOTTOM], [], [
                        task.LEFT, task.TOP, task.RIGHT, task.BOTTOM]],
                    [[task.LEFT, task.BOTTOM], [task.LEFT, task.BOTTOM], [task.BOTTOM], [task.LEFT, task.TOP, task.RIGHT, task.BOTTOM], [task.RIGHT, task.BOTTOM]]]

        for index in range(len(expected)):
            self.assertEqual(result[index], expected[index])

    def test_count_trees(self):
        trees = task.parse_file('testinput')
        self.assertEqual(task.count_trees(trees), 21)

    def test_get_scenic_score(self):
        trees = task.parse_file('testinput')
        self.assertEqual(task.get_scenic_score(trees, 1, 2), 4)
        self.assertEqual(task.get_scenic_score(trees, 3, 2), 8)

    def test_get_max_scenic_score(self):
        trees = task.parse_file('testinput')
        self.assertEqual(task.get_max_scenic_score(trees), 8)


if __name__ == '__main__':
    unittest.main()
