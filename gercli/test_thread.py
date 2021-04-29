from collections import namedtuple
import unittest
import ansi

import comment
import thread

Args = namedtuple('Args', [])

comments_response = [
        {
            'id': '1',
            'patch_set': '3',
            'range': {
                'start_line': 1,
                'end_line': 4,
                'start_character': 5,
                'end_character': 4,
                },
            'author': {'name': 'arvid'},
            'message': 'I will update this',
            'updated': '2021-04-27 21:20:45.1234',
            },
        {
            'id': '2',
            'patch_set': '3',
            'range': {
                'start_line': 1,
                'end_line': 4,
                'start_character': 5,
                'end_character': 4,
                },
            'in_reply_to': '1',
            'author': {'name': 'arvid'},
            'message': 'Done',
            'updated': '2021-04-28 21:20:45.1234',
            },
        {
            'id': '3',
            'patch_set': '2',
            'line': 0,
            'author': {'name': 'arvid'},
            'message': 'Yes',
            'updated': '2021-04-26 21:20:45.1234',
            },
        ]

content_response = [
        'File starts here.',
        'Some content.',
        'Some more content.',
        'This is the end.',
        ]

filename = 'file.txt'

class TestThreads(unittest.TestCase):

    def test_create_thread_two_comments_range(self):
        comments = [comment.Comment(data, filename, content_response)
                for data in comments_response[0:2]]
        t = thread.Thread(comments)
        self.assertEqual(comments, t.comments)
        self.assertEqual('File ', t.context[0])
        self.assertEqual('starts here.\nSome content.\nSome more content.\nThis', t.context[1])
        self.assertEqual(' is the end.', t.context[2])

    def test_str(self):
        comments = [comment.Comment(data, filename, content_response)
                for data in comments_response[0:2]]
        t = thread.Thread(comments)
        expected = ''.join([
            ansi.format('PS3', [ansi.YELLOW]),
            ' ',
            ansi.format('file.txt', [ansi.YELLOW]),
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
            '    arvid ',
            ansi.format('I will update this', [ansi.GREEN, ansi.ITALIC]),
            '\n',
            '    ',
            ansi.format('2021-04-28', [ansi.BLUE]),
            '\n',
            '    arvid ',
            ansi.format('Done', [ansi.GREEN, ansi.ITALIC]),
            ])
        self.assertEqual(expected, str(t))

if __name__ == '__main__':
    unittest.main(verbosity=2)
