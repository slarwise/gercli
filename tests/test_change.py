from collections import namedtuple
import json
import os
import unittest

import context
import change
import ansi

Args = namedtuple('Args', ['subject', 'open', 'closed'])

class TestThreads(unittest.TestCase):

    def setUp(self):
        filepath = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            'changes.json')
            )
        with open(filepath) as f:
            self.changes_data = json.load(f)
        self.maxDiff = None

    def test_create_change(self):
        c = change.Change(self.changes_data[0])
        self.assertEqual(23, c.change_id)
        self.assertEqual('open', c.status)
        self.assertEqual('2021-04-28 21:20', c.datetime)
        self.assertEqual('Fascinating subject', c.subject)

    def test_pad_status(self):
        c = change.Change(self.changes_data[0])
        c.pad_status(6)
        self.assertEqual('open  ', c.status)

    def test_filter_changes(self):
        changes = [change.Change(data) for data in self.changes_data]
        args = Args(subject='asCi', open=None, closed=None)
        actual = list(change.filter_changes(changes, args))
        expected = [changes[0]]
        self.assertEqual(expected, actual)

    def test_sort_changes(self):
        changes = [change.Change(data) for data in self.changes_data]
        actual = list(change.sort_changes(changes))
        expected = [changes[1], changes[0]]
        self.assertEqual(expected, actual)

    def test_create_output(self):
        changes = [change.Change(data) for data in self.changes_data]
        actual = change.create_output(changes, True)
        output1 = ' '.join([
            ansi.format(23, [ansi.YELLOW]),
            ansi.format('open  ', [ansi.MAGENTA]),
            ansi.format('2021-04-28 21:20', [ansi.ITALIC]),
            ansi.format('PS3', [ansi.YELLOW]),
            ansi.format('Fascinating subject', []),
            ])
        output2 = ' '.join([
            ansi.format(42, [ansi.YELLOW]),
            ansi.format('closed', [ansi.MAGENTA]),
            ansi.format('2021-04-29 08:03', [ansi.ITALIC]),
            ansi.format('PS5', [ansi.YELLOW]),
            ansi.format('yee-yee!', []),
            ])
        count_output = '2 changes'
        expected = '\n'.join([output1, output2, count_output])
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main(verbosity=2)
