from collections import namedtuple
import json
import os
import unittest

import context
import comment
import ansi
import thread

class TestThreads(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

        comments_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    'comments.json'
                    )
                )
        with open(comments_path) as f:
            self.comments_data = json.load(f)

        file_contents_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    'file_contents.txt'
                    )
                )
        with open(file_contents_path) as f:
            text = f.read()
            self.file_contents = text.split('\n')

    def test_create_thread_two_comments_range(self):
        filename = 'file1'
        data = self.comments_data[filename][0:2]
        comments = [comment.Comment(d, filename, self.file_contents)
                for d in data]
        t = thread.Thread(comments)
        self.assertEqual(comments, t.comments)
        self.assertEqual('File ', t.context[0])
        self.assertEqual('starts here.\nSome content.\nSome more content.\nThis', t.context[1])
        self.assertEqual(' is the end.', t.context[2])

    def test_str(self):
        filename = 'file1'
        data = self.comments_data[filename][0:2]
        comments = [comment.Comment(d, filename, self.file_contents)
                for d in data]
        t = thread.Thread(comments)
        expected = ''.join([
            ansi.format('PS3', [ansi.YELLOW]),
            ' ',
            ansi.format('file1', [ansi.YELLOW]),
            '\n',
            'File ',
            ansi.format(
                'starts here.\nSome content.\nSome more content.\nThis',
                [ansi.GREEN, ansi.ITALIC],
                ),
            ' is the end.',
            '\n',
            '    ',
            ansi.format('2021-04-27', [ansi.BLUE]),
            '\n',
            '    Name1 ',
            ansi.format('Can you update this, Name2?', [ansi.GREEN, ansi.ITALIC]),
            '\n',
            '    ',
            ansi.format('2021-04-28', [ansi.BLUE]),
            '\n',
            '    Name2 ',
            ansi.format('Done', [ansi.GREEN, ansi.ITALIC]),
            ])
        self.assertEqual(expected, str(t))

if __name__ == '__main__':
    unittest.main(verbosity=2)
