from functools import reduce
from .context import basics as helpers
import os
import re


class Monkey():
    items = []
    operation = None
    true_target = None
    false_target = None
    devisor = None
    inspection_counter = 0
    worry = True
    max_value = None

    def give_item(self, item: int) -> None:
        self.items.append(item)

    def inspect_items(self) -> list[tuple[int]]:
        result = []
        while len(self.items) > 0:
            item = self.items.pop(0)
            item = self.operation(item)
            if self.worry:
                item = item // 3
            else:
                item = item % self.max_value
            if item % self.devisor == 0:
                result.append((self.true_target, item))
            else:
                result.append((self.false_target, item))
            self.inspection_counter += 1

        return result


def play_rounds(monkeys: list[Monkey], rounds) -> None:
    for round_number in range(rounds):
        for monkey in monkeys:
            for passing in monkey.inspect_items():
                monkeys[passing[0]].give_item(passing[1])


def monkey_business(monkeys: list[Monkey], rounds: int) -> int:
    update_max_value(monkeys)
    play_rounds(monkeys, rounds)
    counter = [monkey.inspection_counter for monkey in monkeys]
    counter.sort(reverse=True)
    return counter[0] * counter[1]


def _get_monkeys(worry: bool = True) -> list[Monkey]:
    monkeys = [Monkey() for i in range(8)]

    monkeys[0].items = [63, 84, 80, 83, 84, 53, 88, 72]
    monkeys[0].operation = lambda old:  old * 11
    monkeys[0].devisor = 13
    monkeys[0].true_target = 4
    monkeys[0].false_target = 7
    monkeys[0].worry = worry

    monkeys[1].items = [67, 56, 92, 88, 84]
    monkeys[1].operation = lambda old:  old + 4
    monkeys[1].devisor = 11
    monkeys[1].true_target = 5
    monkeys[1].false_target = 3
    monkeys[1].worry = worry

    monkeys[2].items = [52]
    monkeys[2].operation = lambda old:  old * old
    monkeys[2].devisor = 2
    monkeys[2].true_target = 3
    monkeys[2].false_target = 1
    monkeys[2].worry = worry

    monkeys[3].items = [59, 53, 60, 92, 69, 72]
    monkeys[3].operation = lambda old:  old + 2
    monkeys[3].devisor = 5
    monkeys[3].true_target = 5
    monkeys[3].false_target = 6
    monkeys[3].worry = worry

    monkeys[4].items = [61, 52, 55, 61]
    monkeys[4].operation = lambda old:  old + 3
    monkeys[4].devisor = 7
    monkeys[4].true_target = 7
    monkeys[4].false_target = 2
    monkeys[4].worry = worry

    monkeys[5].items = [79, 53]
    monkeys[5].operation = lambda old:  old + 1
    monkeys[5].devisor = 3
    monkeys[5].true_target = 0
    monkeys[5].false_target = 6
    monkeys[5].worry = worry

    monkeys[6].items = [59, 86, 67, 95, 92, 77, 91]
    monkeys[6].operation = lambda old:  old + 5
    monkeys[6].devisor = 19
    monkeys[6].true_target = 4
    monkeys[6].false_target = 0
    monkeys[6].worry = worry

    monkeys[7].items = [58, 83, 89]
    monkeys[7].operation = lambda old:  old * 19
    monkeys[7].devisor = 17
    monkeys[7].true_target = 2
    monkeys[7].false_target = 1
    monkeys[7].worry = worry

    return monkeys


def update_max_value(monkeys):
    max_value = reduce(
        lambda x, y: x*y, [monkey.devisor for monkey in monkeys])
    for monkey in monkeys:
        monkey.max_value = max_value


def run_day():
    print('Day11')
    print('monkey business (20): ' + str(monkey_business(_get_monkeys(), 20)))
    print('monkey business (10000): ' +
          str(monkey_business(_get_monkeys(False), 10_000)))
