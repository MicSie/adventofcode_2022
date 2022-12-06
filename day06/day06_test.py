import day06.task as task    # The code to test
import unittest   # The test framework
from .context import basics as helpers


class Test_day06(unittest.TestCase):
    def test_find_data_marker(self):
        self.assertEqual(task.find_marker('bvwbjplbgvbhsrlpgdmjqwftvncz',4), 5)
        self.assertEqual(task.find_marker('nppdvjthqldpwncqszvftbrmjlhg',4), 6)
        self.assertEqual(task.find_marker('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg',4), 10)
        self.assertEqual(task.find_marker('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw',4), 11)

    def test_find_message_marker(self):
        self.assertEqual(task.find_marker('mjqjpqmgbljsphdztnvjfqwrcgsmlb',14), 19)
        self.assertEqual(task.find_marker('bvwbjplbgvbhsrlpgdmjqwftvncz',14), 23)
        self.assertEqual(task.find_marker('nppdvjthqldpwncqszvftbrmjlhg',14), 23)
        self.assertEqual(task.find_marker('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg',14), 29)
        self.assertEqual(task.find_marker('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw',14), 26)


if __name__ == '__main__':
    unittest.main()
