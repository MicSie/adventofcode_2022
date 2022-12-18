import day04.task as task    # The code to test
import unittest   # The test framework
from .context import basics as helpers

TEST_DATA = [
    ['2-4', '6-8'],
    ['2-3', '4-5'],
    ['5-7', '7-9'],
    ['2-8', '3-7'],
    ['6-6', '4-6'],
    ['2-6', '4-8']
]


class Test_Day04(unittest.TestCase):
    def test_contains(self):
        self.assertFalse(task.contains(TEST_DATA[0]))
        self.assertFalse(task.contains(TEST_DATA[1]))
        self.assertFalse(task.contains(TEST_DATA[2]))
        self.assertTrue(task.contains(TEST_DATA[3]))
        self.assertTrue(task.contains(TEST_DATA[4]))
        self.assertFalse(task.contains(TEST_DATA[5]))

    def test_count_fully_contained_assignments(self):
        helpers.ensure_directory('day04')
        self.assertEqual(
            task.count_fully_contained_assignments('testinput.txt'), 2)

    def test_overlaps(self):
        self.assertFalse(task.overlaps(TEST_DATA[0]))
        self.assertFalse(task.overlaps(TEST_DATA[1]))
        self.assertTrue(task.overlaps(TEST_DATA[2]))
        self.assertTrue(task. overlaps(TEST_DATA[3]))
        self.assertTrue(task. overlaps(TEST_DATA[4]))
        self.assertTrue(task.overlaps(TEST_DATA[5]))

    def test_count_overlaping_assignments(self):
        helpers.ensure_directory('day04')
        self.assertEqual(
            task.count_overlaping_assignments('testinput.txt'), 4)

if __name__ == '__main__':
    unittest.main()
