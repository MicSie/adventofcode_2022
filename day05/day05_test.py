import day05.task as task    # The code to test
import unittest   # The test framework
from .context import basics as helpers
import os


class Test_Day05(unittest.TestCase):
    def _get_test_crates_and_instrucionts(self):
        helpers.ensure_directory(os.path.dirname(__file__))
        return task.split_crates_and_instructions(
            helpers.read_file('testinput.txt', False))

    def test_read_input(self):
        helpers.ensure_directory(os.path.dirname(__file__))
        crates_and_instrucionts = self._get_test_crates_and_instrucionts()

        self.assertEqual(len(crates_and_instrucionts), 2, 'tuple size')
        self.assertEqual(crates_and_instrucionts[0],
                         [
            '    [D]    ',
            '[N] [C]    ',
            '[Z] [M] [P]',
            ' 1   2   3 '
        ], 'crates')
        self.assertEqual(crates_and_instrucionts[1],
                         [
            'move 1 from 2 to 1',
            'move 3 from 1 to 3',
            'move 2 from 2 to 1',
            'move 1 from 1 to 2',
        ], 'instructions')

    def test_get_stack_count(self):
        self.assertEqual(task.get_stack_count(
            self._get_test_crates_and_instrucionts()[0]), 3)

    def test_read_stacks(self):
        stacks = task.read_stacks(self._get_test_crates_and_instrucionts()[0])
        self.assertEqual(len(stacks), 3, 'stack size')

        self.assertEqual(stacks[0], ['Z', 'N'], 'stack 1')
        self.assertEqual(stacks[1], ['M', 'C', 'D'], 'stack 2')
        self.assertEqual(stacks[2], ['P'], 'stack 3')

    def test_parse_instructions(self):
        instructions = task.parse_instructions(
            self._get_test_crates_and_instrucionts()[1])
        self.assertEqual(instructions[0], [1, 2, 1])
        self.assertEqual(instructions[1], [3, 1, 3])
        self.assertEqual(instructions[2], [2, 2, 1])
        self.assertEqual(instructions[3], [1, 1, 2])

        self.assertEqual(task.parse_instruction(
            'move 26 from 8 to 1'), [26, 8, 1])

    def test_execute_cratemover9000_instruction(self):
        stacks = task.read_stacks(self._get_test_crates_and_instrucionts()[0])
        task.execute_cratemover9000_instruction([1, 2, 1], stacks)
        self.assertEqual(stacks[0], ['Z', 'N', 'D'], 'stack 1')
        self.assertEqual(stacks[1], ['M', 'C'], 'stack 2')
        self.assertEqual(stacks[2], ['P'], 'stack 3')

        task.execute_cratemover9000_instruction([3, 1, 3], stacks)
        self.assertEqual(stacks[0], [], 'stack 1')
        self.assertEqual(stacks[1], ['M', 'C'], 'stack 2')
        self.assertEqual(stacks[2], ['P', 'D', 'N', 'Z'], 'stack 3')

        task.execute_cratemover9000_instruction([2, 2, 1], stacks)
        self.assertEqual(stacks[0], ['C', 'M'], 'stack 1')
        self.assertEqual(stacks[1], [], 'stack 2')
        self.assertEqual(stacks[2], ['P', 'D', 'N', 'Z'], 'stack 3')

        task.execute_cratemover9000_instruction([1, 1, 2], stacks)
        self.assertEqual(stacks[0], ['C'], 'stack 1')
        self.assertEqual(stacks[1], ['M'], 'stack 2')
        self.assertEqual(stacks[2], ['P', 'D', 'N', 'Z'], 'stack 3')

    def test_execute_cratemover9001_instruction(self):
        stacks = task.read_stacks(self._get_test_crates_and_instrucionts()[0])
        task.execute_cratemover9001_instruction([1, 2, 1], stacks)
        self.assertEqual(stacks[0], ['Z', 'N', 'D'], 'stack 1')
        self.assertEqual(stacks[1], ['M', 'C'], 'stack 2')
        self.assertEqual(stacks[2], ['P'], 'stack 3')

        task.execute_cratemover9001_instruction([3, 1, 3], stacks)
        self.assertEqual(stacks[0], [], 'stack 1')
        self.assertEqual(stacks[1], ['M', 'C'], 'stack 2')
        self.assertEqual(stacks[2], ['P', 'Z', 'N', 'D'], 'stack 3')

        task.execute_cratemover9001_instruction([2, 2, 1], stacks)
        self.assertEqual(stacks[0], ['M', 'C'], 'stack 1')
        self.assertEqual(stacks[1], [], 'stack 2')
        self.assertEqual(stacks[2], ['P', 'Z', 'N', 'D'], 'stack 3')

        task.execute_cratemover9001_instruction([1, 1, 2], stacks)
        self.assertEqual(stacks[0], ['M'], 'stack 1')
        self.assertEqual(stacks[1], ['C'], 'stack 2')
        self.assertEqual(stacks[2], ['P', 'Z', 'N', 'D'], 'stack 3')

    def test_cratemover9000(self):
        helpers.ensure_directory(os.path.dirname(__file__))
        self.assertEqual(task.run_createmover9000('testinput.txt'), 'CMZ')

    def test_cratemover9001(self):
        helpers.ensure_directory(os.path.dirname(__file__))
        self.assertEqual(task.run_createmover9001('testinput.txt'), 'MCD')


if __name__ == '__main__':
    unittest.main()
