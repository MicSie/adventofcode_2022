import day01.task as task   # The code to test
import unittest   # The test framework
from .context import basics as helpers


class Test_Day01(unittest.TestCase):

    def test_part1(self):
        helpers.ensure_directory('day01')
        calories = task.read_calories_from_file('testinput')
        self.assertEqual(task.part1(calories), 24000)

    def test_part2(self):
        helpers.ensure_directory('day01')
        calories = task.read_calories_from_file('testinput')
        self.assertEqual(task.part2(calories), 45000)

    def test_sum_lines(self):
        self.assertEqual(task.sum_lines(
            ['5', '5', '', '20', '', '15', '5', '4', '1', '5', '']), [10, 20, 30])

    def test_sum_lines_multiple_empty_lines(self):
        self.assertEqual(task.sum_lines(['5', '5', '', '', '20']), [10, 20])


if __name__ == '__main__':
    unittest.main()
