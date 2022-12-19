import os
import day15.task as task    # The code to test
import unittest   # The test framework
from .context import basics as helpers


class Test_day15(unittest.TestCase):
    def test_count_blocked_tiles_in_row(self):
        gridholder = task.GridHolder('testinput.txt')
        self.assertEqual(gridholder.count_blocked_tiles_in_row(10), 26)

    def test_find_tuning_frequency(self):
        gridholder = task.GridHolder('testinput.txt')
        self.assertEqual(gridholder.find_tuning_frequency(0, 20), 56000011)


if __name__ == '__main__':
    unittest.main()
