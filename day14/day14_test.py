import os
import day14.task as task    # The code to test
import unittest   # The test framework
from .context import basics as helpers


class Test_day14(unittest.TestCase):
    def test_parse_input(self):
        gridholder = task.GridHolder('testinput.txt')

        self.assertTrue(gridholder.grid[0][500].is_start)

        self.assertTrue(gridholder.grid[4][498].is_wall)
        self.assertTrue(gridholder.grid[5][498].is_wall)
        self.assertTrue(gridholder.grid[6][498].is_wall)
        self.assertTrue(gridholder.grid[6][497].is_wall)
        self.assertTrue(gridholder.grid[6][496].is_wall)

        self.assertTrue(gridholder.grid[4][503].is_wall)
        self.assertTrue(gridholder.grid[4][502].is_wall)
        self.assertTrue(gridholder.grid[5][502].is_wall)
        self.assertTrue(gridholder.grid[6][502].is_wall)
        self.assertTrue(gridholder.grid[7][502].is_wall)
        self.assertTrue(gridholder.grid[8][502].is_wall)
        self.assertTrue(gridholder.grid[9][502].is_wall)
        self.assertTrue(gridholder.grid[9][501].is_wall)
        self.assertTrue(gridholder.grid[9][500].is_wall)
        self.assertTrue(gridholder.grid[9][499].is_wall)
        self.assertTrue(gridholder.grid[9][498].is_wall)
        self.assertTrue(gridholder.grid[9][497].is_wall)
        self.assertTrue(gridholder.grid[9][496].is_wall)
        self.assertTrue(gridholder.grid[9][495].is_wall)
        self.assertTrue(gridholder.grid[9][494].is_wall)

    def test_count_sand_abyss(self):
        gridholder = task.GridHolder('testinput.txt', True)
        gridholder.count_sand()
        self.assertEqual(gridholder.abyss_sand_counter, 24)

    def test_count_sand_filled(self):
        gridholder = task.GridHolder('testinput.txt', True)
        gridholder.count_sand()
        self.assertEqual(gridholder.filled_sand_counter, 93)

if __name__ == '__main__':
    unittest.main()
