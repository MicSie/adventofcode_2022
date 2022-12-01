import day01    # The code to test
import unittest   # The test framework
import os


class Test_TestIncrementDecrement(unittest.TestCase):
    def test_Part1(self):
        os.chdir('day01')
        calories = day01.ReadCaloriesFromFile('testinput')
        self.assertEqual(day01.Part1(calories), 24000)

    def test_Part2(self):
        os.chdir('day01')
        calories = day01.ReadCaloriesFromFile('testinput')
        self.assertEqual(day01.Part2(calories), 45000)

    def test_ReadFile(self):
        os.chdir('day01')
        self.assertEqual(day01.ReadFile('simpletestfile'), [
            'first', '2dn', '', '4th'])

    def test_Sumlines(self):
      self.assertEqual(day01.SumLines(['5', '5', '', '20', '', '15', '5', '4', '1', '5', '']), [10,20,30])

    def test_Sumlines_MultipleEmptyLines(self):
      self.assertEqual(day01.SumLines(['5', '5', '', '', '20']), [10,20])


if __name__ == '__main__':
    unittest.main()
