import os
import day13.task as task    # The code to test
import unittest   # The test framework
from .context import basics as helpers


class Test_day13(unittest.TestCase):
    def test_parse_line(self):
        self.assertEqual(task.parse_line('[1,1,3,1,1]'), [1, 1, 3, 1, 1])
        self.assertEqual(task.parse_line('[1,[2,[3,[4,[5,6,7]]]],8,9]'), [
                         1, [2, [3, [4, [5, 6, 7]]]], 8, 9])
        self.assertEqual(task.parse_line('[[1],[2,3,4]]'), [[1], [2, 3, 4]])
        self.assertEqual(task.parse_line('[[8,7,6]]'), [[8, 7, 6]])
        self.assertEqual(task.parse_line('[[4,4],4,4]'), [[4, 4], 4, 4])
        self.assertEqual(task.parse_line('[]'), [])
        self.assertEqual(task.parse_line('[[[]]]'), [[[]]])

    def test_compare_pair(self):
        pairs = task.read_file('testinput')
        self.assertEqual(len(pairs), 8)

        self.assertTrue(task.is_in_order(pairs[0]))
        self.assertTrue(task.is_in_order(pairs[1]))
        self.assertFalse(task.is_in_order(pairs[2]))
        self.assertTrue(task.is_in_order(pairs[3]))
        self.assertFalse(task.is_in_order(pairs[4]))
        self.assertTrue(task.is_in_order(pairs[5]))
        self.assertFalse(task.is_in_order(pairs[6]))
        self.assertFalse(task.is_in_order(pairs[7]))

    def test_sum_indices(self):
        pairs = task.read_file('testinput')
        self.assertEqual(task.sum_indices(pairs), 13)

    def test_insert_divider_packets_and_redorder(self):
        expected_order = [[],
                          [[]],
                          [[[]]],
                          [1, 1, 3, 1, 1],
                          [1, 1, 5, 1, 1],
                          [[1], [2, 3, 4]],
                          [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
                          [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
                          [[1], 4],
                          [[2]],
                          [3],
                          [[4, 4], 4, 4],
                          [[4, 4], 4, 4, 4],
                          [[6]],
                          [7, 7, 7],
                          [7, 7, 7, 7],
                          [[8, 7, 6]],
                          [9]]

        pairs = task.read_file('testinput')
        ordered_list = task.insert_divider_packets_and_redorder(pairs)

        self.assertEqual(ordered_list, expected_order)

    def test_calculate_decoder_key(self):
        pairs = task.read_file('testinput')
        self.assertEqual(task.calculate_decoder_key(pairs), 140)


if __name__ == '__main__':
    unittest.main()
