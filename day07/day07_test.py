import os
import day07.task as task    # The code to test
import unittest   # The test framework
from .context import basics as helpers


class Test_day07(unittest.TestCase):
    def test_directory_init(self):
        directory = task.Directory()
        self.assertEqual(directory.get_name(), '/')
        self.assertEqual(directory.get_size(), 0)

        directory2 = task.Directory('test', directory)
        self.assertEqual(directory2.get_name(), 'test')
        self.assertEqual(directory2.get_size(), 0)
        self.assertEqual(directory2.get_parent().get_name(),
                         directory.get_name())

    def test_directory_files(self):
        directory = task.Directory()

        directory.add_file(task.File('file1', 1))
        self.assertEqual(directory.get_size(), 1)

        directory.add_file(task.File('file2', 2))
        self.assertEqual(directory.get_size(), 3)

    def test_directory_directories(self):
        directory = task.Directory()

        directory.add_file(task.File('file1', 1))
        directory.add_file(task.File('file2', 2))

        directory1 = task.Directory('Dir1')
        directory1.add_file(task.File('file3', 3))
        directory1.add_file(task.File('file4', 4))
        directory.add_directory(directory1)
        self.assertEqual(directory.get_size(), 10)

        directory2 = task.Directory('Dir2')
        directory2.add_file(task.File('file5', 5))
        directory.add_directory(directory2)
        self.assertEqual(directory.get_size(), 15)

        directory3 = task.Directory('Dir3')
        directory3.add_file(task.File('file6', 10))
        directory2.add_directory(directory3)
        self.assertEqual(directory.get_size(), 25)

    def _get_simple_test_directory(self) -> 'task.Directory':
        # /
        # - Dir1
        # - Dir2
        #  - Dir 3

        root = task.Directory()
        directory1 = task.Directory('Dir1')
        root.add_directory(directory1)
        directory2 = task.Directory('Dir2')
        root.add_directory(directory2)
        directory3 = task.Directory('Dir3')
        directory2.add_directory(directory3)
        return root

    def test_directory_find(self):
        directory = self._get_simple_test_directory()

        test = directory.find_directory('Dir1')
        self.assertEqual(test.get_name(), 'Dir1')

        test = directory.find_directory('non_existing')
        self.assertEqual(test, None)

        test = directory.find_directory('Dir2').find_directory('Dir3')
        self.assertEqual(test.get_name(), 'Dir3')

    def test_get_all_directories(self):
        directories = self._get_simple_test_directory().get_all_directories()

        self.assertNotEqual(next(filter((lambda directory: directory.get_name() == 'Dir1'), directories), None), None)
        self.assertNotEqual(next(filter((lambda directory: directory.get_name() == 'Dir2'), directories), None), None)
        self.assertNotEqual(next(filter((lambda directory: directory.get_name() == 'Dir3'), directories), None), None)

    def test_filesystem_change_directory(self):
        filesystem = task.Filesystem(root=self._get_simple_test_directory())

        self.assertEqual(filesystem.get_current_directory().get_name(), '/')

        filesystem.change_directory('Dir1')
        self.assertEqual(filesystem.get_current_directory().get_name(), 'Dir1')

        filesystem.change_directory('non_existing')
        self.assertEqual(filesystem.get_current_directory().get_name(), 'Dir1')

        filesystem.change_directory('..')
        self.assertEqual(filesystem.get_current_directory().get_name(), '/')

        filesystem.change_directory('Dir2')
        filesystem.change_directory('Dir3')
        self.assertEqual(filesystem.get_current_directory().get_name(), 'Dir3')

        filesystem.change_directory('Dir1')
        self.assertEqual(filesystem.get_current_directory().get_name(), 'Dir3')

        filesystem.change_directory('/')
        self.assertEqual(filesystem.get_current_directory().get_name(), '/')

    def test_get_next_instrction(self):
        instructions = ['$ cd /','$ ls', 'dir a']
        self.assertEqual(task.split_instructions(instructions), [['$ cd /'],['$ ls', 'dir a']])

        instructions.append('$ cd abc')
        self.assertEqual(task.split_instructions(instructions), [['$ cd /'],['$ ls', 'dir a'], ['$ cd abc']])

    def test_read_list(self):
        instructions = ['$ ls','dir a','14848514 b.txt','8504156 c.dat','dir d']
        directory = task.Directory()

        task.read_list(instructions, directory)
        self.assertEqual(directory.get_size(), 14848514 + 8504156)

        self.assertEqual(directory.find_directory('a').get_name(), 'a')
        self.assertEqual(directory.find_directory('d').get_name(), 'd')

        file = directory.find_file('b.txt')
        self.assertEqual(file.get_name(), 'b.txt')
        self.assertEqual(file.get_size(), 14848514)
        
        file = directory.find_file('c.dat')
        self.assertEqual(file.get_name(), 'c.dat')
        self.assertEqual(file.get_size(), 8504156)

    def test_sum_smallest_directories(self):
        helpers.ensure_directory(os.path.dirname(__file__))
        self.assertEqual(task.sum_smallest_directories(task.Filesystem('testinput'), 100000), 95437)

    def test_directory_to_delete(self):
        helpers.ensure_directory(os.path.dirname(__file__))
        self.assertEqual(task.directory_size_to_delete(task.Filesystem('testinput')), 24933642)

if __name__ == '__main__':
    unittest.main()
