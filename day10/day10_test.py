import os
import day10.task as task    # The code to test
import unittest   # The test framework
from .context import basics as helpers


class Test_day10(unittest.TestCase):
    def test_run_instrctions(self):
        input = ["noop","addx 3","addx -5"]
        history = task.execute_instructions(input)
        self.assertEqual(len(history), 6)
        self.assertEqual(history[0],1) # init
        self.assertEqual(history[1],1) # noop
        self.assertEqual(history[2],1) # addx 3
        self.assertEqual(history[3],4) # addx 3
        self.assertEqual(history[4],4) # addx -5
        self.assertEqual(history[5],-1) # addx -5

    def test_parse_file(self):
        history = task.parse_file('testinput')
        
        self.assertEqual(history[20-1], 21)
        self.assertEqual(history[60-1], 19)
        self.assertEqual(history[100-1], 18)
        self.assertEqual(history[140-1], 21)
        self.assertEqual(history[180-1], 16)
        self.assertEqual(history[220-1], 18)

        self.assertEqual(task.calulate_strength(history), 13140)

    def test_screen(self):
        history = task.parse_file('testinput')
        screen = task.calculate_screen(history)

        self.assertEqual(screen[0], '##..##..##..##..##..##..##..##..##..##..')
        self.assertEqual(screen[1], '###...###...###...###...###...###...###.')
        self.assertEqual(screen[2], '####....####....####....####....####....')
        self.assertEqual(screen[3], '#####.....#####.....#####.....#####.....')
        self.assertEqual(screen[4], '######......######......######......####')
        self.assertEqual(screen[5], '#######.......#######.......#######.....')

if __name__ == '__main__':
    unittest.main()
