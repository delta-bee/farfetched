import unittest
from fflib import *
class TestStripPath(unittest.TestCase):
    def test_strip_path(self):
        self.assertEqual(strip_path('saves/TopicExample/lessonmanifest.txt'), 'lessonmanifest.txt')
        self.assertEqual(strip_path('saves/TopicExample/lessonlists/chunkmanifest.txt'), 'chunkmanifest.txt')