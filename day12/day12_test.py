import os
import day12.task as task    # The code to test
import unittest   # The test framework
from .context import basics as helpers


class Test_day12(unittest.TestCase):
    def test_steps(self):
        grid_holder = task.GridHolder('testinput.txt')
        grid_holder.find_path()

        self.assertTrue(grid_holder.has_found_path)
        self.assertEqual(grid_holder.steps, 31)
    def test_shortest_path(self):

        grid_holder = task.GridHolder('testinput.txt')
        grid_holder.find_shortest_path()

        self.assertTrue(grid_holder.has_found_path)
        self.assertEqual(grid_holder.steps, 29)
    
    def test_input(self):
        grid_holder = task.GridHolder('input.txt')
        grid_holder.find_path()
        self.assertTrue(grid_holder.has_found_path)
        self.assertEqual(grid_holder.steps, 440)

        grid_holder.find_shortest_path()
        self.assertTrue(grid_holder.has_found_path)
        self.assertEqual(grid_holder.steps, 439)

if __name__ == '__main__':
    unittest.main()
