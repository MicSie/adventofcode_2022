import basics.helpers as helpers   # The code to test
import unittest   # The test framework


class Test_Basics(unittest.TestCase):
    def test_read_file(self):
        helpers.ensure_directory('basics')
        self.assertEqual(helpers.read_file('simpletestfile'), [
            'first', '2dn', '', '4th'])


if __name__ == '__main__':
    unittest.main()
