from collections import namedtuple
import unittest
import ansi
import change

Args = namedtuple('Args', ['subject', 'open', 'closed'])

response = [
        {
            '_number': 23,
            'status': 'open',
            'updated': '2021-04-28 21:20:45.1234',
            'subject': 'Cool story bro'
            },
        {
            '_number': 42,
            'status': 'closed',
            'updated': '2021-04-29 08:03:45.1234',
            'subject': 'yee-yee!'
            }
        ]

class TestThreads(unittest.TestCase):

    def test_create_change(self):
        c = change.Change(response[0])
        self.assertEqual(23, c.change_id)
        self.assertEqual('open', c.status)
        self.assertEqual('2021-04-28 21:20', c.datetime)
        self.assertEqual('Cool story bro', c.subject)

    def test_pad_status(self):
        c = change.Change(response[0])
        c.pad_status(6)
        self.assertEqual('open  ', c.status)

    def test_filter_changes(self):
        changes = [change.Change(data) for data in response]
        args = Args(subject='StoRy', open=None, closed=None)
        actual = list(change.filter_changes(changes, args))
        expected = [changes[0]]
        self.assertEqual(expected, actual)

    def test_sort_changes(self):
        changes = [change.Change(data) for data in response]
        actual = list(change.sort_changes(changes))
        expected = [changes[1], changes[0]]
        self.assertEqual(expected, actual)

    def test_create_output(self):
        changes = [change.Change(data) for data in response]
        actual = change.create_output(changes)
        output1 = ' '.join([
            ansi.format(23, [ansi.YELLOW]),
            ansi.format('open  ', [ansi.MAGENTA]),
            ansi.format('2021-04-28 21:20', [ansi.ITALIC]),
            ansi.format('Cool story bro', []),
            ])
        output2 = ' '.join([
            ansi.format(42, [ansi.YELLOW]),
            ansi.format('closed', [ansi.MAGENTA]),
            ansi.format('2021-04-29 08:03', [ansi.ITALIC]),
            ansi.format('yee-yee!', []),
            ])
        expected = '\n'.join([output1, output2])
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main(verbosity=2)
