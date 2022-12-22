import day16.task as task    # The code to test
import unittest   # The test framework
from .context import basics as helpers


class Test_day16(unittest.TestCase):
    def _get_valves(self):
        return task.read_input('testinput.txt')
    
    def test_shortest_rout_DD_JJ(self):
        valves = self._get_valves()
        self.assertEqual(task.find_shortest_route_testing('DD', 'JJ', valves), ['AA', 'II', 'JJ'])
    
    def test_shortest_rout_JJ_HH(self):
        valves = self._get_valves()
        self.assertEqual(task.find_shortest_route_testing('JJ', 'HH', valves), ['II', 'AA', 'DD', 'EE', 'FF', 'GG', 'HH'])

    def test_open_valves(self):
        valves = self._get_valves()
        self.assertEqual(task.open_valves(valves),1651)

    def test_open_valves_helping_elephant(self):
        valves = self._get_valves()
        self.assertEqual(task.open_valves(valves,True),1707)


if __name__ == '__main__':
    unittest.main()
