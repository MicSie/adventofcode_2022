import day02.task as task    # The code to test
import unittest   # The test framework
from .context import basics as helpers


class Test_Day02(unittest.TestCase):

    def test_get_value(self):
        self.assertEqual(task.get_value('A'), 1)
        self.assertEqual(task.get_value('a'), 1)
        self.assertEqual(task.get_value('X'), 1)

        self.assertEqual(task.get_value('B'), 2)
        self.assertEqual(task.get_value('b'), 2)
        self.assertEqual(task.get_value('Y'), 2)

        self.assertEqual(task.get_value('C'), 3)
        self.assertEqual(task.get_value('c'), 3)
        self.assertEqual(task.get_value('Z'), 3)

    def test_fight(self):
        self.assertEqual(task.fight(task.ROCK, task.ROCK), 3)
        self.assertEqual(task.fight(task.ROCK, task.PAPER), 0)
        self.assertEqual(task.fight(task.ROCK, task.SCISSORS), 6)

        self.assertEqual(task.fight(task.PAPER, task.ROCK), 6)
        self.assertEqual(task.fight(task.PAPER, task.PAPER), 3)
        self.assertEqual(task.fight(task.PAPER, task.SCISSORS), 0)

        self.assertEqual(task.fight(task.SCISSORS, task.ROCK), 0)
        self.assertEqual(task.fight(task.SCISSORS, task.PAPER), 6)
        self.assertEqual(task.fight(task.SCISSORS, task.SCISSORS), 3)

    def test_caluclate_line(self):
        self.assertEqual(task.calulate_line_guest('A Y'), 8)
        self.assertEqual(task.calulate_line_guest('B X'), 1)
        self.assertEqual(task.calulate_line_guest('C Z'), 6)

    def test_read_score(self):
        helpers.ensure_directory('day02')
        self.assertEqual(task.calculate_score('testinput'), 15)

    def test_get_value_updated(self):
        self.test_get_value()
        self.assertEqual(task.get_value('X', False), 0)
        self.assertEqual(task.get_value('Y', False), 3)
        self.assertEqual(task.get_value('Z', False), 6)

    def test_read_guide(self):
        helpers.ensure_directory('day02')
        self.assertEqual(task.read_guide('testinput'), 12)


if __name__ == '__main__':
    unittest.main()
