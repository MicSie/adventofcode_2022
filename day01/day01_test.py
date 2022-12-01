import day01    # The code to test
import unittest   # The test framework
import os


class Test_TestIncrementDecrement(unittest.TestCase):
    def test_part1(self):
        os.chdir('day01')
        calories = day01.read_calories_from_file('testinput')
        self.assertEqual(day01.part1(calories), 24000)

    def test_part2(self):
        os.chdir('day01')
        calories = day01.read_calories_from_file('testinput')
        self.assertEqual(day01.part2(calories), 45000)

    def test_read_file(self):
        os.chdir('day01')
        self.assertEqual(day01.read_file('simpletestfile'), [
            'first', '2dn', '', '4th'])

    def test_sum_lines(self):
      self.assertEqual(day01.sum_lines(['5', '5', '', '20', '', '15', '5', '4', '1', '5', '']), [10,20,30])

    def test_sum_lines_multiple_empty_lines(self):
      self.assertEqual(day01.sum_lines(['5', '5', '', '', '20']), [10,20])


if __name__ == '__main__':
    unittest.main()
