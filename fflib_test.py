import unittest, tempfile, shutil
from unittest import mock
from fflib import *
class TestStripPath(unittest.TestCase):
    def test_strip_path(self):
        self.assertEqual(strip_path('saves/TopicExample/lessonmanifest.txt'), 'lessonmanifest.txt')
        self.assertEqual(strip_path('saves/TopicExample/lessonlists/chunkmanifest.txt'), 'chunkmanifest.txt')
class TestGetImmediateChildDirectories(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        os.mkdir(os.path.join(self.temp_dir.name, 'test1'))
        os.mkdir(os.path.join(self.temp_dir.name, 'test2'))
    def tearDown(self):
        self.temp_dir.cleanup()
    def test_get_immediate_child_directories(self):
        self.assertEqual(get_immediate_child_directories(self.temp_dir.name), [os.path.join(self.temp_dir.name, 'test1'), os.path.join(self.temp_dir.name, 'test2')])
if __name__ == '__main__':
    unittest.main()