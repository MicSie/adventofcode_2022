import day03.task as task    # The code to test
import unittest   # The test framework
from .context import basics as helpers


class Test_Day03(unittest.TestCase):
    def test_get_item_value(self):
        self.assertEqual(task.get_item_value('a'), 1)
        self.assertEqual(task.get_item_value('z'), 26)
        self.assertEqual(task.get_item_value('A'), 27)
        self.assertEqual(task.get_item_value('Z'), 52)

        self.assertEqual(task.get_item_value('p'), 16)
        self.assertEqual(task.get_item_value('L'), 38)
        self.assertEqual(task.get_item_value('P'), 42)
        self.assertEqual(task.get_item_value('v'), 22)
        self.assertEqual(task.get_item_value('t'), 20)
        self.assertEqual(task.get_item_value('s'), 19)

    def test_find_duplicate(self):
        self.assertEqual(task.find_duplicate('vJrwpWtwJgWrhcsFMMfFFhFp'), 'p')
        self.assertEqual(task.find_duplicate(
            'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL'), 'L')
        self.assertEqual(task.find_duplicate('PmmdzqPrVvPwwTWBwg'), 'P')
        self.assertEqual(task.find_duplicate(
            'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn'), 'v')
        self.assertEqual(task.find_duplicate('ttgJtRGJQctTZtZT'), 't')
        self.assertEqual(task.find_duplicate('CrZsJsPPZsGzwwsLwLmpwMDw'), 's')

    def test_read_priority(self):
        helpers.ensure_directory('day03')
        self.assertEqual(task.read_priority('testinput'), 157)

    def test_find_group_items(self):
        helpers.ensure_directory('day03')
        self.assertEqual(task.find_group_items(
            helpers.read_file('testinput')), ['r', 'Z'])

    def test_read_group_priority(self):
        helpers.ensure_directory('day03')
        self.assertEqual(task.read_group_priority('testinput'), 70)


if __name__ == '__main__':
    unittest.main()
