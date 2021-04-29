from collections import namedtuple
import unittest
import ansi

import comment

Args = namedtuple('Args', ['subject', 'open', 'closed'])

response_no_context = {
            'id': '5',
            'patch_set': '3',
            'in_reply_to': '23',
            'author': {'name': 'arvid'},
            'message': 'Done',
            'updated': '2021-04-28 21:20:45.1234',
            }

response_line = {
            'id': '5',
            'patch_set': '3',
            'in_reply_to': '23',
            'author': {'name': 'arvid'},
            'message': 'Done',
            'updated': '2021-04-28 21:20:45.1234',
            'line': 3,
            }

response_range_one_line = {
            'id': '5',
            'patch_set': '3',
            'in_reply_to': '23',
            'author': {'name': 'arvid'},
            'message': 'Done',
            'updated': '2021-04-28 21:20:45.1234',
            'range': {
                'start_line': 1,
                'end_line': 1,
                'start_character': 5,
                'end_character': 11,
                },
            }

response_range_four_lines = {
            'id': '5',
            'patch_set': '3',
            'in_reply_to': '23',
            'author': {'name': 'arvid'},
            'message': 'Done',
            'updated': '2021-04-28 21:20:45.1234',
            'range': {
                'start_line': 1,
                'end_line': 4,
                'start_character': 5,
                'end_character': 4,
                },
            }

content_response = [
        'File starts here.',
        'Some content.',
        'Some more content.',
        'This is the end.',
        ]

filename = 'file.txt'

class TestComment(unittest.TestCase):

    def test_create_comment_no_context(self):
        c = comment.Comment(response_no_context, filename)
        self.assertEqual('5', c.id)
        self.assertEqual('3', c.patch_set)
        self.assertEqual('23', c.parent)
        self.assertEqual('arvid', c.author)
        self.assertEqual('Done', c.message)
        self.assertEqual('2021-04-28', c.date)
        self.assertEqual(filename, c.file)
        self.assertEqual('', c.context[0])
        self.assertEqual('', c.context[1])
        self.assertEqual('', c.context[2])

    def test_create_comment_line(self):
        c = comment.Comment(response_line, filename, content_response)
        self.assertEqual('5', c.id)
        self.assertEqual('3', c.patch_set)
        self.assertEqual('23', c.parent)
        self.assertEqual('arvid', c.author)
        self.assertEqual('Done', c.message)
        self.assertEqual('2021-04-28', c.date)
        self.assertEqual(filename, c.file)
        self.assertEqual('', c.context[0])
        self.assertEqual('Some more content.', c.context[1])
        self.assertEqual('', c.context[2])

    def test_create_comment_range_one_line(self):
        c = comment.Comment(response_range_one_line, filename, content_response)
        self.assertEqual('5', c.id)
        self.assertEqual('3', c.patch_set)
        self.assertEqual('23', c.parent)
        self.assertEqual('arvid', c.author)
        self.assertEqual('Done', c.message)
        self.assertEqual('2021-04-28', c.date)
        self.assertEqual(filename, c.file)
        self.assertEqual('File ', c.context[0])
        self.assertEqual('starts', c.context[1])
        self.assertEqual(' here.', c.context[2])

    def test_create_comment_range_four_lines(self):
        c = comment.Comment(response_range_four_lines, filename, content_response)
        self.assertEqual('5', c.id)
        self.assertEqual('3', c.patch_set)
        self.assertEqual('23', c.parent)
        self.assertEqual('arvid', c.author)
        self.assertEqual('Done', c.message)
        self.assertEqual('2021-04-28', c.date)
        self.assertEqual(filename, c.file)
        self.assertEqual('File ', c.context[0])
        self.assertEqual('starts here.\nSome content.\nSome more content.\nThis', c.context[1])
        self.assertEqual(' is the end.', c.context[2])

    def test_str(self):
        c = comment.Comment(response_no_context, filename)
        actual = str(c)
        expected = ' '.join([
            'arvid',
            ansi.format('Done', [ansi.GREEN, ansi.ITALIC])
            ])
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main(verbosity=2)
