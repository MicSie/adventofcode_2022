import os
import day11.task as task    # The code to test
import unittest   # The test framework
from .context import basics as helpers


class Test_day11(unittest.TestCase):
    def _get_test_monkeys(self, worry: bool = True) -> list[task.Monkey]:
        monkeys = [task.Monkey() for i in range(4)]

        monkeys[0].items = [79, 98]
        monkeys[0].operation = lambda old: old * 19
        monkeys[0].devisor = 23
        monkeys[0].true_target = 2
        monkeys[0].false_target = 3
        monkeys[0].worry = worry

        monkeys[1].items = [54, 65, 75, 74]
        monkeys[1].operation = lambda old: old + 6
        monkeys[1].devisor = 19
        monkeys[1].true_target = 2
        monkeys[1].false_target = 0
        monkeys[1].worry = worry

        monkeys[2].items = [79, 60, 97]
        monkeys[2].operation = lambda old: old * old
        monkeys[2].devisor = 13
        monkeys[2].true_target = 1
        monkeys[2].false_target = 3
        monkeys[2].worry = worry

        monkeys[3].items = [74]
        monkeys[3].operation = lambda old: old + 3
        monkeys[3].devisor = 17
        monkeys[3].true_target = 0
        monkeys[3].false_target = 1
        monkeys[3].worry = worry

        return monkeys

    def test_monkey0(self):
        monkey = self._get_test_monkeys()[0]
        result = monkey.inspect_items()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], (3, 500))
        self.assertEqual(result[1], (3, 620))

    def test_play_round(self):
        monkeys = self._get_test_monkeys()
        task.play_rounds(monkeys, 1)
        self.assertEqual(monkeys[0].items, [20, 23, 27, 26])
        self.assertEqual(monkeys[1].items, [2080, 25, 167, 207, 401, 1046])
        self.assertEqual(len(monkeys[2].items), 0)
        self.assertEqual(len(monkeys[3].items), 0)

    def test_play_rounds(self):
        monkeys = self._get_test_monkeys()
        task.play_rounds(monkeys, 20)
        self.assertEqual(monkeys[0].items, [10, 12, 14, 26, 34])
        self.assertEqual(monkeys[1].items, [245, 93, 53, 199, 115])
        self.assertEqual(len(monkeys[2].items), 0)
        self.assertEqual(len(monkeys[3].items), 0)

    def test_monkey_business(self):
        monkeys = self._get_test_monkeys()
        self.assertEqual(task.monkey_business(monkeys, 20), 10_605)

    def test_no_worry_monkey_business(self):
        monkeys = self._get_test_monkeys(False)
        self.assertEqual(task.monkey_business(monkeys, 20), 10_197)

    def test_big_monkey_business(self):
        monkeys = self._get_test_monkeys(False)
        self.assertEqual(task.monkey_business(monkeys, 10_000), 2713310158)


if __name__ == '__main__':
    unittest.main()
