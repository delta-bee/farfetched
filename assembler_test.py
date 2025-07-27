import unittest, os
from assembler import *
from unittest import mock
from unittest.mock import mock_open, patch

class TestGeneralUtils(unittest.TestCase):
    def test_strip_punctuation(self):
        self.assertEqual(strip_punctuation('Hello, world!'), 'Hello world')
        self.assertEqual(strip_punctuation('No punctuation'), 'No punctuation')

    def test_strip_path(self):
        self.assertEqual(strip_path('Topic2/Lesson/Chunk1', 2), 'Chunk1')
        self.assertEqual(strip_path('Topic2/Lesson/Chunk1', 1), 'Lesson')
        self.assertEqual(strip_path('Topic2/Lesson/Chunk1', 0), 'Topic2')

    def test_flatten_list(self):
        self.assertEqual(flatten_list([['a', 'b'], ['c', 'd']]), ['a', 'b', 'c', 'd'])
        self.assertEqual(flatten_list([['a', 'b', ['c', 'd']], [['e', 'f'], ['g', 'h']]]), ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])

class TestWriteContentsToDrive(unittest.TestCase):
    def test_write_contents_to_drive_mismatching_lists(self):
        with self.assertRaises(ValueError):
            write_contents_to_drive(
                ['Topic2/Lesson/Chunk1', 'Topic2/Lesson/Chunk2'],
                ['This is a line', 'This is another line', 'This is a third line, which is too many.']
            )

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_write_contents_to_drive_correct_usage(self, mock_open):
        paths = ['test1.txt', 'test2.txt']
        contents = ['This is a line', 'This is another line']
        write_contents_to_drive(paths, contents)
        mock_open.assert_any_call(paths[0], 'w')
        mock_open.assert_any_call(paths[1], 'w')
        # Verify that the correct content is written to each file
        mock_open().write.assert_any_call(contents[0])
        mock_open().write.assert_any_call(contents[1])

class TestIfNotExistCreateIt(unittest.TestCase):
    @mock.patch('os.mkdir')
    @mock.patch('os.path.exists')
    def test_does_not_exist(self, mock_exists, mock_mkdir):
        # If there is no directory, it should create the directory.
        mock_exists.return_value = False
        if_not_exist_create_it('test_dir')
        mock_mkdir.assert_called_once_with('test_dir')
    @mock.patch('os.mkdir')
    @mock.patch('os.path.exists')
    def test_with_tuple(self, mock_exists, mock_mkdir):
        mock_exists.return_value = False
        if_not_exist_create_it(('test_dir', 'test_dir2'))
        mock_mkdir.assert_called_once_with('test_dir/test_dir2')
    @mock.patch('os.mkdir')
    @mock.patch('os.path.exists')
    def test_with_args(self, mock_exists, mock_mkdir):
        mock_exists.return_value = False
        if_not_exist_create_it('test_dir', 'test_arg')
        mock_mkdir.assert_called_once_with('test_dir/test_arg')
    def test_with_tuple_and_args(self):
        with self.assertRaises(TypeError):
            if_not_exist_create_it(('test_dir', 'test_dir2'), 'test_arg')
    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            if_not_exist_create_it(123)
        with self.assertRaises(TypeError):
            if_not_exist_create_it(['test_dir', 'test_dir2'])
    @mock.patch('os.mkdir')
    @mock.patch('os.path.exists')
    def test_does_exist(self, mock_exists, mock_mkdir):
        # If there is a directory, it should do nothing.
        mock_exists.return_value = True
        if_not_exist_create_it('test_dir')
        mock_mkdir.assert_not_called()
class TestCheckIfPathValid(unittest.TestCase):
    def test_valid_path(self):
        self.assertTrue(is_path_valid('test_dir'))
    #If anyone has ideas for testing the false stuff cross-platform, let me know. For now, this'll do.
if __name__ == '__main__':
    unittest.main()
